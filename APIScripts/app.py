from flask import Flask, send_from_directory
from excel_routes import register_excel_routes
from mp3_routes import register_mp3_routes

app = Flask(__name__)

register_excel_routes(app)
register_mp3_routes(app)

@app.route('/downloads/<path:filename>')
def serve_download(filename):
    return send_from_directory('downloads', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
