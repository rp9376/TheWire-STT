#!/usr/bin/env python3

import time
import os
import AudioDownloader_TheWire
import Speach2Text_Turbo

interval_minutes = 0.2  # Adjust this value to change the time interval
print(f"Starting... Will do something every {interval_minutes} minutes")

ctr = 0
start_time = time.time()
while True:
    print("Starting cycle: ", ctr)
    print("Running for time: ", round(time.time() - start_time, 2), "seconds")
    cycle_start_time = time.time()


    pass  # Insert your code here
    AudioDownloader_TheWire.check_n_download()
    file_name = Speach2Text_Turbo.CheckForFiles()
    if 1 or Speach2Text_Turbo.Transcribe(file_name):
        print("Transcription successful")
        print("Deleting the audio file...")
        os.remove(file_name)
    


    print("Cycle completed in: ", round(time.time() - cycle_start_time, 2), "seconds")
    ctr += 1
    print("Waiting...\n")
    time.sleep(interval_minutes * 60)
