#!/usr/bin/env python3

import logging
from pytubefix import Channel
import os
from itertools import islice
import re
import argparse

clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def sanitize_filename(filename):
    """Sanitize the filename to remove/replace invalid characters."""
    return re.sub(r'[\\/:*?"<>|]', '_', filename)


def check_n_download(channel_url="https://www.youtube.com/@S2Underground", max_videos=10, audio_dir=None, video_list_path=None):
    """
    Download new audio files from a YouTube channel and update the video list.
    Args:
        channel_url (str): The YouTube channel URL.
        max_videos (int): Max number of videos to check.
        audio_dir (str): Directory to save audio files.
        video_list_path (str): Path to the video list file.
    Returns:
        dict: Summary of downloads and errors.
    """
    if audio_dir is None:
        audio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'audio'))
    if video_list_path is None:
        video_list_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'video_list.txt'))
    os.makedirs(audio_dir, exist_ok=True)
    summary = {"downloaded": [], "skipped": [], "errors": []}
    try:
        channel = Channel(channel_url)
        logging.info(f"Channel URL: {channel.channel_url}")
        logging.info(f"Channel name: {channel.channel_name}")

        # Read the list of previously downloaded videos
        try:
            with open(video_list_path, "r") as file:
                video_list = set(line.strip() for line in file)
        except FileNotFoundError:
            video_list = set()

        for ctr, video in enumerate(islice(channel.videos, max_videos)):
            if "The Wire" in video.title:
                safe_title = sanitize_filename(video.title)
                if video.title not in video_list:
                    output_filename = safe_title + ".mp3"
                    output_filepath = os.path.join(audio_dir, output_filename)
                    if os.path.exists(output_filepath):
                        logging.info(f"{ctr+1}.) File already exists on disk: {output_filepath}")
                        summary["skipped"].append(video.title)
                        continue
                    stream = video.streams.filter(abr="128kbps", only_audio=True).first()
                    if stream and getattr(stream, "audio_codec", None) == "mp4a.40.2":
                        logging.info(f"{ctr+1}.) Downloading {video.title}...")
                        try:
                            stream.download(output_path=audio_dir, filename=output_filename)
                            summary["downloaded"].append(video.title)
                        except Exception as download_err:
                            logging.error(f"Download failed for {video.title}: {download_err}")
                            summary["errors"].append(video.title)
                    else:
                        logging.warning(f"{ctr+1}.) No suitable audio stream found for {video.title}.")
                        summary["errors"].append(video.title)
                else:
                    logging.info(f"{ctr+1}.) Video already in video_list.txt: {video.title}")
                    summary["skipped"].append(video.title)
            else:
                logging.info(f"{ctr+1}.) Video does not match 'The Wire': {video.title}")

        # Append the new videos to the list
        if summary["downloaded"]:
            with open(video_list_path, "a") as file:
                for video in summary["downloaded"]:
                    file.write(video + "\n")
            logging.info(f"New videos downloaded: {summary['downloaded']}")
        else:
            logging.info("No new videos to add to video_list.txt.")
        
        return summary
    except Exception as e:
        logging.error(f"Error in check_n_download: {e}")
        summary["errors"].append(str(e))
    return summary


def main():
    parser = argparse.ArgumentParser(description="Download audio from a YouTube channel.")
    parser.add_argument('--channel_url', type=str, default="https://www.youtube.com/@S2Underground", help='YouTube channel URL')
    parser.add_argument('--max_videos', type=int, default=10, help='Max number of videos to check')
    parser.add_argument('--audio_dir', type=str, default=None, help='Directory to save audio files')
    parser.add_argument('--video_list_path', type=str, default=None, help='Path to video list file')
    args = parser.parse_args()

    clear_screen()
    logging.info("Starting the audio downloader for 'The Wire' channel...\n")
    summary = check_n_download(
        channel_url=args.channel_url,
        max_videos=args.max_videos,
        audio_dir=args.audio_dir,
        video_list_path=args.video_list_path
    )
    logging.info(f"Summary: {summary}")


if __name__ == "__main__":
    main()
