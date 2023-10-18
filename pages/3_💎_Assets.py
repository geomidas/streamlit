import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(layout="centered")

st.markdown("# Perfin")

# Load Settings
selected_currency = st.session_state["selected_currency"]
curr_symbol = st.session_state["curr_symbol"]
price_update_method = st.session_state["price_update_method"]
cgt = st.session_state["cgt"]

st.markdown("### Assets 💎")

tab1, tab2, tab3, tab4 = st.tabs(["💵 __Cash__", "🏛️ __Shares__", "🪙 __Cryptocurrency__", "🏵️ __Net Worth__"])

with tab1:
    st.markdown("#### Cash")
    st.markdown("Cash and cash equivalent")
    df_cash = pd.DataFrame([
        {"Cash": "Under the mattress", "Net": 100},
        {"Cash": "Savings", "Net": 1000},
    ])
    edited_df_cash = st.data_editor(
        df_cash,
        width=360,
        num_rows="dynamic",
    )
    cash_sum = 0
    for key in edited_df_cash["Net"]:
        try: 
            cash_sum += key
        except:
            print("Assets: No cash")
    st.write('Cash Sum:', cash_sum, curr_symbol)

with tab2:
    st.markdown("#### Shares")
    st.markdown("Shares in public companies")
    df_equity = pd.DataFrame(
        [
           {"Stock": "TSLA", "Net": 10, "Gross": 0, "Tax": 0, "Count": 0, "Price": yf.Ticker("TSLA").basic_info[price_update_method], "Avg Cost": 200, "Cost": 0},
           {"Stock": "AAPL", "Net": 20, "Gross": 0, "Tax": 0, "Count": 0, "Price": yf.Ticker("AAPL").basic_info[price_update_method], "Avg Cost": 100, "Cost": 0},
       ]
    )
    edited_df_equity = st.data_editor(
        df_equity,
        width=720,
        num_rows="dynamic",
        # disabled=["Net", "Gross", "Tax", "Price", "Cost"],
    )
    eq_sum = 0
    for key in edited_df_equity["Net"]:
        try: 
            eq_sum += key
        except:
            print("Assets: No shares")
    st.write('Shares Net Sum:', eq_sum, curr_symbol)

with tab3:
    ticker_btc = "BTC-" + selected_currency
    st.markdown("#### Cryptocurrency")
    df_crypto = pd.DataFrame(
        [
           {"Title": "Bitcoin", "Ticker": "BTC", "Count": 2, "Avg Cost": 200,},
       ]
    )
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
    price_btc = yf.Ticker(ticker_btc + "-" + selected_currency).basic_info[price_update_method]
    gross_btc = count_btc * price_btc
    profit_btc = gross_btc - cost_btc
    cgt_btc = profit_btc * cgt
    net_btc = int(gross_btc - cgt_btc)
    df_crypto_value = pd.DataFrame(
        [
            {"Title": title_btc, "Net": net_btc, "Price": price_btc, "Avg Cost": avg_cost_btc, "Cost": cost_btc},
        ]
    )
    st.write("Value")
    st.dataframe(df_crypto_value, hide_index=True, width=720)
    crypto_sum = 0
    for key in df_crypto_value["Net"]:
        try: 
            crypto_sum += key
        except:
            print("Assets: No equity")
    st.write("Crypto Net Sum:", crypto_sum, curr_symbol)

with tab4:
    st.markdown("### Net Worth")
    assets_total = cash_sum + eq_sum + crypto_sum
    st.write("Net Worth:", assets_total, curr_symbol)

    st.markdown("### Net Worth")
    col1, col2 = st.columns([3, 5], gap="medium")
    with col1:
        df_net_worth = pd.DataFrame([
            {"Month": "2023-01", "Net Worth": 100,},
            {"Month": "2023-02", "Net Worth": 150,},
            {"Month": "2023-03", "Net Worth": 200,},
            {"Month": "2023-04", "Net Worth": 200,},
            {"Month": "2023-05", "Net Worth": 250,},
            {"Month": "2023-06", "Net Worth": 400,},
            {"Month": "2023-07", "Net Worth": 350,},
            {"Month": "2023-08", "Net Worth": 500,},
            {"Month": "2023-09", "Net Worth": 500,},
            {"Month": "2023-10", "Net Worth": 600,},
            {"Month": "2023-11", "Net Worth": 500,},
            {"Month": "2023-12", "Net Worth": 700,},
        ])
        edited_df = st.data_editor(df_net_worth, num_rows="dynamic")
    with col2:
        st.line_chart(edited_df, x="Month", y="Net Worth")
