from flask import Flask
from mp3_routes import register_mp3_routes

app = Flask(__name__)

register_mp3_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
