import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Monthly Outflows 🔮")

tab1, tab2, tab3, tab4 = st.tabs(["Debt", "Bills", "transportation", "Investment"])

with tab1:
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
            column_config={"Amount": st.column_config.NumberColumn(min_value=0, step=1, format="%d",),},
            hide_index=True,   
            num_rows="dynamic",
            width=400,
        )

        total = 0
        for key in edited_df["Amount"]:
            try: 
                total += key
            except:
                print("Nothing")
        st.write("Monthly debt payments total:", total, "€")

    with col2:
        if total > 0:
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

        total = 0
        for key in edited_df["Amount"]:
            try: 
                total += key
            except:
                print("Nothing")
        st.write("Monthly bills:", total, "€")

    with col2:
        if total > 0:
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

        total = 0
        for key in edited_df["Amount"]:
            try: 
                total += key
            except:
                print("Nothing")
        st.write("Estimated monthly transportation costs:", total, "€")

    with col2:
        if total > 0:
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
        total = 0
        for key in edited_df["Amount"]:
            try: 
                total += key
            except:
                print("Nothing")
        st.write("Monthly investments:", total, "€")

    with col2:
        if total > 0:
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
