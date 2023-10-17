import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Monthly Debt Payments")
st.markdown("💡 Low interest payments are ok. Try to eliminate higher interest debt.")

col1, col2 = st.columns([2, 3], gap="small")

with col1:
    df = pd.DataFrame([
       {"Title": "Mortgage", "Amount": 0},
       {"Title": "Car loan", "Amount": 0},
       {"Title": "Loan", "Amount": 0},
       {"Title": "Credit card", "Amount": 0},
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
    st.metric("Monthly debt payments total (€):", total)

with col2:
    if total > 0:
        fig1, ax1 = plt.subplots()
        ax1.pie(
            edited_df["Amount"],
            labels = edited_df["Title"],
            autopct = '%.0d%%',
            pctdistance = 0.83,
            # textprops = {'size': 'medium'},
            # radius=1,
        )
        st.pyplot(fig1)
