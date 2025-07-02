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


def update_excel_file(file, update_dict, sheet_name=None):
    try:
        wb = load_workbook(file)
        sheet = wb[sheet_name] if sheet_name else wb.active

        month_col_index = get_month_column(sheet)

        for row in sheet.iter_rows(min_row=5):
            product_cell = row[2]
            target_cell = row[3] if month_col_index == -1 else row[month_col_index]
            remarks_cell = row[4] if month_col_index == -1 else row[month_col_index + 1]

            product_name = str(product_cell.value).strip() if product_cell.value else ""
            if product_name in update_dict:
                target_cell.value[0] = update_dict[product_name]
                remarks_cell.value[1] = update_dict[product_name]

        update_named_cells()

        output_stream = BytesIO()
        wb.save(output_stream)
        output_stream.seek(0)

        return output_stream, None
    except Exception as e:
        return None, str(e)


def get_month_column(sheet):
    current_month = datetime.datetime.now().strftime("%B").lower()  # "june"
    header_row = sheet[4]

    for col_index, cell in enumerate(header_row):
        cell_value = str(cell.value).strip().lower() if cell.value else ""
        if current_month in cell_value:
            return col_index  # 0-based index

    return -1  # Not found


def update_named_cells(sheet):
    for row in sheet.iter_rows():
        for i, cell in enumerate(row):
            if not cell.value:
                continue

            cell_value = str(cell.value).strip().lower()

            # Match "Name"
            if "name" in cell_value:
                row[i + 1].value = "Priyanka Roy"

            # Match "Handover Date:"
            elif "handover" in cell_value:
                row[i + 1].value = datetime.datetime.now().strftime("%d-%m-%Y")
