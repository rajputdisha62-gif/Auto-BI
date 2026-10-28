import pandas as pd
import os


ALLOWED_EXTENSIONS = {"xlsx", "xls"}


def allowed_file(filename):
    """
    Check whether uploaded file is Excel.
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_sheet_names(file_path):
    """
    Return all worksheet names.
    """
    excel_file = pd.ExcelFile(file_path)

    return excel_file.sheet_names


def load_excel(file_path, sheet_name=0):
    """
    Load particular Excel worksheet.
    """

    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name
    )

    # Remove fully empty rows
    df = df.dropna(how="all")

    # Remove fully empty columns
    df = df.dropna(axis=1, how="all")

    # Remove leading/trailing spaces from column names
    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return df