import re
import json
from datetime import datetime

class PIIScrubber:
    def __init__(self):
        # Строгие регулярные выражения для поиска конфиденциальных данных
        self.regex_patterns = {
            "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "PHONE": r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            "EDRPOU": r'\b\d{8}\b',  # Украинский код ЕДРПОУ (8 цифр)
            "PASSPORT": r'\b[A-Z]{2}\d{6}\b|\b\d{9}\b'  # Паспортные данные
        }

    def mask_data(self, text: str):
        """
        Ищет PII в тексте, заменяет их на анонимные токены
        и возвращает очищенный текст и карту соответствия для обратной сборки.
        """
        if not text:
            return "", {}

        masked_text = text
        mapping = {}
        
        for key, pattern in self.regex_patterns.items():
            matches = re.findall(pattern, masked_text)
            unique_matches = list(dict.fromkeys(matches)) # Убираем дубликаты
            
            for index, match in enumerate(unique_matches, start=1):
                token = f"[{key}_{index}]"
                mapping[token] = match
                masked_text = masked_text.replace(match, token)
                
        return masked_text, mapping

    def unmask_data(self, text: str, mapping: dict) -> str:
        """
        Локально возвращает реальные данные на место токенов в ответе ИИ.
        """
        if not text or not mapping:
            return text

        unmasked_text = text
        for token, original_value in mapping.items():
            unmasked_text = unmasked_text.replace(token, original_value)
            
        return unmasked_text

    def save_to_dataset(self, masked_prompt: str, masked_response: str, filename="dataset.json"):
        """
        Формирует безопасный датасет для будущего обучения моделей.
        Записывает только деперсонализированные данные!
        """
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prompt": masked_prompt,
            "response": masked_response
        }
        
        try:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []
                
            data.append(log_entry)
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving dataset entry: {e}")
