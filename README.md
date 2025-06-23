# TheWire-STT

This project automates the process of downloading, transcribing, and translating episodes of "The Wire" (from S2Underground on YouTube). It also provides a utility to interact with an Ollama LLM server.

## Features

- **Automatic Download:**  
  Downloads new "The Wire" videos from the S2Underground YouTube channel and extracts their audio as `.mp3` files.

- **Speech-to-Text Transcription:**  
  Uses OpenAI Whisper (via HuggingFace Transformers) to transcribe the audio files to English text.

- **Translation:**  
  Translates the English transcript to Slovenian using Facebook's mBART model.

- **Ollama LLM Client:**  
  Includes a script to send prompts to a remote Ollama server running Llama 3.1 and print the response.

- **Automation:**  
  The main script (`main.py`) orchestrates the download, transcription, and cleanup in a loop.

## Project Structure

- `services/transcription/` — Fetches videos, transcribes audio, and interacts with Ollama LLM
- `services/api/` — Database and API for storing/fetching transcriptions
- `services/web/` — Web frontend
- `services/mobile/` — Mobile app (future)
- `data/` — Shared data (audio, transcripts, etc.)
- `docker/` — Docker and compose files
- `config/` — Configuration files

## Running with Docker
See `docker/README.md` for details.

---

# Legacy Files (to be moved):
- `AudioDownloader_TheWire.py`
- `main.py`
- `Ollama_Connection.py`
- `Speach2Text_Turbo.py`
- `translate.py`
- `requirements.txt`
- `output.txt`
- `video_list.txt`
- `The Wire - June 14, 2025 - Priority.mp3`
- `The Wire - November 28, 2024.txt`

These will be moved to appropriate service folders.

## Usage

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Run the main automation:**
   ```
   python3 main.py
   ```

3. **Translate a transcript:**
   ```
   python3 translate.py
   ```

4. **Chat with Ollama:**
   ```
   python3 Ollama_Connection.py
   ```

## Notes

- Make sure you have access to a CUDA-capable GPU for faster transcription.
- Update the Ollama server address in `Ollama_Connection.py` as needed.
- The project is modular; you can run each script independently.

---
