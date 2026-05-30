from pii_scrubber import PIIScrubber
import logging
from typing import Tuple, Dict


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class PIIDemo: 
def __init__(self): 
self.scrubber = PIIScrubber() 

def get_sample_prompt(self) -> str: 
return """
Be kind, do an analysis of the beastly giant.
Name: Ivan Ivanenko
Email: ivan.test@digitaltrust.living
Phone: +38(050)123-45-67
EDRPOU organization: 12345678
Passport: AB123456
Bottom line: Please provide legal evidence.
""" 

def simulate_ai_response(self) -> str: 
return """
The animal analysis is completed.
The client with mail [EMAIL_1] and phone [PHONE_1] must send form #42.
The EDRPOU code [EDRPOU_1] and document [PASSPORT_1] have undergone initial verification.
""" 

def run(self) -> None: 
logging.info("=== DOVIRA PII Scrubber Demo ===") 

try: 
# 1. Initial data 
prompt = self.get_sample_prompt() 
logging.info("STEP 1: Original prompt loaded") 

#2. Masking 
masked_prompt, mapping = self.scrubber.mask_data(prompt) 
logging.info("STEP 2: Data masked successfully") 

print("\n--- SAFE PROMPT ---") 
print(masked_prompt) 

# ⚠️ Mapping is not completely logged! 
logging.info(f"Tokens created: {len(mapping)}") 

#3. Answer from AI 
ai_response = self.simulate_ai_response() 
logging.info("STEP 3: AI response simulated") 

print("\n--- AI RESPONSE (TOKENIZED) ---") 
print(ai_response) 

#4. Unmasking 
final_response = self.scrubber.unmask_data(ai_response, mapping) 
logging.info("STEP 4: Data restored") 

print("\n--- FINAL RESPONSE ---") 
print(final_response) 

#5. Saving 
self.scrubber.save_to_dataset(masked_prompt, ai_response) 
logging.info("STEP 5: Dataset saved (masked only)") 

logging.info("Demo completed successfully ✅") 

except Exception as e: 
logging.error(f"Demo failed: {e}") 
raise
Отправить отзыв

if __name__ == "__main__":
    demo = PIIDemo()
    demo.run()
