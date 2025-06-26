#!/usr/bin/env python3

import os
import time
import logging
import re
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def sanitize_filename(filename: str) -> str:
    """Sanitize the filename to remove/replace invalid characters."""
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

def CheckForFiles(audio_dir: str = None) -> str:
    """
    Check for .mp3 files in the audio directory.
    Returns the first file found, or None if none exist.
    """
    if audio_dir is None:
        audio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'audio'))
    mp3_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.mp3')]
    if mp3_files:
        file_name = mp3_files[0]
        logging.info(f"File found: {file_name}")
        return file_name
    else:
        logging.info("No '.mp3' files found in the audio directory")
        return None

def init_pipeline(device: str, torch_dtype):
    """Initialize and return the ASR pipeline."""
    model_id = "openai/whisper-large-v3-turbo"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    return pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
    )

def Transcribe(file_name: str, transcripts_dir: str = None, pipeline_obj=None) -> bool:
    """
    Transcribe the given audio file and save the result in the transcripts directory.
    Returns True on success, False on failure.
    If pipeline_obj is None, it will be initialized automatically (for backward compatibility).
    """
    if file_name is None:
        logging.warning("No file found. Exiting transcription...")
        return False
    if pipeline_obj is None:
        logging.info("No pipeline object provided to Transcribe(). Initializing pipeline (this may be slow)...")
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        pipeline_obj = init_pipeline(device, torch_dtype)
    if transcripts_dir is None:
        transcripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'transcripts'))
    os.makedirs(transcripts_dir, exist_ok=True)
    try:
        start_time = time.time()
        logging.info("Transcribing...")
        result = pipeline_obj(file_name, generate_kwargs={"language": "english"}, return_timestamps=True)
        logging.info("Transcription completed")
        base_filename = os.path.splitext(os.path.basename(file_name))[0]
        base_filename = sanitize_filename(base_filename)
        output_filename = os.path.join(transcripts_dir, f"{base_filename}.txt")
        transcribed_text = result["text"]
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(transcribed_text)
        logging.info(f"Transcription saved to {output_filename}")
        time.sleep(1)  # Ensure file handle is released
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                logging.info(f"Audio file {file_name} deleted from audio directory.")
            except Exception as e:
                logging.error(f"Failed to delete audio file {file_name}: {e}")
        else:
            logging.warning(f"Audio file {file_name} was not found for deletion (may have already been removed).")
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Transcription completed in {elapsed_time:.2f} seconds")
        return True
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return False