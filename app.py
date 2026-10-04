import streamlit as st
import pandas as pd

from pandas_analyzer import (
    load_csv,
    get_basic_info,
    get_preview,
    get_missing_values,
    get_duplicates,
    get_statistics,
    get_unique_values,
    get_data_types,
    get_correlation,
    group_data
)


# Page setup
st.set_page_config(
    page_title="CSV Data Profiler",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CSV Data Profiler")
st.write("Upload a CSV file and analyze it automatically.")


# Upload CSV
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    # Load CSV using our Pandas function
    df = load_csv(uploaded_file)

    st.success("CSV uploaded successfully!")


    # ---------------- BASIC INFORMATION ----------------

    st.subheader("📋 Basic Information")

    info = get_basic_info(df)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", info["rows"])

    with col2:
        st.metric("Columns", info["columns"])


    # ---------------- DATA PREVIEW ----------------

    st.subheader("📄 Data Preview")

    st.dataframe(
        get_preview(df),
        use_container_width=True
    )


    # ---------------- MISSING VALUES ----------------

    st.subheader("❓ Missing Values")

    missing = get_missing_values(df)

    st.write("Total Missing Values:", missing["Total"])

    missing_df = pd.DataFrame(
        list(missing["by_column"].items()),
        columns=["Column", "Missing Values"]
    )

    st.dataframe(
        missing_df,
        use_container_width=True
    )


    # ---------------- DUPLICATES ----------------

    st.subheader("🔁 Duplicate Rows")

    duplicates = get_duplicates(df)

    st.write("Duplicate Rows:", duplicates)


    # ---------------- STATISTICS ----------------

    st.subheader("📊 Numerical Statistics")

    statistics = get_statistics(df)

    st.dataframe(
        statistics,
        use_container_width=True
    )


    # ---------------- UNIQUE VALUES ----------------

    st.subheader("🔢 Unique Values")

    unique_values = get_unique_values(df)

    unique_df = pd.DataFrame(
        list(unique_values.items()),
        columns=["Column", "Unique Values"]
    )

    st.dataframe(
        unique_df,
        use_container_width=True
    )


    # ---------------- DATA TYPES ----------------

    st.subheader("🔤 Data Types")

    data_types = get_data_types(df)

    types_df = pd.DataFrame(
        list(data_types.items()),
        columns=["Column", "Data Type"]
    )

    st.dataframe(
        types_df,
        use_container_width=True
    )


    # ---------------- CORRELATION ----------------

    st.subheader("🔗 Correlation")

    correlation = get_correlation(df)

    st.dataframe(
        correlation,
        use_container_width=True
    )


    # ---------------- GROUP ANALYSIS ----------------

    st.subheader("📊 Group Analysis")

    categorical_columns = df.select_dtypes(
        include="object"
    ).columns.tolist()

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()


    if categorical_columns and numeric_columns:

        group_column = st.selectbox(
            "Select column to group by",
            categorical_columns
        )

        value_column = st.selectbox(
            "Select numerical column",
            numeric_columns
        )

        operation = st.selectbox(
            "Select operation",
            ["mean", "sum", "max", "min", "count"]
        )

        result = group_data(
            df,
            group_column,
            value_column,
            operation
        )

        st.dataframe(result)


    # ---------------- CLEAN DATA ----------------

    st.subheader("🧹 Clean Dataset")

    st.write(
        "The cleaning functions remove duplicate rows "
        "and fill missing numerical values with the mean."
    )

    if st.button("Clean Data"):

        from pandas_analyzer import clean_data

        cleaned_df = clean_data(df)

        st.success("Data cleaned successfully!")

        st.dataframe(
            cleaned_df,
            use_container_width=True
        )