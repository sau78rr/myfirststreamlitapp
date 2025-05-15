# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.1
# ---

# %%
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Water Requirement Calculator", layout="centered")

st.title("Automated Water Requirement Calculator")

# 1. File uploader
uploaded_file = st.file_uploader("data.xlsx", type=["xlsx"])

if uploaded_file:
    # 2. Select sheet
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    sheet = st.selectbox("Water Calculation V3.1", sheet_names)
    df = pd.read_excel(xls, sheet_name=sheet)
    
    st.subheader("Preview of Input Data")
    st.dataframe(df.head())

    # 3. Input parameters (if not in sheet)
    water_req_per_sqm = st.number_input("Water Requirement per SqM (Ltr)", value=12)
    days = st.number_input("Number of Days (for monthly calculation)", value=30)
    
    # 4. Calculation
    # Ensure columns exist and handle missing values
    required_cols = [
        "Area in SqM", "Road @ Centre", "Inside Road Area", "Hockey Area"
    ]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Column '{col}' not found in sheet. Please check your file.")
            st.stop()
    df = df.fillna(0)
    df['Growing Area'] = (
        df['Area in SqM'] - (
            df['Road @ Centre'] + df['Inside Road Area'] + df['Hockey Area']
        )
    )
    df['Water Requirement / Sqm'] = water_req_per_sqm
    df['Total Water (Ltr/Day)'] = df['Growing Area'] * df['Water Requirement / Sqm']
    df['Monthly Water (Ltr)'] = df['Total Water (Ltr/Day)'] * days

    st.subheader("Calculated Water Requirement")
    st.dataframe(df[[
        "Area in SqM", "Growing Area", "Water Requirement / Sqm",
        "Total Water (Ltr/Day)", "Monthly Water (Ltr)"
    ]])

    # 5. Download results
    @st.cache_data
    def convert_df(df):
        return df.to_excel(index=False, engine='openpyxl')

    result_xlsx = convert_df(df)
    st.download_button(
        label="Download Results as Excel",
        data=result_xlsx,
        file_name="water_calculation_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Please upload an Excel file to get started.")

