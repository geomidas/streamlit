import streamlit as st

st.set_page_config(layout="centered")

# Load variables
curr_symbol = st.session_state["curr_symbol"]
assets_cash = st.session_state["assets_cash"]
assets_shares_net = st.session_state["assets_shares_net"]
assets_crypto_net = st.session_state["assets_crypto_net"]
assets_net_worth = st.session_state["assets_net_worth"]
necessary_expenses = st.session_state["necessary_expenses"]
monthly_debt = st.session_state["monthly_debt"]

st.markdown("### Financial Independence")

tab1, = st.tabs([
    "__🏖️ Retirement__",
    ])

with tab1:
    col1, col2, col3, col4 = st.columns([1,1,1,1], gap="medium")
    with col1:
        retire_rr = st.number_input("Expected return rate", min_value=0.0, value=0.08)
    with col2:
        retire_monthly_sal = st.number_input('Monthly "income"', min_value=0, value=1000)
    with col3:
        retire_wr = st.number_input("Withrawal rate", min_value=0.0, value=0.04)
    with col4:
        retire_cgt = st.number_input("CGT in retirement", min_value=0.0, value=0.33)
    st.write("\n\n\n\n")
    retire_yearly_income = retire_monthly_sal * 12
    st.write("You can retire when your Net investments reach", curr_symbol, int(retire_yearly_income*(1/retire_wr)))
    with st.expander("If you retired now"):
        st.write('Yearly budget:', curr_symbol, int(assets_net_worth*retire_wr))
        st.write('Monthly budget:', curr_symbol, int(assets_net_worth*retire_wr/12))

    st.write("#### Projected Net Worth of Investments")
    st.write("__`charty chart`__")

    st.write("Years untill retirement:", "__1234__")
    st.write("Υears of necessary expenses covered:", "__1234__")

    st.write("#### Current status")
    st.write("Net Worth:", curr_symbol, assets_net_worth)
    net_investments = assets_shares_net + assets_crypto_net
    st.write("Net Investments:", curr_symbol, net_investments)
    st.write("Yearly added investments:", curr_symbol, 1234)
    # st.column_config.ProgressColumn("Financial progress")

    if net_investments >= retire_monthly_sal * 840:
        st.write("Financial Status: __Financial Abundance__")
    elif net_investments >= retire_monthly_sal * 600:
       st.write("Financial Status: __Financial Freedom__")
    elif net_investments >= retire_monthly_sal * 480:
       st.write("Financial Status: __Financial Independency__")
    elif net_investments >= retire_monthly_sal * 360:
       st.write("Financial Status: __Financial Flexibility__")
    elif net_investments >= retire_monthly_sal * 240:
       st.write("Financial Status: __Financial Security__")
    elif net_investments >= retire_monthly_sal * 120:
       st.write("Financial Status: __Barista FI__")
    elif int(monthly_debt) == 0:
        st.write("Financial Status: __Debt Freedom__")
    elif assets_cash >= int(6 * necessary_expenses):
        st.write("Financial Status: __Financial Stability__")
    elif assets_cash >= 0:
        st.write("Financial Status: __Financial Solvancy__")
    else:
        st.write("Financial Status: __Financial Dependence__")

    with st.expander("All financial statuses"):
        st.write({
            "Financial Dependence": 0,
            "Financial Solvancy": 0,
            "Financial Stability": int(6 * necessary_expenses),
            "Debt Freedom": 0,
            "Barista FI": retire_monthly_sal * 120,
            "Financial Security": retire_monthly_sal * 240,
            "Financial Flexibility": retire_monthly_sal * 360,
            "Financial Independency": retire_monthly_sal * 480,
            "Financial Freedom": retire_monthly_sal * 600,
            "Financial Abundance": retire_monthly_sal * 840,
        })

    st.write("#### Useful resources")
    st.write("Evaluate your plan:\n", "- Rich, broke or dead?\n", "https://engaging-data.com/will-money-last-retire-early")
