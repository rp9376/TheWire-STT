#!/usr/bin/env python3

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os
import time  # Import the time module for timing
# Start timing
start_time = time.time()

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=256,
    torch_dtype=torch_dtype,
    device=device,
)

file_name = "The Wire  - June 13, 2024.mp3"



result = pipe(file_name, generate_kwargs={"language": "english"})


# Print the transcribed text
print(result["text"])

# Print the type of result
print(type(result))

# Print all keys in the result dictionary
print(result.keys())

# Extract the base filename without the extension
base_filename = os.path.splitext(os.path.basename(file_name))[0]

# Define the output filename with the desired extension
output_filename = f"{base_filename}.txt"

# Extract the transcribed text
transcribed_text = result["text"]

# Write the transcribed text to the output file
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(transcribed_text)

print(f"Transcription saved to {output_filename}")


# End timing
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Transcription completed in {elapsed_time:.2f} seconds")