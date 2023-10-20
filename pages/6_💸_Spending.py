import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

curr_symbol = st.session_state["curr_symbol"]

st.write("# PerFin")
st.write("### Spending 💸")
with st.expander("ℹ️ Track your actual monthly spending."):
    st.write("This acts as a guide for setting more accurate values in Monthly Outflows.")

df_spend = pd.DataFrame(
    [
        {"Date":"2023-10-1", "Rent + Bills":1100, "Pension":100, "Transportation":10, "Food+Fun":500, "Investments":100, "Shopping":50, "Travel":0},
        {"Date":"2023-09-1", "Rent + Bills":1100, "Pension":100, "Transportation":10, "Food+Fun":500, "Investments":100, "Shopping":50, "Travel":0},
        {"Date":"2023-08-1", "Rent + Bills":1100, "Pension":100, "Transportation":10, "Food+Fun":500, "Investments":100, "Shopping":50, "Travel":0},
 ]
)

with st.form("new_spend", clear_on_submit=False):
    st.write("#### Add spending data (in " + curr_symbol + ')')
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        date = str(st.date_input("Date", format="YYYY-MM-DD"))
        spend_rent = st.number_input("Rent + Bills", min_value=0, step=1)
        spend_pension = st.number_input("Pension", min_value=0, step=1)
        spend_transp = st.number_input("Transportation", min_value=0, step=1)
    with col2:
        spend_fun = st.number_input("Food + Fun", min_value=0, step=1)
        spend_invest = st.number_input("Investments", min_value=0, step=1)
        spend_shop = st.number_input("Shopping", min_value=0, step=1)
        spend_travel = st.number_input("Travel expenses", min_value=0, step=1)
    submitted = st.form_submit_button("Submit", help="Adds the data to the table below.")
    if submitted:
       df_spend.add({
           "Date": date, 
            "Rent + Bills": spend_rent, 
            "Pension": spend_pension, 
            "Transportation": spend_transp,
            "Food + Fun": spend_fun,
            "Investments": spend_invest,
            "Shopping": spend_shop,
            "Travel": spend_travel,
        })
       st.toast("Updated Spending table 💸", icon="🎉")

st.dataframe(df_spend, hide_index=True, width=720)
