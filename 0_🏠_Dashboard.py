import streamlit as st
import pandas as pd


# st.set_page_config(layout="centered")
st.set_page_config("PerFin", page_icon="💎")

st.markdown("### PerFin")

tab1, tab2, tab3, tab4 = st.tabs([
    "__⚙️ Settings__",
    "__💵 Tips__",
    "__💰 Income__",
    "__💸 Spending__",
])

with tab1:
    col1, col2, col3 = st.columns([1,1,1], gap="medium")
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

        price_update_method = st.selectbox(
            "Price update method:",
            help="Choose which price you would like to fetch for assets.",
            options=(
                "lastPrice",
                "previousClose",
                "fiftyDayAverage",
                "twoHundredDayAverage",
                "yearLow"
            ),
        )
        if "price_update_method" not in st.session_state:
            st.session_state["price_update_method"] = price_update_method

with tab2:  
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

with tab3:
    if 'income_data' not in st.session_state:
        income_data=pd.DataFrame({
            "Date": [],
            "Net income": [],
            "Health insurance": [],
            "Pension": [],
            "Bonus": []
        })
        st.session_state.income_data = income_data

    def add_df_form():
        row = pd.DataFrame({
            'Date': [st.session_state.input_incume_date],
            'Net income': [st.session_state.input_income_net],
            'Health insurance': [st.session_state.input_income_health],
            'Pension': [st.session_state.input_income_pension],
            'Bonus': [st.session_state.input_income_bonus],
        })
        st.session_state.income_data = pd.concat([st.session_state.income_data, row])

    with st.expander("ℹ️ Track your monthly income."):
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
            st.dataframe(income_averages, hide_index=True, width=720)

    new_income = st.form(key="new_income", clear_on_submit=False)
    with new_income:
        st.write("#### Add income data")
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

    st.write("##### All data")
    st.dataframe(st.session_state.income_data, hide_index=True, width=720)

with tab4:
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

    with st.expander("ℹ️ Track your monthly spending."):
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

    new_spend = st.form(key="new_spend", clear_on_submit=False)
    with new_spend:
        st.write("#### Add spending data")
        df_form_columns = st.columns(8)
        with df_form_columns[0]:
            st.date_input("Date", format="YYYY-MM-DD", key="input_spend_date")
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
