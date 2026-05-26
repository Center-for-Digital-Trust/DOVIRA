import unittest
from pii_scrubber import PIIScrubber


class TestPIIScrubber(unittest.TestCase):

    def setUp(self):
        self.scrubber = PIIScrubber()

    # ✅ БАЗОВЫЕ

    def test_email_masking(self):
        text = "Email: test.user@digitaltrust.living"
        masked, mapping = self.scrubber.mask_data(text)

        self.assertIn("[EMAIL_1]", masked)
        self.assertNotIn("test.user@digitaltrust.living", masked)

        unmasked = self.scrubber.unmask_data(masked, mapping)
        self.assertEqual(text, unmasked)

    def test_empty_text(self):
        masked, mapping = self.scrubber.mask_data("")
        self.assertEqual(masked, "")
        self.assertEqual(mapping, {})

    # ✅ МНОЖЕСТВЕННЫЕ PII

    def test_multiple_pii(self):
        text = "Email test@mail.com, phone +380501234567, код 12345678"
        masked, mapping = self.scrubber.mask_data(text)

        self.assertIn("[EMAIL_1]", masked)
        self.assertIn("[PHONE_1]", masked)
        self.assertIn("[EDRPOU_1]", masked)

        self.assertEqual(len(mapping), 3)

        unmasked = self.scrubber.unmask_data(masked, mapping)
        self.assertEqual(text, unmasked)

    # ✅ ДУБЛИКАТЫ

    def test_duplicate_values(self):
        text = "Email test@mail.com и снова test@mail.com"
        masked, mapping = self.scrubber.mask_data(text)

        self.assertEqual(masked.count("[EMAIL_1]"), 2)
        self.assertEqual(len(mapping), 1)

    # ✅ НЕТ PII

    def test_no_pii(self):
        text = "Это просто текст без персональных данных"
        masked, mapping = self.scrubber.mask_data(text)

        self.assertEqual(text, masked)
        self.assertEqual(mapping, {})

    # ✅ PASSPORT

    def test_passport(self):
        text = "Паспорт AB123456"
        masked, mapping = self.scrubber.mask_data(text)

        self.assertIn("[PASSPORT_1]", masked)

        unmasked = self.scrubber.unmask_data(masked, mapping)
        self.assertEqual(text, unmasked)

    # ✅ ПЕРЕСЕЧЕНИЯ ТОКЕНОВ

    def test_token_collision(self):
        text = "Emails: test1@mail.com, test10@mail.com"
        masked, mapping = self.scrubber.mask_data(text)

        # Проверяем оба токена существуют
        self.assertIn("[EMAIL_1]", masked)
        self.assertIn("[EMAIL_2]", masked)

        # Проверяем корректную обратную замену
        unmasked = self.scrubber.unmask_data(masked, mapping)
        self.assertEqual(text, unmasked)


if __name__ == "__main__":
    unittest.main()
