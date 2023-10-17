import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Monthly Debt Payments")
st.markdown("💡 Low interest payments are ok. Try to eliminate higher interest debt.")

col1, col2 = st.columns([1, 1], gap="small")

with col1:
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
