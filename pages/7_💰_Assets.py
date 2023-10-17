import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(layout="centered")

st.markdown("# Perfin")

# Settings
col1, col2 = st.columns([1, 1], gap="small")
with col2:
    st.markdown("### Settings")

    cgt_base=st.slider(
        "Capital Gains Tax (%):",
        min_value = 0,
        max_value = 100,
        value = 33,
        format = "%d",
    )
    cgt = cgt_base/100

    selected_currency=st.selectbox("Currency:", options=("EUR","GBP","USD"))
    if selected_currency is "EUR":
        curr_symbol = "€"
    elif selected_currency is "GBP":
        curr_symbol = "£"
    elif selected_currency is "GBP":
        curr_symbol = "$"
    else:
        curr_symbol = selected_currency
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

with col1:
    st.markdown("### Assets")
    st.markdown("#### Cash")
    st.markdown("Cash and cash equivalent")
    df_cash = pd.DataFrame([
       {"Cash": "Mattress", "Net": 100},
       {"Cash": "Savings", "Net": 1000},
   ])
    edited_df_cash = st.data_editor(
        df_cash,
        num_rows="dynamic"
    )
    cash_sum = 0
    for key in edited_df_cash["Net"]:
        try: 
            cash_sum += key
        except:
            print("Assets: No cash")
    st.write('Cash Sum:', cash_sum, curr_symbol)
    # st.markdown("---")

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
    num_rows="dynamic",
    # disabled=["Net", "Gross", "Tax", "Price", "Cost"],
)
eq_sum = 0
for key in edited_df_equity["Net"]:
    try: 
        eq_sum += key
    except:
        print("Assets: No equity")
st.write('Equity Net Sum:', eq_sum, curr_symbol)
st.markdown("---")

# st.write(yf.Ticker("BTC-" + selected_currency).info)
ticker_btc = "BTC-" + selected_currency
st.markdown("#### Cryptocurrency")
df_crypto = pd.DataFrame(
    [
       {"Title": "Bitcoin", "Ticker": "BTC", "Count": 2, "Avg Cost": 200,},
   ]
)
edited_df_crypto = st.data_editor(
    df_crypto,
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
st.dataframe(df_crypto_value, hide_index=True)
crypto_sum = 0
for key in df_crypto_value["Net"]:
    try: 
        crypto_sum += key
    except:
        print("Assets: No equity")
st.write("Crypto Net Sum:", crypto_sum, curr_symbol)
st.markdown("---")

st.markdown("### Net Worth")
assets_total = cash_sum + eq_sum + crypto_sum
st.write("Net Worth:", assets_total, curr_symbol)

col1, col2 = st.columns([3, 3], gap="small")

with col2:
    if assets_total > 0:
        fig1, ax1 = plt.subplots()
        ax1.pie(
            [cash_sum, eq_sum, crypto_sum],
            autopct='%.0d%%',
            pctdistance=0.83,
            counterclock=False,
            startangle=90,
            # textprops = {'size': 'medium'},
        )
        st.pyplot(fig1)