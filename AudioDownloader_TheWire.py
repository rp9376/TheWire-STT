#!/usr/bin/env python3

from pytubefix import Channel


def check_n_download():
    """
    Downloads new videos from the specified YouTube channel if they match
    a specific title condition and are not already downloaded.
    """
    channel_url = "https://www.youtube.com/@S2Underground"
    channel = Channel(channel_url)

    print(f"Channel URL: {channel.channel_url}")
    print(f"Channel name: {channel.channel_name}")

    print("Tests:")

    # Read the list of previously downloaded videos
    with open("video_list.txt", "r") as file:
        video_list = [line.strip() for line in file.readlines()]

    new_video_list = []
    counter = 0

    for video in channel.videos:
        if counter > 10:
            break

        if "The Wire" in video.title and video.title not in video_list:
            new_video_list.append(video.title)
            print("New video: ", video.title)
            print("Downloading...")

            # Attempt to find the desired audio stream
            audio_stream = None
            streams = str(video.streams).split(",")
            for stream in streams:
                if 'abr="128kbps"' in stream and 'acodec="mp4a.40.2"' in stream:
                    audio_stream = stream

            if audio_stream:
                print(f"Downloading {video.title}...")
                itag = audio_stream.split('itag="')[1].split('"')[0]
                stream = video.streams.get_by_itag(itag)
                stream.download(filename=video.title + ".mp3")
            else:
                print(f"No suitable audio stream found for {video.title}.")
        else:
            print("Video already exists: ", video.title)

        counter += 1

    print("New videos: ", new_video_list)

    # Append the new videos to the list
    with open("video_list.txt", "a") as file:
        for video in new_video_list:
            file.write(video + "\n")

    return None


if __name__ == "__main__":
    check_n_download()
