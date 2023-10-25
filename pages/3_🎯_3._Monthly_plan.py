import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from numpy import isnan

st.set_page_config(layout="centered")

# Load variables
curr_symbol = st.session_state["curr_symbol"]

st.markdown("### Monthly Plan 🎯")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "__🎯 Monthly Plan__",
    "__⚡ Bills &nbsp;__",
    "__🚌 Transportation__",
    "__🏦 Debt &nbsp;__",
    "__🐷 Savings__",
    "__🚀 Investments__",
])

with tab2:
    with st.expander("ℹ️ Monthly Bill Payments"):
        st.markdown("💡 Tip: Estimations are fine.")

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
        edited_df_bills = st.data_editor(df_bills, num_rows="dynamic", width=400,)

        monthly_bills = 0
        for key in edited_df_bills["Amount"]:
            if not isnan(key):
                monthly_bills += int(key)
        st.write("Monthly bills: €", monthly_bills)
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
                # textprops = {'size': 'medium'},
            )
            st.pyplot(fig1)

with tab3:
    with st.expander("ℹ️ Monthly Transportation Costs"):
        st.markdown("💡 You can split any annual expenses in montly payments")

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
        st.write("Estimated monthly transportation costs:", curr_symbol, monthly_transportation)
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
                # textprops = {'size': 'medium'},
            )
            st.pyplot(fig1)

with tab4:
    with st.expander("ℹ️ Monthly Debt Payments"):
        st.markdown("💡 Low interest payments are ok.")
        st.markdown("💡 Try to eliminate higher interest debt.")

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
            width=400,
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
        st.write("Monthly debt payments total:", curr_symbol, monthly_debt)
        if "monthly_debt" not in st.session_state:
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
                # textprops = {'size': 'medium'},
            )
            st.pyplot(fig1)

with tab5:
    with st.expander("ℹ️ Monthly Savings"):
        st.markdown("💡 Savings for any specific purpose.")

    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        df_savings = pd.DataFrame([
            {"Title": "Emergency Fund", "Amount": 0,},
            {"Title": "House Deposit", "Amount": 100,},
            {"Title": "Car", "Amount": 20,},
        ])
        edited_df_savings = st.data_editor(df_savings, num_rows="dynamic", width=400)
        monthly_savings = 0
        for key in edited_df_savings["Amount"]:
            if not isnan(key):
                monthly_savings += key
        st.write("Monthly savings:", curr_symbol, monthly_savings)
        if "monthly_savings" not in st.session_state:
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
                # textprops = {'size': 'medium'},
            )
            st.pyplot(fig1)

with tab6:
    with st.expander("ℹ️ Monthly Investments (DCA)"):
        st.markdown("💡 Automate funding your accounts.")

    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        df_invest = pd.DataFrame([
            {"Title": "Pension", "Amount": 200,},
            {"Title": "Shares", "Amount": 100,},
            {"Title": "Crypto", "Amount": 20,},
        ])
        edited_df_invest = st.data_editor(df_invest, num_rows="dynamic", width=400)
        monthly_investments = 0
        for key in edited_df_invest["Amount"]:
            if not isnan(key):
                monthly_investments += key
        st.write("Monthly investments:", curr_symbol, monthly_investments)
        if "monthly_investments" not in st.session_state:
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
                # textprops = {'size': 'medium'},
            )
            st.pyplot(fig1)

with tab1:
    # Load variables
    # monthly_bills = st.session_state["monthly_bills"]
    # monthly_transportation = st.session_state["monthly_transportation"]
    # monthly_debt = st.session_state["monthly_debt"]
    # monthly_savings = st.session_state["monthly_savings"]
    # monthly_investments = st.session_state["monthly_investments"]
    
    income = 2500
    st.write("Income:", 2500)
    
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
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
        edited_df = st.data_editor(df, num_rows="dynamic", width=400,)
        
        total_necessary = 0
        account_funding = {}
        for item in range(len(edited_df)):
            if edited_df.iloc[item]["Necessary"]:
                total_necessary += edited_df.iloc[item]["Amount"]
        st.write('Necessary:', total_necessary, "€")

        total = 0
        for key in edited_df["Amount"]:
            try: 
                total += key
            except:
                print("Nothing")
        st.write('All outflows:', total, "€")
        if total > income:
            st.write("⚠️ Your expenses are higher than your income.")
    
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
                # textprops = {'size': 'medium'},
            )
            st.pyplot(fig1)