import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Spending")
st.markdown("Track your actual monthly spending.")

df = pd.DataFrame(
    [
       {"Month":"2023-01", "Rent+Bills":1100, "Pension":100, "Transportation":10, "Food+Fun":500, "Investments":100, "Shopping":50, "Travel":0},
   ]
)
edited_df = st.data_editor(
    df,
    hide_index=True,   
    num_rows="dynamic",
)
