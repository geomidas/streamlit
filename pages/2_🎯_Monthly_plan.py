import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# st.set_page_config(layout="wide")
st.set_page_config(layout="centered")

# Load variables
monthly_bills = st.session_state["monthly_bills"]
monthly_transportation = st.session_state["monthly_transportation"]
monthly_debt = st.session_state["monthly_debt"]
monthly_savings = st.session_state["monthly_savings"]
monthly_investments = st.session_state["monthly_investments"]

st.markdown("### Monthly Plan 🎯")
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

    total = 0
    for key in edited_df["Amount"]:
        try: 
            total += key
        except:
            print("Nothing")
    st.write('Sum:', total, "€")
    if total > income:
        st.write("⚠️ Your expenses are higher than your income.")

    total_necessary = 0
    account_funding = {}
    for item in range(len(edited_df)):
        if edited_df.iloc[item]["Necessary"]:
            total_necessary += edited_df.iloc[item]["Amount"]
    st.write('Sum of necessary expenses:', total_necessary, "€")

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