import streamlit as st
import pandas as pd


st.set_page_config(layout="centered")

curr_symbol = st.session_state["curr_symbol"]

st.write("# PerFin")
st.write("### Income 💰")
with st.expander("ℹ️ Track your actual monthly income."):
    st.write("This acts as a guide for setting more accurate values in Monthly Outflows.")

if 'data' not in st.session_state:
    data=pd.DataFrame({
        "Date": [],
        "Net income": [],
        "Health insurance": [],
        "Pension": [],
        "Bonus": []
    })
    st.session_state.data = data

def add_df_form():
    row = pd.DataFrame({
        'Date': [st.session_state.input_incume_date],
        'Net income': [st.session_state.input_income_net],
        'Health insurance': [st.session_state.input_income_health],
        'Pension': [st.session_state.input_income_pension],
        'Bonus': [st.session_state.input_income_bonus],
    })
    st.session_state.data = pd.concat([st.session_state.data, row])

new_income = st.form(key="new_income", clear_on_submit=False)
with new_income:
    st.write("#### Add income data (in " + curr_symbol + ')')

    df_form_columns = st.columns(5)
    with df_form_columns[0]:
        st.date_input("Date", format="YYYY-MM-DD", key="input_incume_date")
    with df_form_columns[1]:
        st.number_input("Net income", min_value=0, step=1, key="input_income_net")
    with df_form_columns[2]:
        st.number_input("Health insurance", min_value=0, step=1, key="input_income_health")
    with df_form_columns[3]:
        st.number_input("Pension", min_value=0, step=1, key="input_income_pension")
    with df_form_columns[4]:
        st.number_input("Bonus", min_value=0, step=1, key="input_income_bonus")
    
    submitted = st.form_submit_button("Submit", help="Adds the data to the table below.", on_click=add_df_form)
    if submitted:
       st.toast("Updated Income table 💰", icon="🎉")

st.dataframe(st.session_state.data, hide_index=True, width=720)