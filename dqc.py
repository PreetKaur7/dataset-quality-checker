import streamlit as st
import pandas as pd
import numpy as np

def calculate_quality_score(df):
    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    type_mismatches = sum(df.applymap(lambda x: not isinstance(x, (int, float, str)) and pd.notna(x)).sum())
    
    issue_weight = missing_cells + duplicate_rows + type_mismatches
    score = max(0, 100 - (issue_weight / total_cells * 100))
    return round(score, 2)

def main():
    st.title("Dataset Quality Checker")
    st.write("Upload a CSV file to check its quality.")
    
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Data Preview:")
        st.dataframe(df.head())
        
        st.write("### Data Quality Analysis:")
        
        missing_values = df.isnull().sum()
        missing_cols = missing_values[missing_values > 0]
        
        duplicate_count = df.duplicated().sum()
        
        type_mismatches = {
            col: df[col].apply(lambda x: not isinstance(x, (int, float, str)) and pd.notna(x)).sum()
            for col in df.columns
        }
        type_mismatch_cols = {k: v for k, v in type_mismatches.items() if v > 0}
        
        quality_score = calculate_quality_score(df)
        
        st.metric("Dataset Quality Score", f"{quality_score}/100")
        
        if not missing_cols.empty:
            st.write("### Columns with Missing Values:")
            st.write(missing_cols)
        
        if duplicate_count > 0:
            st.write(f"### Duplicate Rows: {duplicate_count}")
            
        if type_mismatch_cols:
            st.write("### Columns with Data Type Mismatches:")
            st.write(type_mismatch_cols)
        
        st.write("### Suggested Fixes:")
        if not missing_cols.empty:
            st.write("- Fill missing values using mean/median for numerical columns or mode for categorical columns.")
        if duplicate_count > 0:
            st.write("- Consider removing duplicate rows.")
        if type_mismatch_cols:
            st.write("- Check and correct inconsistent data types.")
        
if __name__ == "__main__":
    main()
