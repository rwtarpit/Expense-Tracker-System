import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000"

def analytics_month_tab():
    # Single button to get all monthly data
    if st.button("Get Monthly Analytics"):
        # Request data from the backend for all months
        response = requests.post(f"{API_URL}/analytics/monthly")
        
        if response.status_code == 200:
            data = response.json()

            # Process data into a DataFrame
            df = pd.DataFrame(data)
            df['month'] = pd.to_datetime(df['month'], format='%Y-%m')  # Convert month to datetime
            df['month'] = pd.to_datetime(df['month']).dt.strftime('%B %Y')
            df['total_expense'] = df['total_expense'].apply(lambda x: round(x, 2))  # Round the total expenses

            # Display data
            st.title("Monthly Expense Breakdown")

            # Plot the bar chart using Streamlit's built-in method
            st.bar_chart(df.set_index('month')['total_expense'], width=0, height=0, use_container_width=True,)

            # Display the table
            st.subheader("Detailed Monthly Expense Data")
            df_sorted = df.sort_values(by="total_expense", ascending=False)
            st.table(df_sorted)

        else:
            st.error("Failed to retrieve monthly analytics.")
