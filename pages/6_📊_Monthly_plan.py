import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# st.set_page_config(layout="wide")
st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Monthly Plan")

income = 2500
st.write("Income:", 2500)

col1, col2 = st.columns([1, 1], gap="small")

with col1:
    df = pd.DataFrame([
       {"Purpose": "Rent", "Amount": 1000, "Necessary": True},
       {"Purpose": "Bills", "Amount": 100, "Necessary": True},
       {"Purpose": "Transportation", "Amount": 50, "Necessary": True},
       {"Purpose": "Debt", "Amount": 20, "Necessary": True},
       {"Purpose": "Savings", "Amount": 250, "Necessary": False},
       {"Purpose": "Investments", "Amount": 100, "Necessary": False},
       {"Purpose": "Food & fun", "Amount": 500, "Necessary": True},
       {"Purpose": "Shopping", "Amount": 250, "Necessary": False},
       {"Purpose": "Traveling", "Amount": 250, "Necessary": False},
   ])
    edited_df = st.data_editor(df, num_rows="dynamic", hide_index=True)

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
    if total > 0:
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