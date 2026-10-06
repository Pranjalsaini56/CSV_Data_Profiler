import io

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from pandas_analyzer import get_correlation, get_missing_values, group_data

# Size of every chart (width, height in inches) - small enough for a laptop screen
CHART_SIZE = (6, 3.5)
MAX_X_VALUES = 15   # X-Y bar chart allows at most this many different X values


# Histogram: shows how values of a numeric column are spread
def plot_histogram(df, column, bins=10):
    fig, ax = plt.subplots(figsize=CHART_SIZE)
    ax.hist(df[column].dropna(), bins=bins, color="skyblue", edgecolor="black")
    ax.set_title("Histogram of " + column)
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    return fig


# Bar chart of X vs Y: one bar for each X value, bar height = mean/sum/... of Y
# Example: x_column="Age", y_column="Salary", operation="mean" -> average salary of each age
def plot_xy_bar(df, x_column, y_column, operation="mean"):
    result = group_data(df, x_column, y_column, operation)
    if pd.api.types.is_numeric_dtype(result.index):
        result = result.sort_index()                       # numbers: smallest to largest
        labels = [str(int(i)) if float(i).is_integer() else str(i) for i in result.index]  # 20.0 -> 20
    else:
        result = result.sort_values(ascending=False)       # text: biggest bar first
        labels = result.index.astype(str)
    fig, ax = plt.subplots(figsize=CHART_SIZE)
    bars = ax.bar(labels, result.values, color="orange", edgecolor="black")
    ax.bar_label(bars, fmt="%.1f", fontsize=8)
    ax.set_title(operation.capitalize() + " of " + y_column + " by " + x_column)
    ax.set_xlabel(x_column)
    ax.set_ylabel(operation + " of " + y_column)
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig


# Bar chart: counts of each value in a column (top 10 only)
def plot_count_bar(df, column):
    counts = df[column].value_counts().head(10)
    fig, ax = plt.subplots(figsize=CHART_SIZE)
    bars = ax.bar(counts.index.astype(str), counts.values, color="orange", edgecolor="black")
    ax.bar_label(bars, fontsize=8)
    ax.set_title("Count of each value in " + column)
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig


# Pie chart: percentage share of each value in a text column (top 6 only)
def plot_pie(df, column):
    counts = df[column].value_counts().head(6)
    fig, ax = plt.subplots(figsize=CHART_SIZE)
    ax.pie(counts.values, labels=counts.index.astype(str), autopct="%1.1f%%")
    ax.set_title("Pie Chart of " + column)
    fig.tight_layout()
    return fig


# Scatter plot: relation between two numeric columns
def plot_scatter(df, x_column, y_column):
    fig, ax = plt.subplots(figsize=CHART_SIZE)
    ax.scatter(df[x_column], df[y_column], color="green")
    ax.set_title(y_column + " vs " + x_column)
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    fig.tight_layout()
    return fig


# Heatmap: correlation between all numeric columns
def plot_heatmap(df):
    corr = get_correlation(df)
    fig, ax = plt.subplots(figsize=(5, 4.5))
    img = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45)
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, round(corr.iloc[i, j], 2), ha="center", va="center")
    fig.colorbar(img)
    ax.set_title("Correlation Heatmap")
    fig.tight_layout()
    return fig


# Bar chart of missing values in each column
def plot_missing(df):
    missing = get_missing_values(df)["by_column"]
    fig, ax = plt.subplots(figsize=CHART_SIZE)
    ax.bar(list(missing.keys()), list(missing.values()), color="red", edgecolor="black")
    ax.set_title("Missing Values per Column")
    ax.set_ylabel("Missing count")
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig


# Show a figure at a fixed, small size (so it never fills the whole screen)
def show_figure(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=100)
    st.image(buffer, width=600)
    plt.close(fig)


# Menu used by app.py
def render_visualization_menu(df):
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    all_columns = df.columns.tolist()
    text_columns = df.select_dtypes(exclude="number").columns.tolist()

    choice = st.selectbox(
        "Choose a chart",
        ["Histogram", "Bar Chart (X vs Y)", "Bar Chart (counts)", "Pie Chart",
         "Scatter Plot", "Correlation Heatmap", "Missing Values"]
    )

    fig = None

    if choice == "Histogram":
        if numeric_columns:
            col1, col2 = st.columns(2)
            with col1:
                column = st.selectbox("Select numeric column", numeric_columns)
            with col2:
                bins = st.slider("Number of bins", 3, 50, 10)
            fig = plot_histogram(df, column, bins)
        else:
            st.warning("No numeric columns found.")

    elif choice == "Bar Chart (X vs Y)":
        if numeric_columns:
            col1, col2, col3 = st.columns(3)
            with col1:
                x_column = st.selectbox("X axis (any column)", all_columns)
            with col2:
                y_column = st.selectbox("Y axis (numeric column)", numeric_columns)
            with col3:
                operation = st.selectbox("Value of each bar", ["mean", "sum", "max", "min", "count"])
            if df[x_column].nunique() > MAX_X_VALUES:
                st.warning(
                    x_column + " has " + str(df[x_column].nunique()) + " different values - "
                    "too many bars to read. Pick an X column with " + str(MAX_X_VALUES) +
                    " or fewer values, or use the Scatter Plot."
                )
            else:
                fig = plot_xy_bar(df, x_column, y_column, operation)
        else:
            st.warning("No numeric columns found.")

    elif choice == "Bar Chart (counts)":
        column = st.selectbox("Select column", all_columns)
        fig = plot_count_bar(df, column)

    elif choice == "Pie Chart":
        if text_columns:
            column = st.selectbox("Select column", text_columns)
            fig = plot_pie(df, column)
        else:
            st.warning("No text columns found.")

    elif choice == "Scatter Plot":
        if len(numeric_columns) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_column = st.selectbox("X axis", numeric_columns)
            with col2:
                y_column = st.selectbox("Y axis", numeric_columns, index=1)
            fig = plot_scatter(df, x_column, y_column)
        else:
            st.warning("Need at least 2 numeric columns.")

    elif choice == "Correlation Heatmap":
        if len(numeric_columns) >= 2:
            fig = plot_heatmap(df)
        else:
            st.warning("Need at least 2 numeric columns.")

    elif choice == "Missing Values":
        fig = plot_missing(df)

    if fig is not None:
        show_figure(fig)