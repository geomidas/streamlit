import streamlit as st
import pandas as pd


st.set_page_config(layout="centered")

curr_symbol = st.session_state["curr_symbol"]

st.write("# Perfin")
st.write("### Income 💰")
with st.expander("ℹ️ Track your actual monthly income."):
    st.write("This acts as a guide for setting more accurate values in Monthly Outflows.")

df = pd.DataFrame(
    [
       {"Date": "2023-10-1", "Net income": 2500, "Health insurance": 0, "Pension contribution":100, "Bonus": 0},
       {"Date": "2023-09-1", "Net income": 2500, "Health insurance": 0, "Pension contribution":100, "Bonus": 0},
       {"Date": "2023-08-1", "Net income": 2500, "Health insurance": 0, "Pension contribution":100, "Bonus": 0},

   ]
)

with st.form("new_income", clear_on_submit=False):
    st.write("#### Add income data (in " + curr_symbol + ')')
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        date = str(st.date_input("Date", format="YYYY-MM-DD"))
        income_net = st.number_input("Net income", min_value=0, step=1)
    with col2:
        income_health = st.number_input("Health insurance", min_value=0, step=1)
        income_pension = st.number_input("Pension contribution", min_value=0, step=1)
        income_bonus = st.number_input("Bonus", min_value=0, step=1)
    submitted = st.form_submit_button("Submit", help="Adds the data to the table below.")
    if submitted:
       df.add({"Date": date, "Net income": income_net, "Health insurance": income_health, "Pension contribution": income_pension, "Bonus": income_bonus})
       st.toast("Updated Income table 💰", icon="🎉")

st.dataframe(df, hide_index=True, width=720)
