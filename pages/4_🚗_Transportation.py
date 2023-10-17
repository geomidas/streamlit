import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Monthly Transportation Costs")
st.markdown("💡 You can split any annual expenses in montly payments")

col1, col2 = st.columns([1, 1], gap="small")

with col1:
    df = pd.DataFrame([
       {"Title": "Bus", "Amount": 12},
       {"Title": "Taxi", "Amount": 25},
       {"Title": "Car Insurance", "Amount": 3},
       {"Title": "Dublin Bike", "Amount": 3},
   ])
    edited_df = st.data_editor(df, num_rows="dynamic",)

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