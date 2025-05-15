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
from io import BytesIO

st.title("Water Requirement Calculator")

uploaded_file = st.file_uploader("Book1.xlsx", type=["xlsx"])

if uploaded_file:
    # Read the uploaded Excel file
    df = pd.read_excel(uploaded_file)
    st.write("Preview of uploaded data:", df.head())

    # Check for required columns
    required_columns = [
        'Ab Rh @ Achivable Temp & 80% Rh (gm/m3)',
        'Absolute Humidity (gm/m3)'
    ]
    if all(col in df.columns for col in required_columns):
        # Perform calculations
        df['Moisture to add(ml/m3)'] = df['Ab Rh @ Achivable Temp & 80% Rh (gm/m3)'] - df['Absolute Humidity (gm/m3)']
        df['Water Required'] = df['Moisture to add(ml/m3)'] * 69340.64 * 0.4 / 1000 * 60
        df['WaterRequired'] = df['Water Required'] * 11
        df['Requirement Ltr/SqM/Day'] = df['WaterRequired'] / 9216

        st.success("Calculation complete! Preview of results:")
        st.write(df.head())

        # Prepare Excel file for download
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        st.download_button(
            label="Download Result Excel File",
            data=output,
            file_name="finalresult.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error(f"Your file must contain the columns: {', '.join(required_columns)}")
else:
    st.info("Please upload an Excel file to begin.")


# %%
