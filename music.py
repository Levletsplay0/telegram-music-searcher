from ytmusicapi import YTMusic
import yt_dlp
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

ytmusic = YTMusic()
logging.info("YTMusic API и yt_dlp успешно инициализированы")

def get_track_info(query: str):
    if not query:
        logging.warning("Пустой запрос для поиска трека")
        return None
    
    try:
        results = ytmusic.search(query, filter="songs", limit=1)

        if not results:
            logging.warning("Трек не найден")
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
    except Exception as e:
        logging.error(f"Error fetching track info: {e}")
        return None



def download_audio(video_id: str, output_dir: str = "./downloads"):
    file = Path(f"{output_dir}/{video_id}.mp3")
    if file.is_file():
        logging.info(f"Файл уже существует: {file}")
        return f"{output_dir}/{video_id}.mp3"

    url = f"https://music.youtube.com/watch?v={video_id}"
    try:
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
            logging.info(f"✅ Сохранено в {output_dir}/{video_id}.mp3")
            
            return f"{output_dir}/{video_id}.mp3"
    except Exception as e:
        logging.error(f"Error downloading audio: {e}")
        return None