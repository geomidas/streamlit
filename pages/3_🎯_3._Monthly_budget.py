import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from numpy import isnan
import locale

st.set_page_config("PerFin", page_icon="💎")
st.markdown("### Monthly budget")

if 'user_info' not in st.session_state:
    st.write("Please login: https://perfin.streamlit.app")
else:
    locale.setlocale( locale.LC_ALL, 'en_US' )
    def curr_fmt(val):
        return locale.currency(val, symbol=False, grouping=True)

    # Load variables
    curr_symbol = st.session_state["curr_symbol"]
    if "last_net_income" in st.session_state:
        last_net_income = st.session_state.last_net_income
    else:
        last_net_income = 0

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "__🎯 Budget__",
        "__⚡ Bills__",
        "__🏦 Debt__",
        "__🐷 Savings__",
        "__🚀 Investments__",
        "__🍕 Food + Fun__",
        "__🛍️ Shopping__",
        "__✈️ Travel__",
    ])

    with tab2:
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            df_bills = pd.DataFrame([
               {"Title": "Rent", "Amount": 900},
               {"Title": "Mobile Phone", "Amount": 20},
               {"Title": "Internet", "Amount": 30},
               {"Title": "Electricity", "Amount": 40},
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
            st.info("Monthly debt payments: __" + curr_symbol + curr_fmt(monthly_debt) + "__")
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

    with tab4:
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

    with tab5:
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
    with tab6:
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            df_food = pd.DataFrame([
                {"Title": "Groceries", "Amount": 400,},
                {"Title": "Drinks", "Amount": 100,},
                {"Title": "Other", "Amount": 100,},
            ])
            edited_df_food = st.data_editor(df_food, num_rows="dynamic", use_container_width=True)
            monthly_food = 0
            for key in edited_df_food["Amount"]:
                if not isnan(key):
                    monthly_food += key
            st.info("Monthly: __" + curr_symbol + curr_fmt(monthly_food) + "__")
            st.session_state["monthly_food"] = monthly_food

        with col2:
            if len(edited_df_food["Amount"]) > 1 and monthly_food > 0 and edited_df_food["Amount"].isnull().values.any() == False:
                fig1, ax1 = plt.subplots()
                ax1.pie(
                    edited_df_food["Amount"],
                    labels=edited_df_food["Title"],
                    autopct='%.0d%%',
                    pctdistance=0.83,
                    counterclock=False,
                    startangle=90,
                )
                st.pyplot(fig1)

    with tab7:
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            df_shop = pd.DataFrame([
                {"Title": "Clothes", "Amount": 50,},
                {"Title": "Gifts", "Amount": 50,},
                {"Title": "Electronics", "Amount": 100,},
                {"Title": "Other", "Amount": 100,},
            ])
            edited_df_shop = st.data_editor(df_shop, num_rows="dynamic", use_container_width=True)
            monthly_shop = 0
            for key in edited_df_shop["Amount"]:
                if not isnan(key):
                    monthly_shop += key
            st.info("Monthly: __" + curr_symbol + curr_fmt(monthly_shop) + "__")
            st.session_state["monthly_shop"] = monthly_shop

        with col2:
            if len(edited_df_shop["Amount"]) > 1 and monthly_shop > 0 and edited_df_shop["Amount"].isnull().values.any() == False:
                fig1, ax1 = plt.subplots()
                ax1.pie(
                    edited_df_shop["Amount"],
                    labels=edited_df_shop["Title"],
                    autopct='%.0d%%',
                    pctdistance=0.83,
                    counterclock=False,
                    startangle=90,
                )
                st.pyplot(fig1)

    with tab8:
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            df_travel = pd.DataFrame([
                {"Title": "Flights", "Amount": 100,},
                {"Title": "Accomodation", "Amount": 100,},
            ])
            edited_df_travel = st.data_editor(df_travel, num_rows="dynamic", use_container_width=True)
            monthly_travel = 0
            for key in edited_df_travel["Amount"]:
                if not isnan(key):
                    monthly_travel += key
            st.info("Monthly: __" + curr_symbol + curr_fmt(monthly_travel) + "__")
            st.session_state["monthly_travel"] = monthly_travel

        with col2:
            if len(edited_df_travel["Amount"]) > 1 and monthly_travel > 0 and edited_df_travel["Amount"].isnull().values.any() == False:
                fig1, ax1 = plt.subplots()
                ax1.pie(
                    edited_df_travel["Amount"],
                    labels=edited_df_travel["Title"],
                    autopct='%.0d%%',
                    pctdistance=0.83,
                    counterclock=False,
                    startangle=90,
                )
                st.pyplot(fig1)

    with tab1:
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            df = pd.DataFrame([
                {"Purpose": "Bills", "Amount": monthly_bills, "Necessary": True},
                {"Purpose": "Debt", "Amount": monthly_debt, "Necessary": True},
                {"Purpose": "Savings", "Amount": monthly_savings, "Necessary": False},
                {"Purpose": "Investments", "Amount": monthly_investments, "Necessary": False},
                {"Purpose": "Food & fun", "Amount": monthly_food, "Necessary": True},
                {"Purpose": "Shopping", "Amount": 250, "Necessary": False},
                {"Purpose": "Traveling", "Amount": 250, "Necessary": False},
            ])
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                disabled=["Purpose", "Amount"],
            )

            total_necessary = 0
            account_funding = {}
            for item in range(len(edited_df)):
                if edited_df.iloc[item]["Necessary"]:
                    total_necessary += edited_df.iloc[item]["Amount"]
            st.info("Necessary outflows: __" + curr_symbol + str(curr_fmt(total_necessary)) + "__")
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
            st.warning(body="Your outflows are higher than your income.\n\nLast income: __" + curr_symbol + curr_fmt(last_net_income) + "__", icon="⚠️")
