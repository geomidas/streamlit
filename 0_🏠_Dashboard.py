import streamlit as st
import pandas as pd


# st.set_page_config(layout="centered")
st.set_page_config("PerFin", page_icon="💎")

st.markdown("### PerFin")

col1, col2 = st.columns([1,1], gap="medium")
with col1:
    selected_currency=st.selectbox("Currency:", options=("EUR","GBP","USD"))
    if "selected_currency" not in st.session_state:
        st.session_state["selected_currency"] = selected_currency
    if selected_currency == "EUR":
        curr_symbol = "€"
    elif selected_currency == "GBP":
        curr_symbol = "£"
    elif selected_currency == "GBP":
        curr_symbol = "$"
    else:
        curr_symbol = selected_currency
    st.write("Symbol:", curr_symbol)
    if "curr_symbol" not in st.session_state:
        st.session_state["curr_symbol"] = curr_symbol

    st.markdown("### Tips")
    st.markdown("""
    - Update this app at the end of every month :sparkles:
    - Review your allocation in 
        - [Debt payments](/Monthly_Outflows)
        - [Bills](/Monthly_Outflows)
        - [Tansportation](/Monthly_Outflows)
        - [Investments](/Monthly_Outflows)
        - [Savings](/Monthly_plan) (in the Monthly Plan)
    - Add this month's
        - [Income](/Income)
        - [Spending](/Spending)
    - Done! :tada:
    """)
