import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from numpy import isnan
import locale

locale.setlocale( locale.LC_ALL, '' )
def curr_fmt(val):
    return locale.currency(val, symbol=False, grouping=True)

# Load variables
curr_symbol = st.session_state["curr_symbol"]
last_net_income = st.session_state.last_net_income

st.markdown("### Monthly budget")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "__🎯 Monthly budget__",
    "__⚡ Bills &nbsp;__",
    "__🚌 Transportation__",
    "__🏦 Debt &nbsp;__",
    "__🐷 Savings__",
    "__🚀 Investments__",
])

with tab2:
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        df_bills = pd.DataFrame([
           {"Title": "Mobile Phone", "Amount": 20},
           {"Title": "Internet", "Amount": 30},
           {"Title": "Electricity", "Amount": 38},
           {"Title": "Gas", "Amount": 30},
           {"Title": "iCloud", "Amount": 2},
           {"Title": "Netflix", "Amount": 6},
           {"Title": "Bins", "Amount": 10},
       ])
        edited_df_bills = st.data_editor(df_bills, num_rows="dynamic", use_container_width=True)

        monthly_bills = 0
        for key in edited_df_bills["Amount"]:
            if not isnan(key):
                monthly_bills += int(key)
        st.info("Monthly bills: __" + curr_symbol + str(curr_fmt(monthly_bills)) + "__")

        if "monthly_bills" not in st.session_state:
            st.session_state["monthly_bills"] = monthly_bills

    with col2:
        if len(edited_df_bills["Amount"]) > 1 and monthly_bills > 0 and edited_df_bills["Amount"].isnull().values.any() == False:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df_bills["Amount"],
                labels=edited_df_bills["Title"],
                autopct='%.0d%%',
                pctdistance=0.83,
                counterclock=False,
                startangle=90,
            )
            st.pyplot(fig1)

with tab3:
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        df_transp = pd.DataFrame([
           {"Title": "Bus", "Amount": 12},
           {"Title": "Taxi", "Amount": 25},
           {"Title": "Car Insurance", "Amount": 3},
           {"Title": "Dublin Bike", "Amount": 3},
       ])
        edited_df_transp = st.data_editor(df_transp, num_rows="dynamic", width=400,)

        monthly_transportation = 0
        for key in edited_df_transp["Amount"]:
            if not isnan(key):
                monthly_transportation += key
        st.info("Estimated monthly transportation costs: __" + curr_symbol + curr_fmt(monthly_transportation) + "__")

        if "monthly_transportation" not in st.session_state:
            st.session_state["monthly_transportation"] = monthly_transportation

    with col2:
        if len(edited_df_transp["Amount"]) > 1 and monthly_transportation > 0 and edited_df_transp["Amount"].isnull().values.any() == False:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df_transp["Amount"],
                labels=edited_df_transp["Title"],
                autopct='%.0d%%',
                pctdistance=0.83,
                counterclock=False,
                startangle=90,
            )
            st.pyplot(fig1)

with tab4:
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        df_debt = pd.DataFrame([
           {"Title": "Mortgage", "Amount": 2},
           {"Title": "Car loan", "Amount": 1},
           {"Title": "Loan", "Amount": 1},
           {"Title": "Credit card", "Amount": 1},
       ])
        edited_df_debt = st.data_editor(
            df_debt,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Amount": st.column_config.NumberColumn(
                    format=curr_symbol + "%d",
                    min_value=0,
                ),
            }
        )

        monthly_debt = 0
        for key in edited_df_debt["Amount"]:
            if not isnan(key):
                monthly_debt += key
        st.info("Monthly debt payments total: __" + curr_symbol + curr_fmt(monthly_debt) + "__")
        st.session_state["monthly_debt"] = monthly_debt

    with col2:
        if len(edited_df_debt["Amount"]) > 1 and monthly_debt > 0 and edited_df_debt["Amount"].isnull().values.any() == False:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df_debt["Amount"],
                labels=edited_df_debt["Title"],
                autopct='%.0d%%',
                pctdistance=0.83,
                counterclock=False,
                startangle=90,
            )
            st.pyplot(fig1)

