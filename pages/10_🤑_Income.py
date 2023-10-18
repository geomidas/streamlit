import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

st.markdown("# Perfin")
st.markdown("### Income")
st.markdown("Track your actual monthly income. This acts as a guide for setting more accurate values in Outflow.")

df = pd.DataFrame(
    [
       {"Month":"2023-01", "Gross":40000, "Tax":1000, "Health Ins.":100, "Net":2500, "Pension":100, "Bonus":0},
   ]
)
edited_df = st.data_editor(
    df,
    hide_index=True,   
    num_rows="dynamic",
)
