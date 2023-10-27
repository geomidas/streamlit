import streamlit as st
import locale

locale.setlocale( locale.LC_ALL, 'en_IE.UTF-8' )
def curr_fmt(val):
    return locale.currency(val, symbol=False, grouping=True)

# Load variables
curr_symbol = st.session_state["curr_symbol"]
assets_cash = st.session_state["assets_cash"]
assets_shares_net = st.session_state["assets_shares_net"]
assets_crypto_net = st.session_state["assets_crypto_net"]
assets_net_worth = st.session_state["assets_net_worth"]
necessary_expenses = st.session_state["necessary_expenses"]
monthly_debt = st.session_state["monthly_debt"]
net_investments = assets_shares_net + assets_crypto_net

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
    st.info("You can retire when your Net investments reach __" + curr_symbol + curr_fmt(retire_yearly_income*(1/retire_wr)) + "__")
    # st.info("Your budget if you retired now:\n\n > Yearly: __" + curr_symbol + curr_fmt(assets_net_worth*retire_wr) + "__\n\n > Monthly: __" + curr_symbol + curr_fmt(assets_net_worth*retire_wr/12) + "__")

    st.write("#### Projected Net Worth of Investments")
    st.write("__`charty chart`__")

    st.write("Years untill retirement:", "__1234__")
    st.write("Υears of necessary expenses covered:", "__1234__")

    st.write("#### Current status")
    col1, col2, = st.columns([1,1], gap="medium")
    with col1:
        st.info("Net Worth: __" + curr_symbol + curr_fmt(assets_net_worth) + "__")

        if net_investments >= retire_monthly_sal * 840:
            st.info("Financial Status: __Financial Abundance__")
        elif net_investments >= retire_monthly_sal * 600:
            st.info("Financial Status: __Financial Freedom__")
        elif net_investments >= retire_monthly_sal * 480:
            st.info("Financial Status: __Financial Independency__")
        elif net_investments >= retire_monthly_sal * 360:
            st.info("Financial Status: __Financial Flexibility__")
        elif net_investments >= retire_monthly_sal * 240:
            st.info("Financial Status: __Financial Security__")
        elif net_investments >= retire_monthly_sal * 120:
            st.info("Financial Status: __Barista FI__")
        elif int(monthly_debt) == 0:
            st.info("Financial Status: __Debt Freedom__")
        elif assets_cash >= int(6 * necessary_expenses):
            st.info("Financial Status: __Financial Stability__")
        elif assets_cash >= 0:
            st.info("Financial Status: __Financial Solvancy__")
        else:
            st.info("Financial Status: __Financial Dependence__")
    with col2:
        st.info("Net Investments: __" + curr_symbol + curr_fmt(net_investments) + "__")
        st.info("Yearly added investments: __" + curr_symbol + curr_fmt(1234) + "__")

    st.write("#### Useful resources")
    st.write("Evaluate your plan:\n\n", "- Rich, broke or dead? https://engaging-data.com/will-money-last-retire-early")
