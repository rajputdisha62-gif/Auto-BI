import pandas as pd
import plotly.express as px


def apply_theme(fig):
    """
    Apply common styling to Plotly figures.
    """

    fig.update_layout(
        template="plotly_white",

        margin=dict(
            l=40,
            r=20,
            t=60,
            b=40
        ),

        font=dict(
            family="Inter, Arial"
        ),

        paper_bgcolor="white",

        plot_bgcolor="white",

        hoverlabel=dict(
            font_size=13
        )
    )

    return fig


def create_charts(df, column_types):
    """
    Automatically generate charts based on
    detected column types.
    """

    charts = []

    numeric_columns = column_types.get(
        "numeric",
        []
    )

    categorical_columns = column_types.get(
        "categorical",
        []
    )

    date_columns = column_types.get(
        "date",
        []
    )

# for Category + Number = Barchart

    if (
        categorical_columns
        and numeric_columns
    ):

        category = categorical_columns[0]

        numeric = numeric_columns[0]


        try:

            grouped = (
                df.groupby(
                    category,
                    dropna=False
                )[numeric]
                .sum()
                .reset_index()
                .sort_values(
                    numeric,
                    ascending=False
                )
                .head(15)
            )


            grouped[category] = (
                grouped[category]
                .fillna("Unknown")
                .astype(str)
            )


            fig = px.bar(
                grouped,
                x=category,
                y=numeric,
                title=f"{numeric} by {category}"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    f"{numeric} by {category}",

                "figure":
                    fig.to_json(),

                "type":
                    "bar"

            })

        except Exception as error:

            print(
                "Bar chart error:",
                error
            )



# For CATEGORY -- DONUT CHART
    

    if categorical_columns:

        category = categorical_columns[0]


        try:

            category_data = (
                df[category]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .head(10)
                .reset_index()
            )


            category_data.columns = [
                category,
                "Count"
            ]


            fig = px.pie(
                category_data,
                names=category,
                values="Count",
                hole=0.55,
                title=f"{category} Distribution"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    f"{category} Distribution",

                "figure":
                    fig.to_json(),

                "type":
                    "donut"

            })

        except Exception as error:

            print(
                "Donut chart error:",
                error
            )


# For DATE + NUMERIC --- LINE CHART


    if (
        date_columns
        and numeric_columns
    ):

        date_column = date_columns[0]

        numeric = numeric_columns[0]


        try:

            temp_df = df[
                [date_column, numeric]
            ].dropna()


            if not temp_df.empty:

                temp_df = temp_df.copy()


                temp_df[date_column] = (
                    pd.to_datetime(
                        temp_df[date_column],
                        errors="coerce"
                    )
                )


                temp_df = temp_df.dropna(
                    subset=[date_column]
                )


                trend = (
                    temp_df
                    .set_index(date_column)
                    .resample("ME")[numeric]
                    .sum()
                    .reset_index()
                )


                if not trend.empty:

                    fig = px.line(
                        trend,
                        x=date_column,
                        y=numeric,
                        markers=True,
                        title=f"{numeric} Trend"
                    )


                    apply_theme(fig)


                    charts.append({

                        "title":
                            f"{numeric} Trend",

                        "figure":
                            fig.to_json(),

                        "type":
                            "line"

                    })

        except Exception as error:

            print(
                "Line chart error:",
                error
            )



# for NUMERIC --- HISTOGRAM


    if numeric_columns:

        numeric = numeric_columns[0]


        try:

            fig = px.histogram(
                df,
                x=numeric,
                nbins=30,
                title=f"{numeric} Distribution"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    f"{numeric} Distribution",

                "figure":
                    fig.to_json(),

                "type":
                    "histogram"

            })

        except Exception as error:

            print(
                "Histogram error:",
                error
            )


# TWO NUMERIC COLUMNS ---- SCATTER


    if len(numeric_columns) >= 2:

        x_column = numeric_columns[0]

        y_column = numeric_columns[1]


        try:

            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                title=f"{x_column} vs {y_column}"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    f"{x_column} vs {y_column}",

                "figure":
                    fig.to_json(),

                "type":
                    "scatter"

            })

        except Exception as error:

            print(
                "Scatter chart error:",
                error
            )



# SECOND CATEGORY + NUMERIC ---> AVERAGE BAR
    

    if (
        len(categorical_columns) >= 2
        and numeric_columns
    ):

        category = categorical_columns[1]

        numeric = numeric_columns[0]


        try:

            grouped = (
                df.groupby(
                    category,
                    dropna=False
                )[numeric]
                .mean()
                .reset_index()
                .sort_values(
                    numeric,
                    ascending=False
                )
                .head(15)
            )


            grouped[category] = (
                grouped[category]
                .fillna("Unknown")
                .astype(str)
            )


            fig = px.bar(
                grouped,
                x=category,
                y=numeric,
                title=f"Average {numeric} by {category}"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    f"Average {numeric} by {category}",

                "figure":
                    fig.to_json(),

                "type":
                    "bar"

            })

        except Exception as error:

            print(
                "Average bar chart error:",
                error
            )


  
# CORRELATION HEATMAP


    if len(numeric_columns) >= 2:

        try:

            correlation = (
                df[numeric_columns]
                .corr()
                .round(2)
            )


            fig = px.imshow(
                correlation,
                text_auto=True,
                aspect="auto",
                title="Correlation Matrix"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    "Correlation Matrix",

                "figure":
                    fig.to_json(),

                "type":
                    "heatmap"

            })

        except Exception as error:

            print(
                "Correlation chart error:",
                error
            )


# RETURN ALL GENERATED CHARTS

    return charts

