from ytmusicapi import YTMusic
import yt_dlp
from pathlib import Path
import json


ytmusic = YTMusic()

def get_track_info(query: str):
    if not query:
        return None
    
    results = ytmusic.search(query, filter="songs", limit=1)

    if not results:
        return None
        
    track = results[0]

    title = track.get("title", "Unknown")
    artists = ", ".join(a.get("name", "Unknown") for a in track.get("artists", []))
    album = track.get("album", {}).get("name", "Unknown")
    duration = track.get("duration", "Unknown")
    video_id = track.get("videoId")

    thumbnails = track.get("thumbnails", [])
    cover_url = thumbnails[-1]["url"] if thumbnails else None



    return {
        "title": title,
        "artists": artists,
        "album": album,
        "duration": duration,
        "cover_url": cover_url,
        "video_id": video_id
    }



def download_audio(video_id: str, output_dir: str = "./downloads"):
    file = Path(f"{output_dir}/{video_id}.mp3")
    if file.is_file():
        return f"{output_dir}/{video_id}.mp3"

    url = f"https://music.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{                 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/{video_id}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print(f"✅ Сохранено в {output_dir}/{video_id}.mp3")
        with open("tracks.json", "w+") as f:
            json.dump({"video_id": video_id}, f, indent=4)
        return f"{output_dir}/{video_id}.mp3"
