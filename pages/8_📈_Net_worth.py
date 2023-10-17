import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Net Worth")

col1, col2 = st.columns([1, 2], gap="small")

with col1:
    df_net_worth = pd.DataFrame([
       {"Month": "2023-01", "Net Worth": 100,},
       {"Month": "2023-02", "Net Worth": 150,},
       {"Month": "2023-03", "Net Worth": 200,},
       {"Month": "2023-04", "Net Worth": 200,},
       {"Month": "2023-05", "Net Worth": 250,},
       {"Month": "2023-06", "Net Worth": 400,},
       {"Month": "2023-07", "Net Worth": 350,},
       {"Month": "2023-08", "Net Worth": 500,},
       {"Month": "2023-09", "Net Worth": 500,},
       {"Month": "2023-10", "Net Worth": 600,},
       {"Month": "2023-11", "Net Worth": 500,},
       {"Month": "2023-12", "Net Worth": 700,},
   ])
    edited_df = st.data_editor(df_net_worth, num_rows="dynamic")

with col2:
    st.line_chart(edited_df, x="Month", y="Net Worth")
