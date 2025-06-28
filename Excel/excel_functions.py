# excel_functions.py
import datetime
from io import BytesIO
from openpyxl import load_workbook
import pandas as pd


def extract_product_quantity(file_path):
    try:
        df = pd.read_excel(file_path, header=None, skiprows=4)
        if len(df.columns) < 4:
            return {}, "Excel file does not have enough columns"
        product_col, quantity_col = df.columns[2], df.columns[3]

        df[quantity_col] = df[quantity_col].fillna("")

        filtered_df = df[[product_col, quantity_col]]
        data_dict = {
            str(row[product_col]): row[quantity_col]
            for _, row in filtered_df.iterrows()
            if pd.notnull(row[product_col]) and str(row[product_col]).strip() != ""
        }
        return data_dict, None
    except Exception as e:
        return {}, str(e)


def update_excel_file(file, update_dict):
    try:
        wb = load_workbook(file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=5):
            product_cell = row[2]  # Column C
            quantity_cell = row[3]  # Column D
            product_name = str(product_cell.value).strip() if product_cell.value else ""
            if product_name in update_dict:
                quantity_cell.value = update_dict[product_name]

        sheet["E3"] = datetime.datetime.now().strftime("%d-%m-%Y")
        sheet["E1"] = "Priyanka Roy"

        output_stream = BytesIO()
        wb.save(output_stream)
        output_stream.seek(0)

        return output_stream, None
    except Exception as e:
        return None, str(e)
