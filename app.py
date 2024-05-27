import streamlit as st
import requests
import pandas as pd

st.title("Subscription Pricing Calculator")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    with st.spinner('Uploading and processing...'):
        files = {'file': uploaded_file}
        response = requests.post("http://127.0.0.1:5000/upload", files=files)

        if response.status_code == 200:
            filename = response.json()['filename']
            st.success('File uploaded successfully!')

            # Fetch the processed data
            response = requests.get(f"http://127.0.0.1:5000/data/{filename}")
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)

                # Display data with pagination
                st.write("Data Preview:")
                rows_per_page = 20
                total_rows = len(df)
                total_pages = (total_rows // rows_per_page) + (1 if total_rows % rows_per_page > 0 else 0)
                page = st.number_input('Page', min_value=1, max_value=total_pages, step=1)
                start_idx = (page - 1) * rows_per_page
                end_idx = start_idx + rows_per_page
                st.dataframe(df.iloc[start_idx:end_idx])

                # Display subscription pricing
                st.write("Subscription Pricing Preview:")
                st.dataframe(df[['CreditScore', 'CreditLines', 'SubscriptionPrice']].iloc[start_idx:end_idx])
            else:
                st.error("Failed to fetch the processed data.")
        else:
            st.error("File upload failed. Please make sure the CSV file has 'CreditScore' and 'CreditLines' columns.")
