import streamlit as st
import pandas as pd


# st.set_page_config(layout="centered")


st.markdown("# Perfin")
st.markdown("### Dashboard")

tab1, tab2 = st.tabs(["⚙️ __Settings__", "💡 __Tips__"])

with tab1:
  st.markdown("### Settings")
  col1, col2 = st.columns([1, 1], gap="medium")

  with col1:
    st.markdown("#### Global")
    selected_currency=st.selectbox("Currency:", options=("EUR","GBP","USD"))
    if "selected_currency" not in st.session_state:
        st.session_state["selected_currency"] = selected_currency
    if selected_currency == "EUR":
        curr_symbol = "€"
    elif selected_currency == "GBP":
        curr_symbol = "£"
    elif selected_currency == "GBP":
        curr_symbol = "$"
    else:
        curr_symbol = selected_currency
    st.write("Symbol:", curr_symbol)
    if "curr_symbol" not in st.session_state:
        st.session_state["curr_symbol"] = curr_symbol
    # st.markdown("---")

    st.markdown("#### Assets")
    price_update_method = st.selectbox(
        "Price update method:",
        help="Choose which price you would like to fetch for assets.",
        options=(
            "lastPrice",
            "previousClose",
            "fiftyDayAverage",
            "twoHundredDayAverage",
            "yearLow"
        ),
    )
    if "price_update_method" not in st.session_state:
      st.session_state["price_update_method"] = price_update_method

    cgt_base=st.number_input(
        "Capital Gains Tax (%):",
        min_value = 0,
        max_value = 100,
        value = 33,
        format = "%d",
    )
    cgt = cgt_base/100
    if "cgt" not in st.session_state:
      st.session_state["cgt"] = cgt
    # st.markdown("---")

with tab2:
  col1, col2 = st.columns([1, 1], gap="medium")

  with col1:
    st.markdown("### Tips")
    st.markdown("""
    - Update this app at the end of every month :sparkles:
    - Review your allocation in 
      - [Debt payments](/Monthly_Outflows)
      - [Bills](/Monthly_Outflows)
      - [Tansportation](/Monthly_Outflows)
      - [Investments](/Monthly_Outflows)
      - [Savings](/Monthly_plan) (in the Monthly Plan)
    - Add this month's
      - [Income](/Income)
      - [Spending](/Spending)
    - Done! :tada:
    """)
