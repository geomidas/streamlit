import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from numpy import isnan

st.set_page_config(layout="centered")

# Load variables
curr_symbol = st.session_state["curr_symbol"]

st.markdown("# Perfin")
st.markdown("### Monthly Outflows 🔮")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["__⚡ Bills &nbsp;__", "__🚌 Transportation__", "__🏦 Debt &nbsp;__", "__🐷 Savings__", "__🚀 Investments__"])

with tab1:
    st.markdown("### Monthly Bill Payments")
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("💡 Tip: Estimations are fine 🔮")
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

with tab2:
    st.markdown("### Monthly Transportation Costs")

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("💡 You can split any annual expenses in montly payments")

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

with tab3:
    st.markdown("### Monthly Debt Payments")
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("💡 Low interest payments are ok.")
        st.markdown("💡 Try to eliminate higher interest debt.")

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

with tab4:
    st.markdown("### Monthly Savings")

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("💡 Savings for any specific purpose.")

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

with tab5:
    st.markdown("### Monthly Investments")

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("💡 Automate funding your accounts.")

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
