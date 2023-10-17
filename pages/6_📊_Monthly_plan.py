import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.markdown("# Perfin")
st.markdown("### Monthly Plan")

col1, col2 = st.columns([3, 3], gap="small")

with col1:
    st.write("Income:", 2500)
    df = pd.DataFrame([
       {"Purpose": "Rent", "Amount": 1000, "Account": "AIB", "Necessary": True},
       {"Purpose": "Bills", "Amount": 100, "Account": "AIB", "Necessary": True},
       {"Purpose": "Transportation", "Amount": 50, "Account": "AIB", "Necessary": True},
       {"Purpose": "Debt", "Amount": 0, "Account": "AIB", "Necessary": True},
       {"Purpose": "Savings", "Amount": 250, "Account": "AIB", "Necessary": False},
       {"Purpose": "Investments", "Amount": 100, "Account": "AIB", "Necessary": False},
       {"Purpose": "Food & fun", "Amount": 500, "Account": "Revolut", "Necessary": True},
       {"Purpose": "Shopping", "Amount": 250, "Account": "Revolut", "Necessary": False},
       {"Purpose": "Traveling", "Amount": 250, "Account": "Revolut", "Necessary": False},
   ])
    edited_df = st.data_editor(df, num_rows="dynamic", hide_index=True)

    total = 0
    for key in edited_df["Amount"]:
        try: 
            total += key
        except:
            print("Nothing")
    st.write('Sum:', total, "€")

    total_necessary = 0
    account_funding = {}
    for item in range(len(edited_df)):
        if edited_df.iloc[item]["Necessary"]:
            total_necessary += edited_df.iloc[item]["Amount"]
        # Breakdown account funding
        acc = edited_df.iloc[item]["Account"]
        if acc not in account_funding:
            account_funding[acc] = edited_df.iloc[item]["Amount"]
        else:
            account_funding[acc] += edited_df.iloc[item]["Amount"]
    st.write('Sum of necessary expenses:', total_necessary, "€")
    st.markdown("Monthly account funding:")
    for acc_name in account_funding:
        st.write("-", acc_name + ":", account_funding[acc_name])

with col2:
    if total > 0:
        st.markdown("Chart")
        fig1, ax1 = plt.subplots()
        ax1.pie(
            edited_df["Amount"],
            labels = edited_df["Purpose"],
            autopct = '%.0d%%',
            pctdistance = 0.83,
            # textprops = {'size': 'medium'},
            # radius=1,
        )
        st.pyplot(fig1)
