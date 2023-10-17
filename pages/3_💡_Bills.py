import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Monthly Bill Payments")
st.markdown("💡 Tip: Estimations are fine 🔮")

col1, col2 = st.columns([1, 1], gap="small")

with col1:
    df = pd.DataFrame([
       {"Title": "Mobile Phone", "Amount": 20},
       {"Title": "Internet", "Amount": 30},
       {"Title": "Electricity", "Amount": 38},
       {"Title": "Gas", "Amount": 30},
       {"Title": "iCloud", "Amount": 2},
       {"Title": "Netflix", "Amount": 6},
       {"Title": "Bins", "Amount": 10},
   ])
    edited_df = st.data_editor(df, num_rows="dynamic",)

    total = 0
    for key in edited_df["Amount"]:
        try: 
            total += key
        except:
            print("Nothing")
    st.metric("Monthly bills (€):", total)

with col2:
    if total > 0:
        fig1, ax1 = plt.subplots()
        ax1.pie(edited_df["Amount"], labels=edited_df["Title"])
        st.pyplot(fig1)
