import os
import subprocess
import traceback
import uuid
from flask import request, send_file, jsonify
from pytube import YouTube
import yt_dlp

DOWNLOAD_DIR = "/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
FFMPEG_PATH = r'C:/ffmpeg/bin'


def register_mp3_routes(app):
    @app.route("/convert", methods=["POST"])
    def convert():
        try:
            data = request.get_json(force=True)
            url = data.get("url")
            if not url:
                return jsonify({"error": "URL is required"}), 400

            unique_id = str(uuid.uuid4())
            base_path = os.path.join(DOWNLOAD_DIR, unique_id)
            mp3_path = f"{base_path}.mp3"

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{base_path}.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': FFMPEG_PATH,
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if not os.path.exists(mp3_path):
                return jsonify({"error": "Download failed or file not created."}), 500

            return send_file(mp3_path, as_attachment=True)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
   
    @app.route("/title", methods=["POST"])
    def get_title():
        try:
            data = request.get_json(force=True)
            url = data.get("url")
            if not url:
                return jsonify({"error": "URL is required"}), 400

            ydl_opts = {
                'quiet': True,
                'skip_download': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "Unknown Title")
                return title  # Return plain string, not JSON

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

