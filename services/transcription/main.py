#!/usr/bin/env python3

import time
import os
import logging
from scripts import AudioDownloader_TheWire
from scripts import Speach2Text_Turbo

def main():
    interval_minutes = 5.0  # Adjust this value to change the time interval
    ENABLE_TRANSCRIPTION = True  # Set to False to skip transcription for debugging
    RUN_ONCE = True  # Set to True to run only one cycle and exit
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
                AudioDownloader_TheWire.check_n_download()
                file_name = Speach2Text_Turbo.CheckForFiles()
                logging.info(f"File to transcribe next: {file_name}")
                if file_name:
                    if ENABLE_TRANSCRIPTION:
                        try:
                            if Speach2Text_Turbo.Transcribe(file_name):
                                logging.info("Transcription successful")
                                logging.info("Deleting the audio file...")
                                os.remove(file_name)
                            else:
                                logging.warning("Transcription failed or returned False.")
                        except Exception as e:
                            logging.error(f"Error during transcription: {e}")
                    else:
                        logging.info("Transcription step is disabled (debug mode).")
                else:
                    logging.info("No audio files found for transcription.")


                # TODO 
                """ Use Ollama model to parse the transcription and generate a response to put into database"""



            except Exception as e:
                logging.error(f"Error in cycle: {e}")

            logging.info(f"Cycle completed in: {round(time.time() - cycle_start_time, 2)} seconds")
            ctr += 1
            logging.info("Waiting...\n")
            if RUN_ONCE:
                break
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        logging.info("Process interrupted by user. Exiting...")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
