from pii_scrubber import PIIScrubber
import logging
from typing import Tuple, Dict


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class PIIDemo:
    def __init__(self):
        self.scrubber = PIIScrubber()

    def get_sample_prompt(self) -> str:
        return """
Будь ласка, зроби аналіз звернення громадянина.
Ім'я: Іван Іваненко
Email: ivan.test@digitaltrust.living
Телефон: +38(050)123-45-67
ЄДРПОУ організації: 12345678
Паспорт: AB123456
Суть: Прошу надати юридичну довідку.
"""

    def simulate_ai_response(self) -> str:
        return """
Аналіз звернення завершено.
Клієнту з поштою [EMAIL_1] та телефоном [PHONE_1] необхідно надіслати форму #42.
Код ЄДРПОУ [EDRPOU_1] та документ [PASSPORT_1] пройшли первинну перевірку.
"""

    def run(self) -> None:
        logging.info("=== DOVIRA PII Scrubber Demo ===")

        try:
            # 1. Исходные данные
            prompt = self.get_sample_prompt()
            logging.info("STEP 1: Original prompt loaded")

            # 2. Маскирование
            masked_prompt, mapping = self.scrubber.mask_data(prompt)
            logging.info("STEP 2: Data masked successfully")

            print("\n--- SAFE PROMPT ---")
            print(masked_prompt)

            # ⚠️ Mapping не логируем полностью!
            logging.info(f"Tokens created: {len(mapping)}")

            # 3. Ответ от AI
            ai_response = self.simulate_ai_response()
            logging.info("STEP 3: AI response simulated")

            print("\n--- AI RESPONSE (TOKENIZED) ---")
            print(ai_response)

            # 4. Демаскирование
            final_response = self.scrubber.unmask_data(ai_response, mapping)
            logging.info("STEP 4: Data restored")

            print("\n--- FINAL RESPONSE ---")
            print(final_response)

            # 5. Сохранение
            self.scrubber.save_to_dataset(masked_prompt, ai_response)
            logging.info("STEP 5: Dataset saved (masked only)")

            logging.info("Demo completed successfully ✅")

        except Exception as e:
            logging.error(f"Demo failed: {e}")
            raise


if __name__ == "__main__":
    demo = PIIDemo()
    demo.run()
