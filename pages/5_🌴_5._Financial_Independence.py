import streamlit as st

st.set_page_config(layout="centered")

# Load variables
curr_symbol = st.session_state["curr_symbol"]
assets_cash = st.session_state["assets_cash"]
assets_shares_net = st.session_state["assets_shares_net"]
assets_crypto_net = st.session_state["assets_crypto_net"]
assets_net_worth = st.session_state["assets_net_worth"]

st.markdown("### Financial Independence")

tab2, tab3 = st.tabs([
    "__🏖️ Retirement__",
    "__👑 Financial Status__",
    ])

with tab2:
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
    st.write("Years untill retirement:", 1234)
    st.write("Investments as years of all necessary expenses covered:", 1234)
    st.write("If you retired now:")
    st.write('- Yearly budget:', curr_symbol, int(assets_net_worth*retire_wr))
    st.write('- Monthly budget:', curr_symbol, int(assets_net_worth*retire_wr/12))
    st.write("Evaluate your plan:\n", "- Rich, broke or dead?\n", "https://engaging-data.com/will-money-last-retire-early")

with tab3:
    st.write("Net Worth:", curr_symbol, assets_net_worth)
    st.write("Net Investments:", assets_shares_net + assets_crypto_net)
    st.write("Yearly added investments:", 1234)
    # st.column_config.ProgressColumn("Financial progress")
    st.write("Financial Status:")
    st.write([
        "Financial Dependence",
        "Financial Solvancy",
        "Financial Stability",
        "Debt Freedom",
        "Barista FI",
        "Financial Security",
        "Financial Flexibility",
        "Financial Independency",
        "Financial Freedom",
        "Financial Abundance",
    ])

    st.write("Projected Net Worth of Investments. Chart.")
