#!/usr/bin/env python3

from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

# Load the model and tokenizer
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

# Read the content from text.txt
with open('The Wire  - June 13, 2024.txt', 'r', encoding='utf-8') as file:
    article_en = file.read()

# Translate English to Slovenian
tokenizer.src_lang = "en_XX"
encoded_en = tokenizer(article_en, return_tensors="pt")
generated_tokens = model.generate(
    **encoded_en,
    forced_bos_token_id=tokenizer.lang_code_to_id["sl_SI"]
)
translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

# Write the translated text to output.txt
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write(translated_text)

print("Translation completed and written to output.txt")
