import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from numpy import isnan

st.set_page_config(layout="centered")

# Load variables
curr_symbol = st.session_state["curr_symbol"]

st.markdown("# Perfin")
st.markdown("### Monthly Outflows 🔮")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚡ __Bills__", "🚌 __Transportation__", "🏦 __Debt__", "🐷 __Savings__", "🚀 __Investments__"])

with tab1:
    st.markdown("### Monthly Bill Payments")
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("💡 Tip: Estimations are fine 🔮")
        df = pd.DataFrame([
           {"Title": "Mobile Phone", "Amount": 20},
           {"Title": "Internet", "Amount": 30},
           {"Title": "Electricity", "Amount": 38},
           {"Title": "Gas", "Amount": 30},
           {"Title": "iCloud", "Amount": 2},
           {"Title": "Netflix", "Amount": 6},
           {"Title": "Bins", "Amount": 10},
       ])
        edited_df = st.data_editor(df, num_rows="dynamic", width=400,)

        monthly_bills = 0
        for key in edited_df["Amount"]:
            if not isnan(key):
                monthly_bills += int(key)
        st.write("Monthly bills: €", monthly_bills)
        if "monthly_bills" not in st.session_state:
            st.session_state["monthly_bills"] = monthly_bills

    with col2:
        if len(edited_df["Amount"]) > 1 and monthly_bills > 0 and edited_df["Amount"].isnull().values.any() == False:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df["Amount"],
                labels=edited_df["Title"],
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

        df = pd.DataFrame([
           {"Title": "Bus", "Amount": 12},
           {"Title": "Taxi", "Amount": 25},
           {"Title": "Car Insurance", "Amount": 3},
           {"Title": "Dublin Bike", "Amount": 3},
       ])
        edited_df = st.data_editor(df, num_rows="dynamic", width=400,)

        monthly_transportation = 0
        for key in edited_df["Amount"]:
            if not isnan(key):
                monthly_transportation += key
        st.write("Estimated monthly transportation costs:", curr_symbol, monthly_transportation)
        if "monthly_transportation" not in st.session_state:
            st.session_state["monthly_transportation"] = monthly_transportation

    with col2:
        if len(edited_df["Amount"]) > 1 and monthly_transportation > 0 and edited_df["Amount"].isnull().values.any() == False:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df["Amount"],
                labels=edited_df["Title"],
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

        df = pd.DataFrame([
           {"Title": "Mortgage", "Amount": 2},
           {"Title": "Car loan", "Amount": 1},
           {"Title": "Loan", "Amount": 1},
           {"Title": "Credit card", "Amount": 1},
       ])
        edited_df = st.data_editor(
            df,
            width=400,
            hide_index=True,   
            num_rows="dynamic",
            column_config={
                "Amount": st.column_config.NumberColumn(
                    format=curr_symbol + "%d",
                    min_value=0,
                ),
            }
        )

        monthly_debt = 0
        for key in edited_df["Amount"]:
            if not isnan(key):
                monthly_debt += key
        st.write("Monthly debt payments total:", curr_symbol, monthly_debt)
        if "monthly_debt" not in st.session_state:
            st.session_state["monthly_debt"] = monthly_debt

    with col2:
        if len(edited_df["Amount"]) > 1 and monthly_debt > 0 and edited_df["Amount"].isnull().values.any() == False:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df["Amount"],
                labels=edited_df["Title"],
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

        df_investments = pd.DataFrame([
            {"Title": "Emergency Fund", "Amount": 0,},
            {"Title": "House Deposit", "Amount": 100,},
            {"Title": "Car", "Amount": 20,},
        ])
        edited_df = st.data_editor(df_investments, num_rows="dynamic", width=400)
        monthly_savings = 0
        for key in edited_df["Amount"]:
            if not isnan(key):
                monthly_savings += key
        st.write("Monthly savings:", curr_symbol, monthly_savings)
        if "monthly_savings" not in st.session_state:
            st.session_state["monthly_savings"] = monthly_savings

    with col2:
        if len(edited_df["Amount"]) > 1 and monthly_savings > 0 and edited_df["Amount"].isnull().values.any() == False:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df["Amount"],
                labels=edited_df["Title"],
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

        df_investments = pd.DataFrame([
            {"Title": "Pension", "Amount": 200,},
            {"Title": "Shares", "Amount": 100,},
            {"Title": "Crypto", "Amount": 20,},
        ])
        edited_df = st.data_editor(df_investments, num_rows="dynamic", width=400)
        monthly_investments = 0
        for key in edited_df["Amount"]:
            if not isnan(key):
                monthly_investments += key
        st.write("Monthly investments:", curr_symbol, monthly_investments)
        if "monthly_investments" not in st.session_state:
            st.session_state["monthly_investments"] = monthly_investments

    with col2:
        if len(edited_df["Amount"]) > 1 and monthly_investments > 0 and edited_df["Amount"].isnull().values.any() == False:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                edited_df["Amount"],
                labels=edited_df["Title"],
                autopct='%.0d%%',
                pctdistance=0.83,
                counterclock=False,
                startangle=90,
                # textprops = {'size': 'medium'},
            )
            st.pyplot(fig1)
