from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)

import os
import uuid
import pandas as pd

from werkzeug.utils import secure_filename

from services.excel_service import (
    allowed_file,
    get_sheet_names,
    load_excel
)

from services.analyzer import (
    detect_column_types,
    generate_kpis,
    generate_summary,
    get_column_information
)

from services.chart_service import (
 
    create_charts
)


app = Flask(__name__)



# CONFIGURATION


UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = (
    25 * 1024 * 1024
)


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# In-memory uploaded file registry
uploaded_files = {}


# HOME PAGE


@app.route("/")
def index():

    return render_template(
        "index.html"
    )



# FILE UPLOAD


@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    if "file" not in request.files:

        return jsonify({
            "error": "No file uploaded."
        }), 400


    file = request.files["file"]


    if file.filename == "":

        return jsonify({
            "error": "Please select a file."
        }), 400


    if not allowed_file(file.filename):

        return jsonify({
            "error":
                "Only .xlsx and .xls files are supported."
        }), 400


    file_id = str(uuid.uuid4())

    filename = secure_filename(
        file.filename
    )

    stored_filename = (
        f"{file_id}_{filename}"
    )

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        stored_filename
    )


    file.save(file_path)


    try:

        sheet_names = get_sheet_names(
            file_path
        )

    except Exception as error:

        os.remove(file_path)

        return jsonify({
            "error":
                f"Unable to read Excel file: {str(error)}"
        }), 400


    uploaded_files[file_id] = {

        "path": file_path,

        "original_name": filename,

        "sheets": sheet_names
    }


    first_sheet = sheet_names[0]


    return redirect(
        url_for(
            "dashboard",
            file_id=file_id,
            sheet=first_sheet
        )
    )


# DASHBOARD


@app.route(
    "/dashboard/<file_id>"
)
def dashboard(file_id):

    if file_id not in uploaded_files:

        return redirect(
            url_for("index")
        )


    file_info = uploaded_files[file_id]


    selected_sheet = request.args.get(
        "sheet",
        file_info["sheets"][0]
    )


    if selected_sheet not in file_info["sheets"]:

        selected_sheet = (
            file_info["sheets"][0]
        )


    try:

        df = load_excel(
            file_info["path"],
            selected_sheet
        )

    except Exception as error:

        return f"""
        Error reading worksheet:
        {str(error)}
        """


    column_types = (
        detect_column_types(df)
    )


    kpis = generate_kpis(
        df,
        column_types
    )


    summary = generate_summary(
        df,
        column_types
    )


    charts = create_charts(
        df,
        column_types
    )


    column_info = (
        get_column_information(df)
    )


# FILTER VALUES


    filters = {}

    for column in (
        column_types["categorical"][:6]
    ):

        unique_values = (
            df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        # Prevent huge filters
        if len(unique_values) <= 100:

            filters[column] = sorted(
                unique_values
            )



    # DATA PREVIEW


    preview_df = df.head(100).copy()


    for column in preview_df.columns:

        if pd.api.types.is_datetime64_any_dtype(
            preview_df[column]
        ):

            preview_df[column] = (
                preview_df[column]
                .dt.strftime(
                    "%Y-%m-%d"
                )
            )


    preview_data = (
        preview_df
        .fillna("")
        .to_dict(
            orient="records"
        )
    )


    return render_template(

        "dashboard.html",

        file_id=file_id,

        filename=(
            file_info["original_name"]
        ),

        sheets=file_info["sheets"],

        selected_sheet=selected_sheet,

        kpis=kpis,

        charts=charts,

        summary=summary,

        filters=filters,

        columns=list(df.columns),

        column_info=column_info,

        preview_data=preview_data
    )



# DYNAMIC FILTER API


@app.route(
    "/api/filter/<file_id>",
    methods=["POST"]
)
def filter_dashboard(file_id):

    if file_id not in uploaded_files:

        return jsonify({
            "error": "File not found."
        }), 404


    payload = (
        request.get_json()
        or {}
    )


    sheet = payload.get(
        "sheet",
        uploaded_files[file_id]["sheets"][0]
    )


    selected_filters = (
        payload.get(
            "filters",
            {}
        )
    )


    df = load_excel(
        uploaded_files[file_id]["path"],
        sheet
    )


    # APPLY FILTERS
  

    for column, selected_values in (
        selected_filters.items()
    ):

        if (
            column in df.columns
            and selected_values
        ):

            df = df[
                df[column]
                .astype(str)
                .isin(selected_values)
            ]


    column_types = (
        detect_column_types(df)
    )


    kpis = generate_kpis(
        df,
        column_types
    )


    charts = create_charts(
        df,
        column_types
    )


    summary = generate_summary(
        df,
        column_types
    )


    return jsonify({

        "kpis": kpis,

        "charts": charts,

        "summary": summary
    })



# RUN APPLICATION


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
