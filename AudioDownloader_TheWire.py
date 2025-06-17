#!/usr/bin/env python3

import logging
from pytubefix import Channel
import os
from itertools import islice

clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def check_n_download(channel_url="https://www.youtube.com/@S2Underground", max_videos=10):
    try:
        channel = Channel(channel_url)
        logging.info(f"Channel URL: {channel.channel_url}")
        logging.info(f"Channel name: {channel.channel_name}")

        # Read the list of previously downloaded videos
        try:
            with open("video_list.txt", "r") as file:
                video_list = set(line.strip() for line in file)
        except FileNotFoundError:
            video_list = set()

        new_video_list = []

        for ctr, video in enumerate(islice(channel.videos, max_videos)):
            if "The Wire" in video.title:
                if video.title not in video_list:
                    output_filename = video.title + ".mp3"
                    if os.path.exists(output_filename):
                        logging.info(f"{ctr+1}.) File already exists on disk: {output_filename}")
                        continue
                    stream = video.streams.filter(abr="128kbps", only_audio=True).first()
                    if stream and getattr(stream, "audio_codec", None) == "mp4a.40.2":
                        logging.info(f"{ctr+1}.) Downloading {video.title}...")
                        stream.download(filename=output_filename)
                        new_video_list.append(video.title)
                    else:
                        logging.warning(f"{ctr+1}.) No suitable audio stream found for {video.title}.")
                else:
                    logging.info(f"{ctr+1}.) Video already in video_list.txt: {video.title}")
            else:
                logging.info(f"{ctr+1}.) Video does not match 'The Wire': {video.title}")

        # Append the new videos to the list
        if new_video_list:
            with open("video_list.txt", "a") as file:
                for video in new_video_list:
                    file.write(video + "\n")
            logging.info(f"New videos downloaded: {new_video_list}")
        else:
            logging.info("No new videos to add to video_list.txt.")
        
        return new_video_list
    except Exception as e:
        logging.error(f"Error in check_n_download: {e}")
    return []


if __name__ == "__main__":
    clear_screen()
    logging.info("Starting the audio downloader for 'The Wire' channel...\n")

    check_n_download()
