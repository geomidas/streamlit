import streamlit as st
import auth_functions
import locale
import datetime
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import shared.functions as sf
from numpy import isnan
import firebase_admin
import json


# cred = firebase_admin.credentials.Certificate("perfin-db-firebase-adminsdk.json")
# ref = firebase_admin.db.reference("/", url=st.secrets['DB_URL'])
# data = {"UserID": {"testkey": "value"}}
# ref.set(data)

st.set_page_config("PerFin", page_icon="💰")
locale.setlocale( locale.LC_ALL, 'en_US' )

st.markdown("# Personal Finance")

# Not logged in -----------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    sf.login_box()

# Logged in --------------------------------------------------------------------------------------
else:
    tab1, tab2 = st.tabs([
        "__⚙️ Account__",
        "__ℹ️ Info__",
    ])

    with tab1:
        st.write("#### Account")
        col1, col2, col3 = st.columns([4,3,4], gap="medium")
        with col1:
            st.info(
                "__Email:__ `" + st.session_state.user_info["email"] + "`\n\n" + 
                "__Verified:__ `" + str(st.session_state.user_info["emailVerified"]) + "`"
            )
        with col2:
            # Sign out
            st.write("Sign out:")
            st.button(label='Sign Out',on_click=auth_functions.sign_out,type='primary')
        with col3:
            # Delete Account
            st.write('Delete account:')
            password = st.text_input(label='Confirm your password',type='password')
            st.button(label='Delete Account',on_click=auth_functions.delete_account,args=[password],type='primary')

        st.write("#### Settings")
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
            if "curr_symbol" not in st.session_state:
                st.session_state["curr_symbol"] = curr_symbol
        with col2:
            cgt_base=st.number_input(
                "Capital Gains Tax (%):",
                min_value = 0,
                max_value = 100,
                value = 33,
                format = "%d",
            )
            cgt = cgt_base/100
            if "cgt" not in st.session_state:
                st.session_state["cgt"] = cgt

    with tab2:
        st.write("""
            - Tracking Income & Expenses
            - Budgeting
            - Tracking Asset Value
            - Estimating Financial Freedom
        """)
        st.image("https://www.theglobeandmail.com/files/dev/www/cache-long/arc-site-team/for-you-package/banner-desktop-900.png")

        st.write("### Path to Financial Independence")
        st.graphviz_chart("""
            digraph {
                "Track Expenses" -> "Emergency Fund"
                "Emergency Fund" -> "Pay bad debt"
                "Pay bad debt" -> "Save"
                "Pay bad debt" -> "Pension"
                "Pay bad debt" -> "Extra Investments"
                "Pension" -> "FI"
                "Extra Investments" -> "FI"
            }
            """,
            use_container_width=True
        )
        st.write("#### Useful resources")
        st.write("Evaluate your plan:\n\n", "- Rich, broke or dead? https://engaging-data.com/will-money-last-retire-early")


    st.markdown("# Monthly inflows and outflows")

    tab1, tab2 = st.tabs([
        "__💰 Inflows__",
        "__💸 Outflows__",
    ])

    with tab1:
        def init_income_data():
            income_data=pd.DataFrame({
                "Date": [],
                "Net income": [],
                "Health insurance": [],
                "Pension": [],
                "Bonus": []
            })
            st.session_state.income_data = income_data

        if 'income_data' not in st.session_state:
            init_income_data()

        def add_df_form():
            row = pd.DataFrame({
                'Date': [st.session_state.input_income_date],
                'Net income': [st.session_state.input_income_net],
                'Health insurance': [st.session_state.input_income_health],
                'Pension': [st.session_state.input_income_pension],
                'Bonus': [st.session_state.input_income_bonus],
            })
            st.session_state.income_data = pd.concat([st.session_state.income_data, row])

        new_income = st.form(key="new_income", clear_on_submit=False)
        with new_income:
            st.write("#### Add income data")
            df_form_columns = st.columns(5)
            with df_form_columns[0]:
                st.date_input("Date", format="YYYY-MM-DD", key="input_income_date")
            with df_form_columns[1]:
                st.number_input("Net income", min_value=0, step=1, key="input_income_net")
            with df_form_columns[2]:
                st.number_input("Health insurance", min_value=0, step=1, key="input_income_health")
            with df_form_columns[3]:
                st.number_input("Pension", min_value=0, step=1, key="input_income_pension")
            with df_form_columns[4]:
                st.number_input("Bonus", min_value=0, step=1, key="input_income_bonus")

            submitted = st.form_submit_button("Submit", help="Adds the data to the table below.", on_click=add_df_form, type='primary')
            if submitted:
                st.toast("Updated Income table 💰", icon="🎉")

        if len(st.session_state.income_data["Date"]) < 1:
            add_sample_income_data = st.button("Add sample income data", help="Imports sample data. Removes any existing data.")
            st.write("Current bug with the above button. Double-click it.")
            if add_sample_income_data:
                st.session_state.income_data = pd.DataFrame({
                    'Date': ["2023-01-01", "2023-02-01", "2023-03-01", "2023-04-01", "2023-05-01", "2023-06-01", "2023-07-01", "2023-08-01"],
                    'Net income': [2000, 2000, 1900, 1900, 2000, 2100, 2100, 2200],
                    'Health insurance': [0, 100, 100, 100, 110, 110, 110, 110],
                    'Pension': [0, 0, 0, 120, 240, 240, 240, 200],
                    'Bonus': [0, 0, 0, 500, 0, 0, 200, 0],
                })
                st.toast("Imported sample data", icon="🎉")
        else:
            income_chart_data = pd.DataFrame(
                st.session_state.income_data,
                columns=["Date", "Net income", "Health insurance", "Pension", "Bonus"]
            )
            with st.expander("Income Chart", expanded=True):
                st.area_chart(
                    income_chart_data,
                    x="Date",
                    # y=["Pension", "Net income", "Health insurance", "Bonus"],
                    # color=["#8ec127", "#00aedb", "#a200ff", "#f47835"]
                )

            with st.expander("All income data"):
                st.dataframe(st.session_state.income_data, hide_index=True, use_container_width=True)

                delete_income_data = st.button("Delete income data", help="Delete all income data.")
                if delete_income_data:
                    init_income_data()
                    st.toast("Deleted income data", icon="🎉")

            # Store last income for use in budgeting
            if st.session_state.income_data.tail(1)["Net income"].any():
                last_net_income = int(st.session_state.income_data.tail(1)["Net income"].item())
                st.session_state.last_net_income = last_net_income

            with st.expander("Monthly Average"):
                st.write("This acts as a guide for setting more accurate values in Monthly Outflows.")
                if len(st.session_state.income_data) > 1:
                    st.write("##### Average")
                    for key in st.session_state.income_data:
                        if key in "Date":
                            pass
                        elif key in "Net income":
                            values_list = st.session_state.income_data[key]
                            avg_net_income = sum(values_list)/len(values_list)
                        elif key in "Health insurance":
                            values_list = st.session_state.income_data[key]
                            avg_health_ins = sum(values_list)/len(values_list)
                        elif key in "Pension":
                            values_list = st.session_state.income_data[key]
                            avg_income_pension = sum(values_list)/len(values_list)
                        elif key in "Bonus":
                            values_list = st.session_state.income_data[key]
                            avg_income_bonus = sum(values_list)/len(values_list)
                        else:
                            pass
                    income_averages = pd.DataFrame({
                        'Net income': [avg_net_income],
                        'Health insurance': [avg_health_ins],
                        'Pension': [avg_income_pension],
                        'Bonus': [avg_income_bonus],
                    })
                    st.dataframe(income_averages, hide_index=True, use_container_width=True)

    with tab2:
        def init_spend_data():
            spend_data=pd.DataFrame({
                "Date": [],
                "Bills": [],
                "Pension": [],
                "Food + Fun": [],
                "Investments": [],
                "Shopping": [],
                "Travel": [],
            })
            st.session_state.spend_data = spend_data

        if 'spend_data' not in st.session_state:
            init_spend_data()

        def add_df_form():
            row = pd.DataFrame({
                "Date": [st.session_state.input_spend_date],
                "Bills": [st.session_state.input_spend_bills],
                "Pension": [st.session_state.input_spend_pension],
                "Food + Fun": [st.session_state.input_spend_food],
                "Investments": [st.session_state.input_spend_invest],
                "Shopping": [st.session_state.input_spend_shop],
                "Travel": [st.session_state.input_spend_travel],
            })
            st.session_state.spend_data = pd.concat([st.session_state.spend_data, row])

        new_spend = st.form(key="new_spend", clear_on_submit=False)
        with new_spend:
            st.write("#### Add spending data")
            df_form_columns = st.columns(7)
            with df_form_columns[0]:
                st.date_input("Date", format="YYYY-MM-DD", key="input_spend_date")
            with df_form_columns[1]:
                st.number_input("Bills", min_value=0, step=1, key="input_spend_bills")
            with df_form_columns[2]:
                st.number_input("Pension", min_value=0, step=1, key="input_spend_pension")
            with df_form_columns[3]:
                st.number_input("Food + Fun", min_value=0, step=1, key="input_spend_food")
            with df_form_columns[4]:
                st.number_input("Investments", min_value=0, step=1, key="input_spend_invest")
            with df_form_columns[5]:
                st.number_input("Shopping", min_value=0, step=1, key="input_spend_shop")
            with df_form_columns[6]:
                st.number_input("Travel", min_value=0, step=1, key="input_spend_travel")

            submitted = st.form_submit_button("Submit", help="Adds the data to the table below.", on_click=add_df_form, type='primary')
            if submitted:
                st.toast("Updated Spending 💸", icon="🎉")

        if len(st.session_state.spend_data["Date"]) < 1:
            add_sample_spend_data = st.button("Add sample spending data", help="Imports sample data. Removes any existing data.")
            if add_sample_spend_data:
                st.session_state.spend_data = pd.DataFrame({
                    "Date": ["2023-01-01", "2023-02-01", "2023-03-01", "2023-04-01", "2023-05-01", "2023-06-01", "2023-07-01", "2023-08-01", "2023-09-01"],
                    "Bills": [800,800,800,800,800,900,900,900,900],
                    "Pension": [100,100,100,100,100,120,120,120,120],
                    "Food + Fun": [400,430,542,610,490,580,550,520,500],
                    "Investments": [0,0,100,100,150,100,130,100,100],
                    "Shopping": [50,80,100,10,250,30,130,40,0],
                    "Travel": [0,0,0,130,150,0,0,90,100],
                })
                st.toast("Imported sample data", icon="🎉")
        else:
            spend_chart_data = pd.DataFrame(
                st.session_state.spend_data,
                columns=["Date", "Bills", "Pension", "Food+Fun", "Investments", "Shopping", "Travel",],
            )
            with st.expander(label="Spending Chart", expanded=True):
                st.area_chart(
                    spend_chart_data,
                    use_container_width=True,
                    x="Date",
                    # y=["Pension", "Bills", "Food+Fun", "Investments", "Shopping", "Travel"],
                    # color=["#ff6961", "#f10ff8", "#f1aff8", "#d7740d", "#08cad1", "#0d70d7"],
                )

            with st.expander("All spending data"):
                st.dataframe(st.session_state.spend_data, hide_index=True, width=720)

                delete_spend_data = st.button("Delete spending data", help="Delete all spending data.")
                if delete_spend_data:
                    init_spend_data()
                    st.toast("Deleted spending data", icon="🎉")

            with st.expander("Monthly Average"):
                if len(st.session_state.spend_data) > 1:
                    for key in st.session_state.spend_data:
                        if key in "Date":
                            pass
                        elif key in "Bills":
                            values_list = st.session_state.spend_data[key]
                            avg_spend_bills = sum(values_list)/len(values_list)
                        elif key in "Pension":
                            values_list = st.session_state.spend_data[key]
                            avg_spend_pension = sum(values_list)/len(values_list)
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
                        "Bills": [avg_spend_bills],
                        "Pension": [avg_spend_pension],
                        "Food + Fun": [avg_spend_food],
                        "Investments": [avg_spend_invest],
                        "Shopping": [avg_spend_shop],
                        "Travel": [avg_spend_travel],
                    })
                    st.dataframe(spend_averages, hide_index=True, use_container_width=True)


    st.markdown("# Monthly budget")

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


    st.markdown("# Assets")

    def curr_fmt(val):
        return locale.currency(val, symbol=False, grouping=True)

    def get_share_price(ticker):
        return yf.Ticker(ticker).basic_info["lastPrice"]

    def get_crypto_price(ticker, selected_currency):
        return yf.Ticker(ticker + "-" + selected_currency).basic_info["lastPrice"]

    # Load Settings
    selected_currency = st.session_state["selected_currency"]
    curr_symbol = st.session_state["curr_symbol"]
    cgt = st.session_state["cgt"]
    necessary_expenses = st.session_state["necessary_expenses"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "__⚙️ Dashboard__",
        "__💵 Cash &nbsp; &nbsp;__",
        "__🏛️ Shares &nbsp;__",
        "__🪙 Cryptocurrency__",
    ])

    with tab2:
        st.markdown("Cash and cash equivalents:")
        df_cash = pd.DataFrame([
            {"Cash": "Under the mattress", "Net": 0},
            {"Cash": "Savings", "Net": 1000},
        ])
        edited_df_cash = st.data_editor(df_cash, width=380, num_rows="dynamic")
        assets_cash = 0
        for key in edited_df_cash["Net"]:
            try:
                assets_cash += key
            except:
                print("Assets: No cash")
        st.info('Cash Sum: __' + curr_symbol + curr_fmt(assets_cash) + "__")
        st.session_state["assets_cash"] = assets_cash

        st.write("#### Emergency Fund")
        st.info("Months of all necessary expenses covered: __" + str(int(assets_cash / necessary_expenses)) + "__")

    with tab3:
        st.markdown("Add any shares you own:")
        df_shares = pd.DataFrame({"Title": ["Tesla"], "Ticker": ["TSLA"], "Count": [100.0], "Avg Cost": [200.0]})
        edited_df_shares = st.data_editor(df_shares, use_container_width=True, num_rows="dynamic")

        assets_shares_net = 0
        if sum(edited_df_shares["Count"]) > 0 and not edited_df_shares.isnull().values.any():
            st.write("##### Value")
            df_shares_value = pd.DataFrame({"Title": [], "Net": [], "Gross": [], "Tax": [], "Price": [], "Total Cost": []})
            for row in range(len(edited_df_shares)):
                row_title = edited_df_shares.T[row]["Title"]
                row_ticker = edited_df_shares.T[row]["Ticker"]
                row_count = edited_df_shares.T[row]["Count"]
                row_avg_cost = edited_df_shares.T[row]["Avg Cost"]
                row_cost = row_count * row_avg_cost
                row_price = get_share_price(row_ticker)
                row_gross = int(row_count * row_price)
                row_profit = int(row_gross - row_cost)
                row_tax = int(row_gross * cgt)
                row_net = int(row_gross - row_tax)

                new_row = pd.DataFrame({
                    "Title": [row_title],
                    "Net": [row_net],
                    "Gross": [row_gross],
                    "Tax": [row_tax],
                    "Price": [row_price],
                    "Total Cost": [row_cost],
                })
                df_shares_value = pd.concat([df_shares_value, new_row])

            st.dataframe(df_shares_value, hide_index=True, use_container_width=True)
            for key in df_shares_value["Net"]:
                try:
                    assets_shares_net += key
                except:
                    print("Assets: No shares")
            st.info('Shares Net Sum: __' + curr_symbol + curr_fmt(assets_shares_net) + "__")

        st.session_state["assets_shares_net"] = assets_shares_net

    with tab4:
        ticker_btc = "BTC-" + selected_currency
        st.markdown("Crypto you hodl:")
        df_crypto = pd.DataFrame({"Title": ["Bitcoin"], "Ticker": ["BTC"], "Count": [0.1], "Avg Cost": [1000.0]})
        edited_df_crypto = st.data_editor(df_crypto, use_container_width=True, num_rows="dynamic")

        assets_crypto_net = 0
        if sum(edited_df_crypto["Count"]) > 0 and not edited_df_crypto.isnull().values.any():
            st.write("##### Value")
            df_crypto_value = pd.DataFrame({"Title": [], "Net": [], "Gross": [], "Tax": [], "Price": [], "Total Cost": []})
            for row in range(len(edited_df_crypto)):
                row_title = edited_df_crypto.T[row]["Title"]
                row_ticker = edited_df_crypto.T[row]["Ticker"]
                row_count = edited_df_crypto.T[row]["Count"]
                row_avg_cost = edited_df_crypto.T[row]["Avg Cost"]
                row_cost = row_count * row_avg_cost
                row_price = get_crypto_price(row_ticker, selected_currency)
                row_gross = int(row_count * row_price)
                row_profit = int(row_gross - row_cost)
                row_tax = int(row_profit * cgt)
                row_net = int(row_gross - row_tax)

                new_row = pd.DataFrame({
                    "Title": [row_title],
                    "Net": [row_net],
                    "Gross": [row_gross],
                    "Tax": [row_tax],
                    "Price": [row_price],
                    "Total Cost": [row_cost],
                })
                df_crypto_value = pd.concat([df_crypto_value, new_row])

            st.dataframe(df_crypto_value, hide_index=True, use_container_width=True)
            for key in df_crypto_value["Net"]:
                try:
                    assets_crypto_net += key
                except:
                    print("Assets > Crypto > Value calc error")
            st.info("Crypto Net Sum: __" + curr_symbol + curr_fmt(assets_crypto_net) + "__")

        st.session_state["assets_crypto_net"] = assets_crypto_net

    with tab1:

        if assets_cash != 0 and assets_shares_net != 0:
            col1, col2, col3 = st.columns([3, 3, 4], gap="medium")
            with col1:
                st.write("##### Net Worth")
                assets_net_investments = int(assets_shares_net + assets_crypto_net)
                st.session_state.assets_net_investments = assets_net_investments
                assets_net_worth = int(assets_cash) + assets_net_investments
                st.info("Current Net Worth: __" + curr_symbol + curr_fmt(assets_net_worth) + "__")
                st.info("Net Investments: __" + curr_symbol + curr_fmt(assets_net_investments) + "__")
                st.session_state["assets_net_worth"] = assets_net_worth
            with col2:
                st.markdown("##### Allocation")
                st.info("Cash: __" + curr_symbol + curr_fmt(assets_cash) + "__")
                st.info("Net Shares: __" + curr_symbol + curr_fmt(assets_shares_net) + "__")
                st.info("Net Crypto: __" + curr_symbol + curr_fmt(assets_crypto_net) + "__")
            with col3:
                fig1, ax1 = plt.subplots()
                ax1.pie(
                    [assets_cash, assets_shares_net, assets_crypto_net],
                    labels=["Cash", "Shares", "Crypto"],
                    autopct='%.0d%%',
                    pctdistance=0.83,
                    counterclock=False,
                    startangle=45,
                )
                st.pyplot(fig1)

        st.write("##### Net Worth over time")
        df_net_worth = pd.DataFrame([
            {"Month": "2023-01", "Net Worth": 100, "Net Investments": 50, "Net Shares": 50, "Net Crypto": 30},
            {"Month": "2023-02", "Net Worth": 150, "Net Investments": 50, "Net Shares": 50, "Net Crypto": 30},
            {"Month": "2023-03", "Net Worth": 200, "Net Investments": 150, "Net Shares": 50, "Net Crypto": 30},
            {"Month": "2023-04", "Net Worth": 200, "Net Investments": 150, "Net Shares": 50, "Net Crypto": 30},
            {"Month": "2023-05", "Net Worth": 250, "Net Investments": 150, "Net Shares": 50, "Net Crypto": 30},
            {"Month": "2023-06", "Net Worth": 400, "Net Investments": 250, "Net Shares": 150, "Net Crypto": 30},
            {"Month": "2023-07", "Net Worth": 350, "Net Investments": 150, "Net Shares": 150, "Net Crypto": 30},
            {"Month": "2023-08", "Net Worth": 500, "Net Investments": 350, "Net Shares": 150, "Net Crypto": 30},
            {"Month": "2023-09", "Net Worth": 500, "Net Investments": 350, "Net Shares": 150, "Net Crypto": 30},
            {"Month": "2023-10", "Net Worth": 600, "Net Investments": 450, "Net Shares": 200, "Net Crypto": 30},
            {"Month": "2023-11", "Net Worth": 500, "Net Investments": 350, "Net Shares": 100, "Net Crypto": 30},
            {"Month": "2023-12", "Net Worth": 700, "Net Investments": 450, "Net Shares": 200, "Net Crypto": 30},
        ])
        with st.expander(label="Net Worth Data", expanded=False):
            edited_df = st.data_editor(df_net_worth, num_rows="dynamic")
        st.line_chart(df_net_worth, x="Month", height=420, use_container_width=True)


    st.markdown("# Financial Freedom / Retirement")

    def curr_fmt(val):
        return locale.currency(val, symbol=False, grouping=True)

    # Load variables
    curr_symbol = st.session_state["curr_symbol"]
    assets_cash = st.session_state["assets_cash"]
    assets_shares_net = st.session_state["assets_shares_net"]
    assets_crypto_net = st.session_state["assets_crypto_net"]
    assets_net_worth = st.session_state["assets_net_worth"]
    assets_net_investments = st.session_state["assets_net_investments"]
    necessary_expenses = st.session_state["necessary_expenses"]
    monthly_debt = st.session_state["monthly_debt"]

    col1, col2 = st.columns([1,1], gap="medium")
    with col1:
        retire_monthly_sal = st.number_input("Monthly budget in retirement (in " + curr_symbol + ")", min_value=0, value=2000)
    with col2:
        retire_wr_perc = st.number_input("Withrawal rate (%)", min_value=0.0, value=3.5)
        retire_wr = retire_wr_perc / 100
    retire_yearly_income = retire_monthly_sal * 12
    retire_target = retire_yearly_income*(1/retire_wr)
    st.info("You can retire when your Net investments reach __" + curr_symbol + curr_fmt(retire_target) + "__")
    # st.info("Your budget if you retired now:\n\n > Yearly: __" + curr_symbol + curr_fmt(assets_net_worth*retire_wr) + "__\n\n > Monthly: __" + curr_symbol + curr_fmt(assets_net_worth*retire_wr/12) + "__")
    st.write("#### Projected Net Worth of Investments")
    col1, col2 = st.columns([1,1], gap="medium")
    with col1:
        retire_rr_perc = st.number_input("Expected return rate (%)", min_value=0.0, value=8.0)
        retire_rr = retire_rr_perc / 100
        years_to_project = st.number_input("Years ahead to project", min_value=0, value=60)
    with col2:
        today = datetime.date.today()
        year = int(today.year)
        future_nw = pd.DataFrame(
            index=range(years_to_project),
            columns=["Year", "Projected Net Investments"]
        )
        year_counter = year
        assets_net_investments_compounder = assets_net_investments
        target_hit_date = "Never"
        for row in range(len(future_nw)):
            year_counter += 1
            future_nw.T[row]["Year"] = str(year_counter)
            assets_net_investments_compounder = assets_net_investments_compounder * (1.0 + retire_rr)
            future_nw.T[row]["Projected Net Investments"] = int(assets_net_investments_compounder)
            if assets_net_investments_compounder >= retire_target:
                target_hit_date = str(year_counter)
                break
        future_nw = future_nw.dropna()
        st.dataframe(future_nw, hide_index=True, height=296, use_container_width=True)
    with col1:
        if target_hit_date != "Never":
            st.info("Year of retirement: __" + target_hit_date + "__")
            st.info("Years until retirement: __" + str(int(target_hit_date) - year) + "__")
        else:
            st.warning("You won't have enough investments in " + str(years_to_project) + " years")
    st.area_chart(future_nw, x="Year", y="Projected Net Investments", height=320)
    st.write("#### Current Financial Status")
    col1, col2 = st.columns([1,1], gap="medium")
    with col1:
        if assets_net_investments >= retire_monthly_sal * 600:
            st.info("__Financial Freedom__" + "\n\n" + "You have more money than you'll ever need.\n\nYou don't have to worry about money, even in economic downturns.")
        elif assets_net_investments >= retire_monthly_sal * 480:
            st.info("__Financial Independence__" + "\n\n" + "Your investment income or passive income is enough to cover your basic needs, you've achieved financial independence.\n\nA financially independent person can retire at any time without worrying about how to cover their costs of living, even if they may have to downsize their lifestyle a bit.")
        elif assets_net_investments >= retire_monthly_sal * 240:
            st.info("__Financial Security__" + "\n\n" + "You have eliminated your debt (or have enough assets to pay off all your debt) and could weather a period of unemployment without worry.\n\nAt this point, money is not just a safety net, but also a tool you can use to build the future you've been planning.\n\nAt this point, you may consider investing in other assets besides retirement accounts — a taxable account, rental real estate, or even your own small business.")
        elif assets_net_investments >= retire_monthly_sal * 120:
            st.info("__Barista FI__" + "\n\n" + "You are able to meet your financial obligations on your own.")
        elif assets_cash >= int(6 * necessary_expenses):
            st.info("__Financial Stability__" + "\n\n" + "You have an emergency fund of a few months expenses, repaid high-interest debt and are continuing to live within your means.\n\nWhile stability does not require you to be debt-free—as you may still have a mortgage, student loans, or even credit card debt, you'll have a savings buffer to ensure that you won't go into debt if you encounter an emergency or unexpected expense.")
        elif assets_cash >= 0:
            st.info("__Financial Solvency__" + "\n\n" + "You are able to meet your financial obligations on your own.")
        else:
            st.progress(0)
            st.info("__Financial Dependence__" + "\n\n" + "If you rely on a parent, a significant other, or someone else to pay your living expenses.\n\nThis stage starts from childhood.")
    with col2:
        retirement_progress = assets_net_investments/retire_target
        st.progress(retirement_progress, text="Retirement Progress")
        st.info("__" + curr_fmt(retirement_progress*100) + "%__ of the " + curr_symbol + curr_fmt(retire_target) + " needed.")
