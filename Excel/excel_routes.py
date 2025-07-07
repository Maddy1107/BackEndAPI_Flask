# routes.py

import os
import json
from flask import request, jsonify, send_file
from excel_functions import extract_product_quantity, update_excel_file

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def register_excel_routes(app):
    @app.route("/upload", methods=["POST"])
    def upload_file():
        file = request.files.get("file")
        if not file or file.filename == "":
            return jsonify({"error": "No file provided"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        data_dict, error = extract_product_quantity(file_path)
        if error:
            return jsonify({"error": "Failed to process file", "message": error}), 500

        try:
            return jsonify({"data": data_dict})
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    @app.route("/export/<name>", methods=["POST"])
    def export_file(name):
        file = request.files.get("file")
        filename = request.form.get("filename")
        json_data = request.form.get("data")

        if not file or file.filename == "":
            return jsonify({"error": "No Excel file provided"}), 400
        if not filename:
            return jsonify({"error": "No filename provided"}), 400
        if not json_data:
            return jsonify({"error": "No JSON data provided"}), 400

        try:
            update_dict = json.loads(json_data)
        except Exception as e:
            return jsonify({"error": "Invalid JSON format", "message": str(e)}), 400

        output_stream, error = update_excel_file(file, update_dict, name)
        if error:
            return (
                jsonify({"error": "Failed to update Excel file", "message": error}),
                500,
            )

        return send_file(
            output_stream,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename,
        )

    @app.route("/export-sheet/<name>", methods=["POST"])
    def export_specific_sheet(name):
        file = request.files.get("file")
        filename = request.form.get("filename")
        json_data = request.form.get("data")
        sheet_name = request.form.get("sheet")  # <- New param from Unity

        if not file or file.filename == "":
            return jsonify({"error": "No Excel file provided"}), 400
        if not filename:
            return jsonify({"error": "No filename provided"}), 400
        if not json_data:
            return jsonify({"error": "No JSON data provided"}), 400
        if not sheet_name:
            return jsonify({"error": "No sheet name provided"}), 400

        try:
            update_dict = json.loads(json_data)
        except Exception as e:
            return jsonify({"error": "Invalid JSON format", "message": str(e)}), 400

        output_stream, error = update_excel_file(file, update_dict, name, sheet_name)
        if error:
            return (
                jsonify({"error": "Failed to update Excel file", "message": error}),
                500,
            )

        return send_file(
            output_stream,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename,
        )