with tab5:
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        df_savings = pd.DataFrame([
            {"Title": "Emergency Fund", "Amount": 0,},
            {"Title": "House Deposit", "Amount": 100,},
            {"Title": "Car", "Amount": 20,},
        ])
        edited_df_savings = st.data_editor(df_savings, num_rows="dynamic", use_container_width=True)
        monthly_savings = 0
        for key in edited_df_savings["Amount"]:
            if not isnan(key):
                monthly_savings += key
        st.info("Monthly savings: __" + curr_symbol + str(monthly_savings) + "__")
        st.session_state["monthly_savings"] = monthly_savings

    with col2:
        if len(edited_df_savings["Amount"]) > 1 and monthly_savings > 0 and edited_df_savings["Amount"].isnull().values.any() == False:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df_savings["Amount"],
                labels=edited_df_savings["Title"],
                autopct='%.0d%%',
                pctdistance=0.83,
                counterclock=False,
                startangle=90,
            )
            st.pyplot(fig1)

with tab6:
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        df_invest = pd.DataFrame([
            {"Title": "Pension", "Amount": 200,},
            {"Title": "Shares", "Amount": 100,},
            {"Title": "Crypto", "Amount": 20,},
        ])
        edited_df_invest = st.data_editor(df_invest, num_rows="dynamic", use_container_width=True)
        monthly_investments = 0
        for key in edited_df_invest["Amount"]:
            if not isnan(key):
                monthly_investments += key
        st.info("Monthly investments: __" + curr_symbol + curr_fmt(monthly_investments) + "__")
        st.session_state["monthly_investments"] = monthly_investments

    with col2:
        if len(edited_df_invest["Amount"]) > 1 and monthly_investments > 0 and edited_df_invest["Amount"].isnull().values.any() == False:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df_invest["Amount"],
                labels=edited_df_invest["Title"],
                autopct='%.0d%%',
                pctdistance=0.83,
                counterclock=False,
                startangle=90,
            )
            st.pyplot(fig1)

with tab1:
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        st.info("Income: __" + curr_symbol + curr_fmt(last_net_income) + "__")
        df = pd.DataFrame([
            {"Purpose": "Rent", "Amount": 1000, "Necessary": True},
            {"Purpose": "Bills", "Amount": monthly_bills, "Necessary": True},
            {"Purpose": "Transportation", "Amount": monthly_transportation, "Necessary": True},
            {"Purpose": "Debt", "Amount": monthly_debt, "Necessary": True},
            {"Purpose": "Savings", "Amount": monthly_savings, "Necessary": False},
            {"Purpose": "Investments", "Amount": monthly_investments, "Necessary": False},
            {"Purpose": "Food & fun", "Amount": 500, "Necessary": True},
            {"Purpose": "Shopping", "Amount": 250, "Necessary": False},
            {"Purpose": "Traveling", "Amount": 250, "Necessary": False},
        ])
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        total_necessary = 0
        account_funding = {}
        for item in range(len(edited_df)):
            if edited_df.iloc[item]["Necessary"]:
                total_necessary += edited_df.iloc[item]["Amount"]
        st.info("Necessary: __" + curr_symbol + str(curr_fmt(total_necessary)) + "__")
        st.session_state["necessary_expenses"] = total_necessary

        total = 0
        for key in edited_df["Amount"]:
            try: 
                total += key
            except:
                print("Nothing")
        st.info("All outflows: __" + curr_symbol + curr_fmt(total) + "__")
    
    with col2:
        if len(edited_df["Amount"]) > 1:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df["Amount"],
                labels=edited_df["Purpose"],
                autopct='%.0d%%',
                pctdistance=0.83,
                counterclock=False,
                startangle=90,
            )
            st.pyplot(fig1)

    if total > last_net_income:
        st.warning(body="Your expenses are higher than your income.", icon="⚠️")