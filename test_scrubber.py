import unittest
from pii_scrubber import PIIScrubber

class TestPIIScrubber(unittest.TestCase):
    def setUp(self):
        self.scrubber = PIIScrubber()

    def test_email_masking(self):
        text = "Связаться по адресу test.user@digitaltrust.living для проверки."
        masked, mapping = self.scrubber.mask_data(text)
        self.assertIn("[EMAIL_1]", masked)
        self.assertNotIn("test.user@digitaltrust.living", masked)
        
        # Проверяем обратную сборку
        unmasked = self.scrubber.unmask_data(masked, mapping)
        self.assertEqual(text, unmasked)

    def test_edrpou_masking(self):
        text = "Код организации: 12345678."
        masked, mapping = self.scrubber.mask_data(text)
        self.assertIn("[EDRPOU_1]", masked)
        
        unmasked = self.scrubber.unmask_data(masked, mapping)
        self.assertEqual(text, unmasked)

    def test_empty_text(self):
        masked, mapping = self.scrubber.mask_data("")
        self.assertEqual(masked, "")
        self.assertEqual(mapping, {})

if __name__ == "__main__":
    unittest.main()
