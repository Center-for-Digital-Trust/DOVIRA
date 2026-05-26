from pii_scrubber import PIIScrubber

def run_demo():
    print("=== DOVIRA PII Scrubber: Демонстрация работы ===")
    
    # 1. Инициализация ядра безопасности
    scrubber = PIIScrubber()
    
    # 2. Имитация исходного промпта сотрудника (содержит PII)
    original_prompt = """
    Будь ласка, зроби аналіз звернення громадянина.
    Ім'я: Іван Іваненко
    Email: ivan.test@digitaltrust.living
    Телефон: +38(050)123-45-67
    ЄДРПОУ організації: 12345678
    Паспорт: AB123456
    Суть: Прошу надати юридичну довідку.
    """
    
    print("\n[ШАГ 1] Оригинальный текст (ОПАСНО ОТПРАВЛЯТЬ В ОБЛАКО):")
    print(original_prompt)
    
    # 3. Маскировка данных на компьютере пользователя
    masked_prompt, mapping = scrubber.mask_data(original_prompt)
    
    print("\n[ШАГ 2] Замаскированный текст (БЕЗОПАСНО ДЛЯ ПЕРЕДАЧИ В ИИ):")
    print(masked_prompt)
    print("\nКарта токенов (надежно хранится только локально):")
    for token, val in mapping.items():
        print(f"  {token} -> {val}")
    
    # 4. Имитация ответа от облачной LLM (ИИ видит только токены)
    mock_ai_response = """
    Аналіз звернення завершено.
    Клієнту з поштою [EMAIL_1] та телефоном [PHONE_1] необхідно надіслати форму #42.
    Код ЄДРПОУ [EDRPOU_1] та документ [PASSPORT_1] пройшли первинну перевірку в базі.
    """
    
    print("\n[ШАГ 3] Ответ от облачного ИИ (содержит только токены):")
    print(mock_ai_response)
    
    # 5. Демаскировка: подстановка реальных данных обратно в ответ
    final_result = scrubber.unmask_data(mock_ai_response, mapping)
    
    print("\n[ШАГ 4] Финальный результат на экране пользователя (ДАННЫЕ ВОССТАНОВЛЕНЫ):")
    print(final_result)
    
    # 6. Сохранение безопасного следа в реестр датасета
    print("\n[ШАГ 5] Сохранение полностью анонимного лога в dataset.json...")
    scrubber.save_to_dataset(masked_prompt, mock_ai_response)
    print("Успешно! Операция завершена в рамках концепции Zero-Data Retention.")

if __name__ == "__main__":
    run_demo()
