#!/usr/bin/env python3

import os
import time  # Import the time module for timing

clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def CheckForFiles():
    # Check if there are any ".mp3" files available in the current directory
    mp3_files = [f for f in os.listdir('.') if f.endswith('.mp3')]

    # If there are any ".mp3" files, put the first filename to a variable
    if mp3_files:
        file_name = mp3_files[0]
        print("File found: ", file_name)
        return file_name
    else:
        print("No '.mp3' files found in the current directory")
        return None
    

def Transcribe(file_name):
    if file_name is None:
        print("No file found. Exiting transcription...")
        return
    import torch
    from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

    # Start timing
    start_time = time.time()
    print ("Setting up the model...")
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3-turbo"

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
        torch_dtype=torch_dtype,
        device=device,
    )

    print("Transcribing...")
    result = pipe(file_name, generate_kwargs={"language": "english"})
    print("Transcription completed")

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
    

if __name__ == "__main__":
    clear_screen()
    file_name = CheckForFiles()
    print("File to transcribe: ", file_name)
    Transcribe(file_name)