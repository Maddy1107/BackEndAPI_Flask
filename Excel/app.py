from flask import Flask
from database import init_db
from db_routes import register_product_routes
from excel_routes import register_excel_routes

app = Flask(__name__)
init_db(app)

register_excel_routes(app)
register_product_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
