import yt_dlp
import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import sys

base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

output_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'getspotify')
os.makedirs(output_dir, exist_ok=True)

need_check = True

def set_metadata(file_path, album, artists):
    thumbnail_path = os.path.join(base_dir, "tmp", "thumbnail.jpg")
    try:
        audio = MP3(file_path, ID3=EasyID3)
        audio['album'] = album
        audio['artist'] = artists
        audio.save()
        audio = MP3(file_path, ID3=ID3)
        with open(thumbnail_path, 'rb') as albumart:
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=u'Cover',
                data=albumart.read()
            )
        audio.save()
    except Exception as e:
        print(f"An error occurred: {e}")

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} - {d['_speed_str']} ETA: {d['_eta_str']}", end='\r')
    elif d['status'] == 'finished':
        print("\nDownload completed")

def download_audio_as_mp3(url, folder, name, ffmpeg_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, folder, f'{name}.%(ext)s'),
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
        'postprocessor_args': [
            '-vn',
        ],
        'ffmpeg_location': ffmpeg_path,
        'keepvideo': False,
        'quiet': True,
        'progress_hooks': [progress_hook],
        'concurrent_fragments': 1
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download(url, folder, name, artists, album, ffmpeg_path):
    try:
        download_audio_as_mp3(url, folder, name, ffmpeg_path)
        path = os.path.join(output_dir, folder, f"{name}.mp3")
        set_metadata(path, album, artists)
    except Exception as e:
        print("An error occurred while downloading the video. Please try again later. Error:", e)