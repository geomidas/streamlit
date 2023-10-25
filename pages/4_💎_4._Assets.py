import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(layout="centered")

def get_price(ticker):
    return yf.Ticker(ticker).basic_info["lastPrice"]

# Load Settings
selected_currency = st.session_state["selected_currency"]
curr_symbol = st.session_state["curr_symbol"]
cgt = st.session_state["cgt"]

st.markdown("### Assets 💎")
tab1, tab2, tab3, tab4 = st.tabs([
    "__⚙️ Dashboard__",
    "__💵 Cash &nbsp; &nbsp;__",
    "__🏛️ Shares &nbsp;__",
    "__🪙 Cryptocurrency__",
])

with tab2:
    st.markdown("Cash and cash equivalent:")
    df_cash = pd.DataFrame([
        {"Cash": "Under the mattress", "Net": 100},
        {"Cash": "Savings", "Net": 1000},
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
    st.write("Months of all necessary expenses covered:", 2)

with tab3:
    st.markdown("Add shares in public companies in your portfolio:")
    df_shares = pd.DataFrame([
        {"Title": "Tesla", "Ticker": "TSLA", "Count": 2, "Avg Cost": 200},
        {"Title": "Apple", "Ticker": "AAPL", "Count": 2, "Avg Cost": 200},
    ])
    edited_df_shares = st.data_editor(df_shares, width=720, num_rows="dynamic")

    st.write("##### Status")
    df_shares_value = pd.DataFrame({
        "Title": [],
        "Net": [],
        "Gross": [], 
        "Tax": [],
        "Price": [],
        "Total Cost": [],
    })
    for row in range(len(edited_df_shares)):
        title = edited_df_shares.T[row]["Title"]
        ticker = edited_df_shares.T[row]["Ticker"]
        count = edited_df_shares.T[row]["Count"]
        avg_cost = edited_df_shares.T[row]["Avg Cost"]
        cost = count * avg_cost
        price = get_price(ticker)
        gross = int(count * price)
        tax = int(gross * cgt)
        net = int(gross - tax)
        new_row = pd.DataFrame({
            "Title": [title],
            "Net": [net],
            "Gross": [gross], 
            "Tax": [tax],
            "Price": [price],
            "Total Cost": [cost],
        })
        df_shares_value = pd.concat([df_shares_value, new_row])

    st.dataframe(df_shares_value, hide_index=True, width=720)
    assets_shares_net = 0
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
    st.markdown("Add your holdings here:")
    df_crypto = pd.DataFrame([
        {"Title": "Bitcoin", "Ticker": "BTC", "Count": 2, "Avg Cost": 200},
    ])
    edited_df_crypto = st.data_editor(
        df_crypto,
        width=720,
        num_rows="dynamic",
    )

    title_btc = df_crypto["Title"][0]
    ticker_btc = df_crypto["Ticker"][0]
    count_btc = df_crypto["Count"][0]
    avg_cost_btc = df_crypto["Avg Cost"][0]
    cost_btc = count_btc * avg_cost_btc
    price_btc = yf.Ticker(ticker_btc + "-" + selected_currency).basic_info["lastPrice"]
    gross_btc = count_btc * price_btc
    profit_btc = gross_btc - cost_btc
    cgt_btc = profit_btc * cgt
    net_btc = int(gross_btc - cgt_btc)
    df_crypto_value = pd.DataFrame([
        {"Title": title_btc, "Net": net_btc, "Price": price_btc, "Avg Cost": avg_cost_btc, "Cost": cost_btc},
    ])
    st.write("##### Value")
    st.dataframe(df_crypto_value, hide_index=True, width=720)
    assets_crypto_net = 0
    for key in df_crypto_value["Net"]:
        try:
            assets_crypto_net += key
        except:
            print("Assets > Crypto > Value calc error")
    st.write("Crypto Net Sum:", curr_symbol, assets_crypto_net)
    if "assets_crypto_net" not in st.session_state:
        st.session_state["assets_crypto_net"] = assets_crypto_net

with tab1:
    assets_net_worth = assets_cash + assets_shares_net + assets_crypto_net
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
    