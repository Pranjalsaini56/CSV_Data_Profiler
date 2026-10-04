import pandas as pd

#Load the csv
def load_csv(file_path):
    df=pd.read_csv(file_path)
    return df

#Get basic information
def get_basic_info(df):
    return{
        "rows":df.shape[0],#gives number of rows
        "columns":df.shape[1],#gives number of columns
        "column_names":list(df.columns),"data_types":df.dtypes.astype(str).to_dict()
    }

#Get preview
def get_preview(df):
    return df.head()

#Missing data
def get_missing_values(df):
    missing=df.isnull().sum()
    return{
        "Total":int(missing.sum()),
        "by_column":missing.to_dict()
    }

#duplicate rows
def get_duplicates(df):
    return int(df.duplicated().sum())

def get_statistics(df):
    numeric_df=df.select_dtypes(include="number") #selects only the numeric columns
    if numeric_df.empty:
        return pd.DataFrame()  #empty dataframe
    return numeric_df.describe().T  #calculate statistics using describe(count,max,mean,min,...)  and then take its transposecolumns to row 

def get_unique_values(df):
    return df.nunique().to_dict()

def get_data_types(df):
    return df.dtypes.astype(str).to_dict()

def remove_duplicates(df):
    return df.drop_duplicates()

#fill missing numerical values
def fill_missing_values(df,method="mean"):
    df=df.copy()
    numeric_columns=df.select_dtypes(include="number").columns
    for column in numeric_columns:
        if method=="mean":
            df[column]=df[column].fillna(df[column].mean())
        elif method=="median":
            df[column]=df[column].fillna(df[column].median())
        elif method=="zero":
            df[column]=df[column].fillna(0)
    return df

#group and aggregate data
def group_data(df,group_column,value_column,operation="mean"):
    grouped=df.groupby(group_column)[value_column]
    if operation=="mean":
        return grouped.mean()
    elif operation=="sum":
        return grouped.sum()
    elif operation=="max":
        return grouped.max()
    elif operation=="min":
        return grouped.min()
    elif operation=="count":
        return grouped.count()

#corelation #1=postive correlation=one up other also up
#-1=negative correlation=one up another down
#0=zero correlation(no relationship)
def get_correlation(df):
    numeric_df=df.select_dtypes(include="number")
    if numeric_df.empty:
        return pd.DataFrame()
    return numeric_df.corr()

#clean dataset
def clean_data(df):
    df=df.drop_duplicates()
    df=fill_missing_values(df,"mean")
    return df

#testing the pandas module
if __name__=="__main__":
    df=load_csv("sample_sales.csv")
    
    print("\n--- DATA ---")
    print(df)

    print("\n--- BASIC INFORMATION ---")
    print(get_basic_info(df))

    print("\n--- PREVIEW ---")
    print(get_preview(df))

    print("\n--- MISSING VALUES ---")
    print(get_missing_values(df))

    print("\n--- DUPLICATES ---")
    print(get_duplicates(df))

    print("\n--- STATISTICS ---")
    print(get_statistics(df))

    print("\n--- UNIQUE VALUES ---")
    print(get_unique_values(df))

    print("\n--- DATA TYPES ---")
    print(get_data_types(df))

    print("\n--- CORRELATION ---")
    print(get_correlation(df))

    print("\n--- GROUPED DATA ---")
    print(group_data(df, "Department", "Salary", "mean"))

    print("\n--- CLEANED DATA ---")
    cleaned_df = clean_data(df)
    print(cleaned_df)