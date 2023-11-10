import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import locale
import pages.shared.functions as sf


st.set_page_config("PerFin", page_icon="💰")
st.markdown("### Assets")

if "user_info" not in st.session_state:
    sf.login_box()
elif "necessary_expenses" not in st.session_state:
    st.write("Please follow the page order, so variables can get initialized.")
else:
    locale.setlocale( locale.LC_ALL, 'en_US' )
    def curr_fmt(val):
        return locale.currency(val, symbol=False, grouping=True)

    def get_share_price(ticker):
        return yf.Ticker(ticker).basic_info["lastPrice"]

    def get_crypto_price(ticker, selected_currency):
        return yf.Ticker(ticker + "-" + selected_currency).basic_info["lastPrice"]

    # Load Settings
    selected_currency = st.session_state["selected_currency"]
    curr_symbol = st.session_state["curr_symbol"]
    cgt = st.session_state["cgt"]
    necessary_expenses = st.session_state["necessary_expenses"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "__⚙️ Dashboard__",
        "__💵 Cash &nbsp; &nbsp;__",
        "__🏛️ Shares &nbsp;__",
        "__🪙 Cryptocurrency__",
    ])

    with tab2:
        st.markdown("Cash and cash equivalents:")
        df_cash = pd.DataFrame([
            {"Cash": "Under the mattress", "Net": 0},
            {"Cash": "Savings", "Net": 1000},
        ])
        edited_df_cash = st.data_editor(df_cash, width=380, num_rows="dynamic")
        assets_cash = 0
        for key in edited_df_cash["Net"]:
            try:
                assets_cash += key
            except:
                print("Assets: No cash")
        st.info('Cash Sum: __' + curr_symbol + curr_fmt(assets_cash) + "__")
        st.session_state["assets_cash"] = assets_cash

        st.write("#### Emergency Fund")
        st.info("Months of all necessary expenses covered: __" + str(int(assets_cash / necessary_expenses)) + "__")

    with tab3:
        st.markdown("Add any shares you own:")
        df_shares = pd.DataFrame({"Title": ["Tesla"], "Ticker": ["TSLA"], "Count": [100.0], "Avg Cost": [200.0]})
        edited_df_shares = st.data_editor(df_shares, use_container_width=True, num_rows="dynamic")

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

            st.dataframe(df_shares_value, hide_index=True, use_container_width=True)
            for key in df_shares_value["Net"]:
                try:
                    assets_shares_net += key
                except:
                    print("Assets: No shares")
            st.info('Shares Net Sum: __' + curr_symbol + curr_fmt(assets_shares_net) + "__")

        st.session_state["assets_shares_net"] = assets_shares_net

    with tab4:
        ticker_btc = "BTC-" + selected_currency
        st.markdown("Crypto you hodl:")
        df_crypto = pd.DataFrame({"Title": ["Bitcoin"], "Ticker": ["BTC"], "Count": [0.1], "Avg Cost": [1000.0]})
        edited_df_crypto = st.data_editor(df_crypto, use_container_width=True, num_rows="dynamic")

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

            st.dataframe(df_crypto_value, hide_index=True, use_container_width=True)
            for key in df_crypto_value["Net"]:
                try:
                    assets_crypto_net += key
                except:
                    print("Assets > Crypto > Value calc error")
            st.info("Crypto Net Sum: __" + curr_symbol + curr_fmt(assets_crypto_net) + "__")

        st.session_state["assets_crypto_net"] = assets_crypto_net

    with tab1:

        if assets_cash != 0 and assets_shares_net != 0:
            col1, col2, col3 = st.columns([3, 3, 4], gap="medium")
            with col1:
                st.write("##### Net Worth")
                assets_net_investments = int(assets_shares_net + assets_crypto_net)
                st.session_state.assets_net_investments = assets_net_investments
                assets_net_worth = int(assets_cash) + assets_net_investments
                st.info("Current Net Worth: __" + curr_symbol + curr_fmt(assets_net_worth) + "__")
                st.info("Net Investments: __" + curr_symbol + curr_fmt(assets_net_investments) + "__")
                st.session_state["assets_net_worth"] = assets_net_worth
            with col2:
                st.markdown("##### Allocation")
                st.info("Cash: __" + curr_symbol + curr_fmt(assets_cash) + "__")
                st.info("Net Shares: __" + curr_symbol + curr_fmt(assets_shares_net) + "__")
                st.info("Net Crypto: __" + curr_symbol + curr_fmt(assets_crypto_net) + "__")
            with col3:
                fig1, ax1 = plt.subplots()
                ax1.pie(
                    [assets_cash, assets_shares_net, assets_crypto_net],
                    labels=["Cash", "Shares", "Crypto"],
                    autopct='%.0d%%',
                    pctdistance=0.83,
                    counterclock=False,
                    startangle=45,
                )
                st.pyplot(fig1)

        st.write("##### Net Worth over time")
        df_net_worth = pd.DataFrame([
            {"Month": "2023-01", "Net Worth": 100, "Net Investments": 50, "Net Shares": 50, "Net Crypto": 30},
            {"Month": "2023-02", "Net Worth": 150, "Net Investments": 50, "Net Shares": 50, "Net Crypto": 30},
            {"Month": "2023-03", "Net Worth": 200, "Net Investments": 150, "Net Shares": 50, "Net Crypto": 30},
            {"Month": "2023-04", "Net Worth": 200, "Net Investments": 150, "Net Shares": 50, "Net Crypto": 30},
            {"Month": "2023-05", "Net Worth": 250, "Net Investments": 150, "Net Shares": 50, "Net Crypto": 30},
            {"Month": "2023-06", "Net Worth": 400, "Net Investments": 250, "Net Shares": 150, "Net Crypto": 30},
            {"Month": "2023-07", "Net Worth": 350, "Net Investments": 150, "Net Shares": 150, "Net Crypto": 30},
            {"Month": "2023-08", "Net Worth": 500, "Net Investments": 350, "Net Shares": 150, "Net Crypto": 30},
            {"Month": "2023-09", "Net Worth": 500, "Net Investments": 350, "Net Shares": 150, "Net Crypto": 30},
            {"Month": "2023-10", "Net Worth": 600, "Net Investments": 450, "Net Shares": 200, "Net Crypto": 30},
            {"Month": "2023-11", "Net Worth": 500, "Net Investments": 350, "Net Shares": 100, "Net Crypto": 30},
            {"Month": "2023-12", "Net Worth": 700, "Net Investments": 450, "Net Shares": 200, "Net Crypto": 30},
        ])
        with st.expander(label="Net Worth Data", expanded=False):
            edited_df = st.data_editor(df_net_worth, num_rows="dynamic")
        st.line_chart(df_net_worth, x="Month", height=420, use_container_width=True)
