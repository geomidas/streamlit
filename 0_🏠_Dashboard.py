import pandas as pd 
import streamlit as st 
import yfinance as yf
from datetime import date

st.set_page_config(layout="centered")

st.markdown("# Perfin")

st.markdown("### Tips")
tips = """
- It is easier to update this app at the end of every month.
- Review your allocation in 
  - [Debt payments](/Debt)
  - [Bills](/Bills)
  - [Tansportation](/Transportation)
  - [Investments](/Investments)
  - [Savings](/Monthly_plan) (in the Monthly Plan)
- Add this month's
  - [Income](/Income)
  - [Spending](/Spending)
- You're all done! :tada:
"""
st.markdown(tips)
