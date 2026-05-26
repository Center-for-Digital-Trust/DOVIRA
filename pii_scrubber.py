import re
import json
import threading
from datetime import datetime
from typing import Dict, Tuple


class PIIScrubber:
    def __init__(self):
        # Компилированные regex (быстрее и безопаснее)
        self.patterns = {
            "EMAIL": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
            "PHONE": re.compile(r"\+?\d[\d\-\(\) ]{7,}\d"),
            "EDRPOU": re.compile(r"\b\d{8}\b"),
            "PASSPORT": re.compile(r"\b[A-Z]{2}\d{6}\b|\b\d{9}\b"),
        }

        self._file_lock = threading.Lock()

    # ===================== MASK =====================
    def mask_data(self, text: str) -> Tuple[str, Dict[str, str]]:
        if not text:
            return "", {}

        mapping: Dict[str, str] = {}
        masked_text = text

        for key, pattern in self.patterns.items():
            value_to_token = {}

            def replacer(match):
                value = match.group(0)

                if value not in value_to_token:
                    token = f"[{key}_{len(value_to_token) + 1}]"
                    value_to_token[value] = token
                    mapping[token] = value

                return value_to_token[value]

            masked_text = pattern.sub(replacer, masked_text)

        return masked_text, mapping

    # ===================== UNMASK =====================
    def unmask_data(self, text: str, mapping: Dict[str, str]) -> str:
        if not text or not mapping:
            return text

        # Защита от пересечений токенов (например EMAIL_1 и EMAIL_10)
        for token in sorted(mapping.keys(), key=len, reverse=True):
            text = text.replace(token, mapping[token])

        return text

    # ===================== SAVE =====================
    def save_to_dataset(
        self,
        masked_prompt: str,
        masked_response: str,
        filename: str = "dataset.json",
    ) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": masked_prompt,
            "response": masked_response,
        }

        with self._file_lock:
            try:
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = []

                data.append(entry)

                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

            except Exception as e:
                # Лучше чем print — можно заменить на logging
                raise RuntimeError(f"Failed to save dataset: {e}")
