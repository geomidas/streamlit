import streamlit as st
import pandas as pd
import pages.shared.functions as sf


st.set_page_config("PerFin", page_icon="💎")
st.markdown("### Monthly Inflows and Outflows")

if 'user_info' not in st.session_state:
    sf.login_box()
else:
    tab1, tab2 = st.tabs([
        "__💰 Income__",
        "__💸 Spending__",
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
