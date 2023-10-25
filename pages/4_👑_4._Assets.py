import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


def get_share_price(ticker):
    return yf.Ticker(ticker).basic_info["lastPrice"]

def get_crypto_price(ticker, selected_currency):
    return yf.Ticker(ticker + "-" + selected_currency).basic_info["lastPrice"]


# Load Settings
selected_currency = st.session_state["selected_currency"]
curr_symbol = st.session_state["curr_symbol"]
cgt = st.session_state["cgt"]
necessary_expenses = st.session_state["necessary_expenses"]

st.markdown("### Assets")
tab1, tab2, tab3, tab4 = st.tabs([
    "__⚙️ Dashboard__",
    "__💵 Cash &nbsp; &nbsp;__",
    "__🏛️ Shares &nbsp;__",
    "__🪙 Cryptocurrency__",
])

with tab2:
    st.markdown("Cash and cash equivalent:")
    df_cash = pd.DataFrame([
        {"Cash": "Under the mattress", "Net": 0},
        {"Cash": "Savings", "Net": 0},
    ])
    edited_df_cash = st.data_editor(df_cash, width=380, num_rows="dynamic")
    assets_cash = 0
    for key in edited_df_cash["Net"]:
        try:
            assets_cash += key
        except:
            print("Assets: No cash")
    st.write('Cash Sum:', curr_symbol, assets_cash)
    if "assets_cash" not in st.session_state:
        st.session_state["assets_cash"] = assets_cash

    st.write("#### Emergency Fund")
    st.write("Months of all necessary expenses covered:", int(assets_cash / necessary_expenses))

with tab3:
    st.markdown("Add any shares you own:")
    df_shares = pd.DataFrame({"Title": ["Tesla"], "Ticker": ["TSLA"], "Count": [0.0], "Avg Cost": [0.0]})
    edited_df_shares = st.data_editor(df_shares, width=720, num_rows="dynamic")
    
    assets_shares_net = 0
    if sum(edited_df_shares["Count"]) > 0 and not edited_df_shares.isnull().values.any():
        st.write("##### Value")
        df_shares_value = pd.DataFrame({"Title": [], "Net": [], "Gross": [], "Tax": [], "Price": [], "Total Cost": []})
        for row in range(len(edited_df_shares)):
            row_title = edited_df_shares.T[row]["Title"]
            row_ticker = edited_df_shares.T[row]["Ticker"]
            row_count = edited_df_shares.T[row]["Count"]
            row_avg_cost = edited_df_shares.T[row]["Avg Cost"]
            row_cost = row_count * row_avg_cost
            row_price = get_share_price(row_ticker)
            row_gross = int(row_count * row_price)
            row_profit = int(row_gross - row_cost)
            row_tax = int(row_gross * cgt)
            row_net = int(row_gross - row_tax)

            new_row = pd.DataFrame({
                "Title": [row_title],
                "Net": [row_net],
                "Gross": [row_gross],
                "Tax": [row_tax],
                "Price": [row_price],
                "Total Cost": [row_cost],
            })
            df_shares_value = pd.concat([df_shares_value, new_row])

        st.dataframe(df_shares_value, hide_index=True, width=720)
        for key in df_shares_value["Net"]:
            try:
                assets_shares_net += key
            except:
                print("Assets: No shares")
        st.write('Shares Net Sum:', curr_symbol, assets_shares_net)

    if "assets_shares_net" not in st.session_state:
        st.session_state["assets_shares_net"] = assets_shares_net

with tab4:
    ticker_btc = "BTC-" + selected_currency
    st.markdown("Crypto you hodl:")
    df_crypto = pd.DataFrame({"Title": ["Bitcoin"], "Ticker": ["BTC"], "Count": [0.0], "Avg Cost": [0.0]})
    edited_df_crypto = st.data_editor(df_crypto, width=720, num_rows="dynamic")

    assets_crypto_net = 0
    if sum(edited_df_crypto["Count"]) > 0 and not edited_df_crypto.isnull().values.any():
        st.write("##### Value")
        df_crypto_value = pd.DataFrame({"Title": [], "Net": [], "Gross": [], "Tax": [], "Price": [], "Total Cost": []})
        for row in range(len(edited_df_crypto)):
            row_title = edited_df_crypto.T[row]["Title"]
            row_ticker = edited_df_crypto.T[row]["Ticker"]
            row_count = edited_df_crypto.T[row]["Count"]
            row_avg_cost = edited_df_crypto.T[row]["Avg Cost"]
            row_cost = row_count * row_avg_cost
            row_price = get_crypto_price(row_ticker, selected_currency)
            row_gross = int(row_count * row_price)
            row_profit = int(row_gross - row_cost)
            row_tax = int(row_profit * cgt)
            row_net = int(row_gross - row_tax)

            new_row = pd.DataFrame({
                "Title": [row_title],
                "Net": [row_net],
                "Gross": [row_gross],
                "Tax": [row_tax],
                "Price": [row_price],
                "Total Cost": [row_cost],
            })
            df_crypto_value = pd.concat([df_crypto_value, new_row])

        st.dataframe(df_crypto_value, hide_index=True, width=720)
        for key in df_crypto_value["Net"]:
            try:
                assets_crypto_net += key
            except:
                print("Assets > Crypto > Value calc error")
        st.write("Crypto Net Sum:", curr_symbol, assets_crypto_net)

    if "assets_crypto_net" not in st.session_state:
        st.session_state["assets_crypto_net"] = assets_crypto_net

with tab1:
    assets_net_worth = int(assets_cash + assets_shares_net + assets_crypto_net)
    if "assets_net_worth" not in st.session_state:
        st.session_state["assets_net_worth"] = assets_net_worth
    st.write("Current Net Worth:", curr_symbol, assets_net_worth)

    st.markdown("##### Net Worth over time")
    col1, col2 = st.columns([1, 2], gap="medium")
    with col1:
        df_net_worth = pd.DataFrame([
            {"Month": "2023-01", "Net Worth": 100},
            {"Month": "2023-02", "Net Worth": 150},
            {"Month": "2023-03", "Net Worth": 200},
            {"Month": "2023-04", "Net Worth": 200},
            {"Month": "2023-05", "Net Worth": 250},
            {"Month": "2023-06", "Net Worth": 400},
            {"Month": "2023-07", "Net Worth": 350},
            {"Month": "2023-08", "Net Worth": 500},
            {"Month": "2023-09", "Net Worth": 500},
            {"Month": "2023-10", "Net Worth": 600},
            {"Month": "2023-11", "Net Worth": 500},
            {"Month": "2023-12", "Net Worth": 700},
        ])
        edited_df = st.data_editor(df_net_worth, num_rows="dynamic")
    with col2:
        st.line_chart(edited_df, x="Month", y="Net Worth")
    st.divider()

    st.markdown("##### Allocation")
    st.write("Add pie")
    