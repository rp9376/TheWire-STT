import os
import logging
from ollama import Client

MODEL = 'llama3.3:70b'
OLLAMA_HOST = 'http://10.45.10.10:11434'
TRANSCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'transcripts'))
PROMPT_DIR = os.path.dirname(__file__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def create_client():
    """Create and return an Ollama client."""
    logger.debug(f"Connecting to Ollama host at {OLLAMA_HOST}")
    return Client(host=OLLAMA_HOST)

def get_latest_prompt(prompt_dir=None):
    """Return the contents of the latest prompt file containing 'latest' in its name."""
    if prompt_dir is None:
        prompt_dir = PROMPT_DIR
    # Match any file with 'latest' in the name and ending with .txt
    prompts = [f for f in os.listdir(prompt_dir) if 'latest' in f and f.endswith('.txt') and os.path.isfile(os.path.join(prompt_dir, f))]
    if not prompts:
        logger.error('No prompt file with "latest" in the name found in ollama folder.')
        raise FileNotFoundError('No prompt file with "latest" in the name found in ollama folder.')
    prompts.sort(key=lambda f: os.path.getmtime(os.path.join(prompt_dir, f)), reverse=True)
    prompt_path = os.path.join(prompt_dir, prompts[0])
    logger.info(f"Using prompt file: {prompt_path}")
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_transcript_file():
    """Return the path to the latest transcript file in the transcripts directory."""
    txt_files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith('.txt')]
    if not txt_files:
        logger.error('No transcript files found in transcripts folder.')
        raise FileNotFoundError('No transcript files found in transcripts folder.')
    # Pick the first transcript (could be improved to pick by date, etc.)
    txt_files.sort(key=lambda f: os.path.getmtime(os.path.join(TRANSCRIPTS_DIR, f)), reverse=True)
    transcript_path = os.path.join(TRANSCRIPTS_DIR, txt_files[0])
    logger.info(f"Using transcript file: {transcript_path}")
    return transcript_path

def combine_prompt_and_transcript(prompt, transcript):
    """Combine prompt and transcript as if appending two files."""
    return f"{prompt}\n{transcript}"

def run_llm_on_transcript():
    """Run the LLM on the latest prompt and transcript, return the LLM's response."""
    client = create_client()
    transcript_path = get_transcript_file()
    prompt_text = get_latest_prompt()
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read()
    combined = combine_prompt_and_transcript(prompt_text, transcript)
    logger.info("Sending combined prompt and transcript to LLM...")
    try:
        response = client.chat(MODEL, messages=[{'role': 'user', 'content': combined}])
        logger.info("Received response from LLM.")
        return response['message']['content']
    except Exception as e:
        logger.error(f"Error communicating with LLM: {e}")
        raise

def main():
    logger.info("Starting LLM transcript processing...")
    try:
        result = run_llm_on_transcript()
        logger.info("LLM processing complete. Output below:")
        print("\nLLM Response:\n", result)
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