import pandas as pd
import plotly.express as px


def apply_theme(fig):
    """
    Apply common styling to Plotly figures.
    """

    fig.update_layout(
        template="plotly_white",

        margin=dict(
            l=40,
            r=20,
            t=60,
            b=40
        ),

        font=dict(
            family="Inter, Arial"
        ),

        paper_bgcolor="white",

        plot_bgcolor="white",

        hoverlabel=dict(
            font_size=13
        )
    )

    return fig


def create_charts(df, column_types):
    """
    Automatically generate charts based on
    detected column types.
    """

    charts = []

    numeric_columns = column_types.get(
        "numeric",
        []
    )

    categorical_columns = column_types.get(
        "categorical",
        []
    )

    date_columns = column_types.get(
        "date",
        []
    )

# for Category + Number = Barchart

    if (
        categorical_columns
        and numeric_columns
    ):

        category = categorical_columns[0]

        numeric = numeric_columns[0]


        try:

            grouped = (
                df.groupby(
                    category,
                    dropna=False
                )[numeric]
                .sum()
                .reset_index()
                .sort_values(
                    numeric,
                    ascending=False
                )
                .head(15)
            )


            grouped[category] = (
                grouped[category]
                .fillna("Unknown")
                .astype(str)
            )


            fig = px.bar(
                grouped,
                x=category,
                y=numeric,
                title=f"{numeric} by {category}"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    f"{numeric} by {category}",

                "figure":
                    fig.to_json(),

                "type":
                    "bar"

            })

        except Exception as error:

            print(
                "Bar chart error:",
                error
            )



# For CATEGORY -- DONUT CHART
    

    if categorical_columns:

        category = categorical_columns[0]


        try:

            category_data = (
                df[category]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .head(10)
                .reset_index()
            )


            category_data.columns = [
                category,
                "Count"
            ]


            fig = px.pie(
                category_data,
                names=category,
                values="Count",
                hole=0.55,
                title=f"{category} Distribution"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    f"{category} Distribution",

                "figure":
                    fig.to_json(),

                "type":
                    "donut"

            })

        except Exception as error:

            print(
                "Donut chart error:",
                error
            )


# For DATE + NUMERIC --- LINE CHART


    if (
        date_columns
        and numeric_columns
    ):

        date_column = date_columns[0]

        numeric = numeric_columns[0]


        try:

            temp_df = df[
                [date_column, numeric]
            ].dropna()


            if not temp_df.empty:

                temp_df = temp_df.copy()


                temp_df[date_column] = (
                    pd.to_datetime(
                        temp_df[date_column],
                        errors="coerce"
                    )
                )


                temp_df = temp_df.dropna(
                    subset=[date_column]
                )


                trend = (
                    temp_df
                    .set_index(date_column)
                    .resample("ME")[numeric]
                    .sum()
                    .reset_index()
                )


                if not trend.empty:

                    fig = px.line(
                        trend,
                        x=date_column,
                        y=numeric,
                        markers=True,
                        title=f"{numeric} Trend"
                    )


                    apply_theme(fig)


                    charts.append({

                        "title":
                            f"{numeric} Trend",

                        "figure":
                            fig.to_json(),

                        "type":
                            "line"

                    })

        except Exception as error:

            print(
                "Line chart error:",
                error
            )



# for NUMERIC --- HISTOGRAM


    if numeric_columns:

        numeric = numeric_columns[0]


        try:

            fig = px.histogram(
                df,
                x=numeric,
                nbins=30,
                title=f"{numeric} Distribution"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    f"{numeric} Distribution",

                "figure":
                    fig.to_json(),

                "type":
                    "histogram"

            })

        except Exception as error:

            print(
                "Histogram error:",
                error
            )


# TWO NUMERIC COLUMNS ---- SCATTER


    if len(numeric_columns) >= 2:

        x_column = numeric_columns[0]

        y_column = numeric_columns[1]


        try:

            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                title=f"{x_column} vs {y_column}"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    f"{x_column} vs {y_column}",

                "figure":
                    fig.to_json(),

                "type":
                    "scatter"

            })

        except Exception as error:

            print(
                "Scatter chart error:",
                error
            )



# SECOND CATEGORY + NUMERIC ---> AVERAGE BAR
    

    if (
        len(categorical_columns) >= 2
        and numeric_columns
    ):

        category = categorical_columns[1]

        numeric = numeric_columns[0]


        try:

            grouped = (
                df.groupby(
                    category,
                    dropna=False
                )[numeric]
                .mean()
                .reset_index()
                .sort_values(
                    numeric,
                    ascending=False
                )
                .head(15)
            )


            grouped[category] = (
                grouped[category]
                .fillna("Unknown")
                .astype(str)
            )


            fig = px.bar(
                grouped,
                x=category,
                y=numeric,
                title=f"Average {numeric} by {category}"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    f"Average {numeric} by {category}",

                "figure":
                    fig.to_json(),

                "type":
                    "bar"

            })

        except Exception as error:

            print(
                "Average bar chart error:",
                error
            )


  
# CORRELATION HEATMAP


    if len(numeric_columns) >= 2:

        try:

            correlation = (
                df[numeric_columns]
                .corr()
                .round(2)
            )


            fig = px.imshow(
                correlation,
                text_auto=True,
                aspect="auto",
                title="Correlation Matrix"
            )


            apply_theme(fig)


            charts.append({

                "title":
                    "Correlation Matrix",

                "figure":
                    fig.to_json(),

                "type":
                    "heatmap"

            })

        except Exception as error:

            print(
                "Correlation chart error:",
                error
            )


# RETURN ALL GENERATED CHARTS

    return charts

