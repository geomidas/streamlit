import streamlit as st
import pandas as pd


st.write("# PerFin")
st.write("### Spending 💰")

if 'spend_data' not in st.session_state:
    spend_data=pd.DataFrame({
        "Date": [],
        "Rent + Bills": [],
        "Pension": [],
        "Transportation": [],
        "Food + Fun": [],
        "Investments": [],
        "Shopping": [],
        "Travel": [],
    })
    st.session_state.spend_data = spend_data

def add_df_form():
    row = pd.DataFrame({
        "Date": [st.session_state.input_incume_date],
        "Rent + Bills": [st.session_state.input_spend_rent],
        "Pension": [st.session_state.input_spend_pension],
        "Transportation": [st.session_state.input_spend_transp],
        "Food + Fun": [st.session_state.input_spend_food],
        "Investments": [st.session_state.input_spend_invest],
        "Shopping": [st.session_state.input_spend_shop],
        "Travel": [st.session_state.input_spend_travel],
    })
    st.session_state.spend_data = pd.concat([st.session_state.spend_data, row])

with st.expander("ℹ️ Track your actual monthly spending."):
    st.write("This acts as a guide for setting more accurate values in Monthly Outflows.")
    if len(st.session_state.spend_data) > 1:
        st.write("##### Average")
        for key in st.session_state.spend_data:
            if key in "Date":
                pass
            elif key in "Rent + Bills":
                values_list = st.session_state.spend_data[key]
                avg_spend_rent = sum(values_list)/len(values_list)
            elif key in "Pension":
                values_list = st.session_state.spend_data[key]
                avg_spend_pension = sum(values_list)/len(values_list)
            elif key in "Transportation":
                values_list = st.session_state.spend_data[key]
                avg_spend_transp = sum(values_list)/len(values_list)
            elif key in "Food + Fun":
                values_list = st.session_state.spend_data[key]
                avg_spend_food = sum(values_list)/len(values_list)
            elif key in "Investments":
                values_list = st.session_state.spend_data[key]
                avg_spend_invest = sum(values_list)/len(values_list)
            elif key in "Shopping":
                values_list = st.session_state.spend_data[key]
                avg_spend_shop = sum(values_list)/len(values_list)
            elif key in "Travel":
                values_list = st.session_state.spend_data[key]
                avg_spend_travel = sum(values_list)/len(values_list)
            else:
                pass
        spend_averages = pd.DataFrame({
            "Rent + Bills": [avg_spend_rent],
            "Pension": [avg_spend_pension],
            "Transportation": [avg_spend_transp],
            "Food + Fun": [avg_spend_food],
            "Investments": [avg_spend_invest],
            "Shopping": [avg_spend_shop],
            "Travel": [avg_spend_travel],
        })
        st.dataframe(spend_averages, hide_index=True, width=720)

new_income = st.form(key="new_income", clear_on_submit=False)
with new_income:
    st.write("#### Add income data")
    df_form_columns = st.columns(8)
    with df_form_columns[0]:
        st.date_input("Date", format="YYYY-MM-DD", key="input_incume_date")
    with df_form_columns[1]:
        st.number_input("Rent + Bills", min_value=0, step=1, key="input_spend_rent")
    with df_form_columns[2]:
        st.number_input("Pension", min_value=0, step=1, key="input_spend_pension")
    with df_form_columns[3]:
        st.number_input("Transport", min_value=0, step=1, key="input_spend_transp")
    with df_form_columns[4]:
        st.number_input("Food + Fun", min_value=0, step=1, key="input_spend_food")
    with df_form_columns[5]:
        st.number_input("Invested", min_value=0, step=1, key="input_spend_invest")
    with df_form_columns[6]:
        st.number_input("Shopping", min_value=0, step=1, key="input_spend_shop")
    with df_form_columns[7]:
        st.number_input("Travel", min_value=0, step=1, key="input_spend_travel")

    submitted = st.form_submit_button("Submit", help="Adds the data to the table below.", on_click=add_df_form)
    if submitted:
       st.toast("Updated Spending 💸", icon="🎉")

st.write("##### All data")
st.dataframe(st.session_state.spend_data, hide_index=True, width=720)
