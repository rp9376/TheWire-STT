#!/usr/bin/env python3

import time
import os
import logging
import json
from scripts import AudioDownloader_TheWire
from scripts import Speach2Text_Turbo
from ollama_utils.run_llm_on_transcript import run_llm_on_transcript, get_transcript_file
import requests



def main():
    interval_minutes = 1.0  # Adjust this value to change the time interval
    ENABLE_TRANSCRIPTION = True  # Set to False to skip transcription for debugging
    RUN_ONCE = False  # Set to True to run only one cycle and exit
    USE_MOCK_JSON = False  # Set to True to use mock_json.txt even if no transcription
    NUMBER_OF_VIDEOS = 2  # Number of videos to download
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    logging.info(f"Starting... The cycle will run every {interval_minutes} minutes.")

    ctr = 0
    start_time = time.time()
    try:
        while True:
            logging.info(f"Starting cycle: #{ctr}")
            logging.info(f"Running for time: {round(time.time() - start_time, 2)} seconds")
            cycle_start_time = time.time()

            try:
                AudioDownloader_TheWire.check_n_download(max_videos=NUMBER_OF_VIDEOS)
                # Batch process all audio files for transcription
                while True:
                    file_name = Speach2Text_Turbo.CheckForFiles()
                    if not file_name:
                        logging.info("No audio files found for transcription.")
                        break
                    logging.info(f"File to transcribe next: {file_name}")
                    if ENABLE_TRANSCRIPTION:
                        try:
                            if Speach2Text_Turbo.Transcribe(file_name):
                                logging.info(f"Transcription successful for {file_name}")
                                os.remove(file_name)
                                logging.info(f"Deleted audio file: {file_name}")
                            else:
                                logging.warning(f"Transcription failed or returned False for {file_name}.")
                        except Exception as e:
                            logging.error(f"Error during transcription of {file_name}: {e}")
                    else:
                        logging.info("Transcription step is disabled (debug mode).")
                        break

                # Batch process all transcripts for LLM/Mock
                while True:
                    llm_response = None
                    if not is_api_available():
                        logging.error("API/database is not available. Skipping LLM processing and upload.")
                        break
                    if USE_MOCK_JSON:
                        logging.info("USE_MOCK_JSON is enabled. Loading mock JSON for testing.")
                        mock_json_path = os.path.join(os.path.dirname(__file__), 'mock_json.txt')
                        if os.path.exists(mock_json_path):
                            with open(mock_json_path, 'r', encoding='utf-8') as f:
                                llm_response = json.load(f)
                            logging.info("Mock JSON loaded successfully.")
                            send_success = send_llm_json_to_api(llm_response)
                            if not send_success:
                                logging.error("Failed to upload mock JSON to API. Will retry next cycle.")
                        else:
                            logging.error(f"Mock JSON file not found: {mock_json_path}")
                        break  # Only send once per cycle in mock mode
                    else:
                        try:
                            transcript_path = get_transcript_file()
                            if not transcript_path:
                                logging.info("No transcript file found to run LLM on.")
                                break
                            logging.info(f"Running LLM on transcript: {transcript_path}")
                            llm_response = run_llm_on_transcript(transcript_path=transcript_path)
                            logging.info("LLM response received.")
                            send_success = send_llm_json_to_api(llm_response)
                            if send_success:
                                try:
                                    os.remove(transcript_path)
                                    logging.info(f"Deleted transcript file: {transcript_path}")
                                except FileNotFoundError:
                                    logging.warning(f"Transcript file not found for deletion: {transcript_path}")
                            else:
                                logging.error(f"Failed to upload LLM JSON to API. Transcript will not be deleted and will be retried next cycle: {transcript_path}")
                        except Exception as e:
                            logging.error(f"Error running LLM on transcript: {e}")
                            break
                
            except Exception as e:
                logging.error(f"Error in cycle: {e}")

            logging.info(f"Cycle completed in: {round(time.time() - cycle_start_time, 2)} seconds")

            if RUN_ONCE:
                logging.info("RUN_ONCE is set to True. Exiting after one cycle.")
                break
                
            ctr += 1
            logging.info("Waiting...\n")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        logging.info("Process interrupted by user. Exiting...")


def send_llm_json_to_api(llm_response):
    """Send the LLM JSON to the API/database."""
    if isinstance(llm_response, str):
        try:
            llm_response = json.loads(llm_response)
        except Exception as parse_exc:
            logging.error(f"Failed to parse LLM response as JSON: {parse_exc}")
            return False
    if not llm_response:
        logging.error("No LLM response to send to API.")
        return False
    try:
        api_url = "http://localhost:5000/api/stories"
        resp = requests.post(api_url, json=llm_response)
        if resp.status_code == 201:
            logging.info("LLM JSON successfully sent to API/database.")
            return True
        else:
            logging.error(f"Failed to send LLM JSON to API: {resp.status_code} {resp.text}")
            return False
    except Exception as api_exc:
        logging.error(f"Exception sending LLM JSON to API: {api_exc}")
        return False

def is_api_available(api_url="http://localhost:5000/api/stories"):
    try:
        resp = requests.get(api_url.replace('/stories', '/dump_stories'), timeout=3)
        return resp.status_code == 200
    except Exception as e:
        logging.error(f"API/database not available: {e}")
        return False

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
