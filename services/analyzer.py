import pandas as pd
import numpy as np


def detect_date_columns(df):
    """
    Detect columns containing dates.
    """

    date_columns = []

    for column in df.columns:

        # Already datetime
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            date_columns.append(column)
            continue

        # Try converting object/string columns
        if pd.api.types.is_object_dtype(df[column]):

            non_null = df[column].dropna()

            if len(non_null) == 0:
                continue

            try:
                converted = pd.to_datetime(
                    non_null,
                    errors="coerce"
                )

                success_rate = converted.notna().mean()

                # If at least 80% values behave like dates
                if success_rate >= 0.8:

                    df[column] = pd.to_datetime(
                        df[column],
                        errors="coerce"
                    )

                    date_columns.append(column)

            except Exception:
                pass

    return date_columns


def detect_column_types(df):
    """
    Classify dataset columns.
    """

    date_columns = detect_date_columns(df)

    numeric_columns = []

    categorical_columns = []

    for column in df.columns:

        if column in date_columns:
            continue

        if pd.api.types.is_numeric_dtype(df[column]):
            numeric_columns.append(column)

        else:
            categorical_columns.append(column)

    return {
        "numeric": numeric_columns,
        "categorical": categorical_columns,
        "date": date_columns
    }


def format_number(value):
    """
    Human readable large numbers.
    """

    try:

        value = float(value)

        if abs(value) >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f}B"

        elif abs(value) >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"

        elif abs(value) >= 1_000:
            return f"{value / 1_000:.2f}K"

        elif value.is_integer():
            return f"{int(value):,}"

        else:
            return f"{value:,.2f}"

    except Exception:

        return str(value)


def generate_kpis(df, column_types):
    """
    Automatically create KPI cards.
    """

    kpis = []

    # KPI 1
    kpis.append({
        "title": "Total Records",
        "value": f"{len(df):,}",
        "icon": "bi-table"
    })

    # KPI 2
    kpis.append({
        "title": "Columns",
        "value": str(len(df.columns)),
        "icon": "bi-layout-three-columns"
    })

    # KPI 3
    missing_values = int(df.isnull().sum().sum())

    kpis.append({
        "title": "Missing Values",
        "value": f"{missing_values:,}",
        "icon": "bi-exclamation-triangle"
    })

    # KPI 4
    duplicates = int(df.duplicated().sum())

    kpis.append({
        "title": "Duplicate Rows",
        "value": f"{duplicates:,}",
        "icon": "bi-copy"
    })

    # Automatically create numeric KPI cards
    numeric_columns = column_types["numeric"]

    for column in numeric_columns[:4]:

        total = df[column].sum()

        kpis.append({
            "title": f"Total {column}",
            "value": format_number(total),
            "icon": "bi-graph-up-arrow"
        })

    return kpis


def generate_summary(df, column_types):
    """
    High level dataset summary.
    """

    total_cells = df.shape[0] * df.shape[1]

    missing_cells = df.isnull().sum().sum()

    if total_cells > 0:
        completeness = (
            (total_cells - missing_cells)
            / total_cells
        ) * 100
    else:
        completeness = 0

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "numeric_columns":
            len(column_types["numeric"]),

        "categorical_columns":
            len(column_types["categorical"]),

        "date_columns":
            len(column_types["date"]),

        "missing_values":
            int(missing_cells),

        "duplicates":
            int(df.duplicated().sum()),

        "completeness":
            round(completeness, 2)
    }


def get_column_information(df):
    """
    Information shown in Data Overview.
    """

    information = []

    for column in df.columns:

        information.append({

            "column": column,

            "dtype": str(df[column].dtype),

            "missing":
                int(df[column].isnull().sum()),

            "unique":
                int(df[column].nunique()),

            "missing_percentage":
                round(
                    df[column].isnull().mean() * 100,
                    2
                )
        })

    return information
