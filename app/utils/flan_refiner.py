from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from langdetect import detect  # For language detection

# Load model and tokenizer for FLAN-T5
tokenizer_flan = AutoTokenizer.from_pretrained("google/flan-t5-large")
model_flan = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")

# Setup device (GPU or CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_flan.to(device)

def refine_japanese(text: str) -> str:
    """
    Refinement: If text is in Japanese, refine it to polite Japanese (keigo).
    If text is in Indonesian, refine it to natural casual Indonesian.
    """
    try:
        # Detect the language of the input text
        detected_language = detect(text)

        # If the text is in Japanese, refine it to polite Japanese (keigo)
        if detected_language == "ja":
            prompt = f"Please rephrase the following sentence into polite Japanese (keigo) but still sounding natural:\n{text}"
            inputs = tokenizer_flan(prompt, return_tensors="pt").to(device)
            output = model_flan.generate(
                **inputs,
                max_length=100,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
            result = tokenizer_flan.decode(output[0], skip_special_tokens=True).strip()

        # If the text is in Indonesian, refine it to natural casual Indonesian
        elif detected_language == "id":
            prompt = f"Please rephrase the following sentence in natural and casual Indonesian:\n{text}"
            inputs = tokenizer_flan(prompt, return_tensors="pt").to(device)
            output = model_flan.generate(
                **inputs,
                max_length=100,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
            result = tokenizer_flan.decode(output[0], skip_special_tokens=True).strip()

        # Return the refined result
        return result

    except Exception as e:
        print("❌ Flan refine failed:", e)
        return text
