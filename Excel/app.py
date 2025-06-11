from flask import Flask
from excel_routes import register_excel_routes

app = Flask(__name__)

register_excel_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
