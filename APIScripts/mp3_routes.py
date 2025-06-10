import uuid
import os
from flask import request, jsonify, send_from_directory
from yt_dlp import YoutubeDL

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def register_mp3_routes(app):
    @app.route('/link-to-mp3', methods=['POST'])
    def link_to_mp3():
        data = request.get_json()
        if not data or 'links' not in data:
            return jsonify({'error': 'No links provided'}), 400

        links = data['links']
        if not isinstance(links, list):
            return jsonify({'error': 'Links should be a list'}), 400

        results = []
        any_link_failed = False

        for link in links:
            try:
                # Generate a unique ID for the file to prevent collision
                filename_base = str(uuid.uuid4())

                # Configure yt-dlp to download the MP3 file
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'ffmpeg_location': r'C:/ffmpeg/ffmpeg-master-latest-win64-gpl-shared/bin',  # Specify the path to ffmpeg
                    'quiet': True,
                    'extractaudio': True,
                    'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{filename_base}.mp3'),  # Save to the download folder
                    'noplaylist': True,  # Avoid playlist download
                }

                # Using yt-dlp to download the audio as MP3
                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(link, download=True)  # Download the file
                    title = info_dict.get('title', 'Unknown Title')

                # Create a download link
                download_url = f"{request.host_url}downloads/{filename_base}.mp3"
                
                results.append({
                    'title': title,
                    'download_url': download_url,
                    'message': 'Download link generated'
                })

            except Exception as e:
                any_link_failed = True
                results.append({
                    'original_link': link,
                    'error': str(e)
                })

        # Return the results with either success or failure status
        if any_link_failed:
            return jsonify({'results': results}), 400
        else:
            return jsonify({'results': results}), 200
        
    @app.route('/downloads/<filename>', methods=['GET'])
    def download_file(filename):
        try:
            # Send the file to the user
            file_path = os.path.join(DOWNLOAD_FOLDER, filename)

            # Ensure the file exists
            if not os.path.isfile(file_path):
                return jsonify({'error': 'File not found'}), 404

            # Send file for download
            response = send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

            # After sending the file, delete it from the server
            os.remove(file_path)  # Delete the file after it's downloaded
            print(f"File {filename} deleted after download.")

            return response
        except Exception as e:
            return jsonify({'error': f'Failed to download or delete the file: {str(e)}'}), 500