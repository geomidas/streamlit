import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Spending 💸")
st.markdown("Track your actual monthly spending. This acts as a guide for setting more accurate values in Monthly Outflows.")

st.form("Add new data")

df = pd.DataFrame(
    [
        {"Month":"2023-10", "Rent+Bills":1100, "Pension":100, "Transportation":10, "Food+Fun":500, "Investments":100, "Shopping":50, "Travel":0},
        {"Month":"2023-09", "Rent+Bills":1100, "Pension":100, "Transportation":10, "Food+Fun":500, "Investments":100, "Shopping":50, "Travel":0},
        {"Month":"2023-08", "Rent+Bills":1100, "Pension":100, "Transportation":10, "Food+Fun":500, "Investments":100, "Shopping":50, "Travel":0},
 ]
)
st.table(df)
