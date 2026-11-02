📊 CSV Data Profiler

CSV Data Profiler is a Python-based data analysis tool that automatically examines uploaded CSV files and generates useful insights about their structure, data quality and numerical statistics.

The application provides an easy-to-use interface where users can upload datasets, explore their contents, identify missing values and duplicates, perform statistical analysis and clean their data.

✨ Features

📁 1. CSV Upload

- Upload CSV files directly through the application.
- Automatically load CSV data into Pandas DataFrames.

🔍 2. Dataset Overview

- Total number of rows and columns.
- Column names and data types.
- Preview of the uploaded dataset.

🧹 3. Data Quality Analysis

- Detect missing values.
- Calculate missing values column-wise.
- Identify duplicate rows.
- Remove duplicate records.
- Fill missing numerical values using mean, median or zero.

📈 4. Statistical Analysis

- Mean
- Median
- Standard deviation
- Minimum and maximum
- Quartiles
- Count

🔢 5. Unique Values

- Identify the number of distinct values in each column.

🔗 6. Correlation Analysis

- Calculate correlations between numerical columns.
- Display a correlation matrix.

📊 7. Grouping and Aggregation

Perform grouping operations using categorical columns and calculate:

- Mean
- Sum
- Minimum
- Maximum
- Count

🛠️ Technologies Used

Technology| Purpose
Python| Core programming language
Pandas| CSV processing, data manipulation and analysis
Streamlit| Interactive web application interface

📂 Project Structure

CSV_Data_Profiler/
│
├── app.py                 # Main Streamlit application
├── pandas_analyzer.py     # Pandas analysis functions
├── sample_sales.csv       # Sample dataset for testing
└── README.md              # Project documentation

⚙️ Installation and Setup

1. Clone the repository

git clone https://github.com/Pranjalsaini56/CSV_Data_Profiler.git

2. Navigate to the project directory

cd CSV_Data_Profiler

3. Install dependencies

pip install streamlit pandas

4. Run the application

streamlit run app.py

The application will open automatically in your default web browser.

🚀 How to Use

1. Launch the application.
2. Upload a CSV file.
3. View the dataset overview and preview.
4. Explore missing values and duplicate records.
5. Analyze numerical statistics.
6. Examine unique values and data types.
7. Explore correlations between numerical columns.
8. Perform grouping and aggregation.
9. Clean the dataset using the available cleaning options.

🎯 Project Objective

The objective of this project is to simplify the initial stage of data analysis by automating common dataset exploration and data-cleaning tasks.

It helps developers and data analysts understand the structure and quality of a dataset without manually performing every operation.

🔮 Future Enhancements

- NumPy-based numerical analysis.
- Matplotlib data visualizations.
- Interactive charts and graphical reports.
- Export cleaned datasets.
- Support for additional data formats.

👩‍💻 Contributors

Developed collaboratively as a team project using Python and data analysis libraries.

---

CSV Data Profiler — Making Dataset Analysis Simpler!
