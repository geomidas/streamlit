import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Monthly Investments")
st.markdown("💡 Automate funding your accounts.")

col1, col2 = st.columns([1, 1], gap="small")
with col1:
    df_investments = pd.DataFrame([
        {"Title": "Pension", "Amount": 200,},
        {"Title": "Shares", "Amount": 100,},
        {"Title": "Crypto", "Amount": 20,},
    ])
    edited_df = st.data_editor(df_investments, num_rows="dynamic")
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