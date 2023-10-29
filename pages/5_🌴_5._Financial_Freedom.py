import streamlit as st
import pandas as pd
import datetime
import locale


locale.setlocale( locale.LC_ALL, 'en_US' )
def curr_fmt(val):
    return locale.currency(val, symbol=False, grouping=True)

st.set_page_config("PerFin", page_icon="💎")

# Load variables
curr_symbol = st.session_state["curr_symbol"]
assets_cash = st.session_state["assets_cash"]
assets_shares_net = st.session_state["assets_shares_net"]
assets_crypto_net = st.session_state["assets_crypto_net"]
assets_net_worth = st.session_state["assets_net_worth"]
assets_assets_net_investments = st.session_state["assets_assets_net_investments"]
necessary_expenses = st.session_state["necessary_expenses"]
monthly_debt = st.session_state["monthly_debt"]

st.markdown("### Financial Freedom")

tab1, = st.tabs([
    "__🏖️ Retirement__",
    ])

with tab1:
    col1, col2 = st.columns([1,1], gap="medium")
    with col1:
        retire_monthly_sal = st.number_input("Monthly budget (in " + curr_symbol + ")", min_value=0, value=2000)
    with col2:
        retire_wr_perc = st.number_input("Withrawal rate (%)", min_value=0.0, value=3.5)
        retire_wr = retire_wr_perc / 100
    retire_yearly_income = retire_monthly_sal * 12
    retire_target = retire_yearly_income*(1/retire_wr)
    st.info("You can retire when your Net investments reach __" + curr_symbol + curr_fmt(retire_target) + "__")
    # st.info("Your budget if you retired now:\n\n > Yearly: __" + curr_symbol + curr_fmt(assets_net_worth*retire_wr) + "__\n\n > Monthly: __" + curr_symbol + curr_fmt(assets_net_worth*retire_wr/12) + "__")

    st.write("#### Projected Net Worth of Investments")
    col1, col2 = st.columns([1,1], gap="medium")
    with col1:
        retire_rr_perc = st.number_input("Expected return rate (%)", min_value=0.0, value=8.0)
        retire_rr = retire_rr_perc / 100
        years_to_project = st.number_input("Years ahead to project", min_value=0, value=60)
    with col2:
        today = datetime.date.today()
        year = int(today.year)

        future_nw = pd.DataFrame(
            index=range(years_to_project),
            columns=["Year", "Projected Net Investments"]
        )
        year_counter = year
        assets_net_investments_compounder = assets_net_investments
        target_hit_date = "Never"
        for row in range(len(future_nw)):
            year_counter += 1
            future_nw.T[row]["Year"] = str(year_counter)
            assets_net_investments_compounder = assets_net_investments_compounder * (1.0 + retire_rr)
            future_nw.T[row]["Projected Net Investments"] = curr_fmt(assets_net_investments_compounder)
            if assets_net_investments_compounder >= retire_target:
                target_hit_date = str(year_counter)
                break
        st.dataframe(future_nw, hide_index=True)

    with col1:
        if target_hit_date != "Never":
            st.info("Year of retirement: __" + target_hit_date + "__")
            st.info("Years until retirement: __" + str(int(target_hit_date) - year) + "__")
        else:
            st.warning("🍆 You won't have enough investments in " + str(years_to_project) + " years")

    st.write("#### Current Financial Status")

    # st.info("Net Worth: __" + curr_symbol + curr_fmt(assets_net_worth) + "__" + "\n\n" + "Net Investments: __" + curr_symbol + curr_fmt(assets_net_investments) + "__" + "\n\n" + "Yearly added investments: __" + curr_symbol + curr_fmt(1234) + "__")

    if assets_net_investments >= retire_monthly_sal * 600:
        st.info("__Financial Freedom__" + "\n\n" + "You have more money than you'll ever need.\n\nYou don't have to worry about money, even in economic downturns.")
        st.progress(100)
    elif assets_net_investments >= retire_monthly_sal * 480:
        st.info("__Financial Independence__" + "\n\n" + "Your investment income or passive income is enough to cover your basic needs, you've achieved financial independence.\n\nA financially independent person can retire at any time without worrying about how to cover their costs of living, even if they may have to downsize their lifestyle a bit.")
        st.progress(90)
    elif assets_net_investments >= retire_monthly_sal * 240:
        st.info("__Financial Security__" + "\n\n" + "You have eliminated your debt (or have enough assets to pay off all your debt) and could weather a period of unemployment without worry.\n\nAt this point, money is not just a safety net, but also a tool you can use to build the future you've been planning.\n\nAt this point, you may consider investing in other assets besides retirement accounts — a taxable account, rental real estate, or even your own small business.")
        st.progress(60)
    elif assets_net_investments >= retire_monthly_sal * 120:
        st.info("__Barista FI__" + "\n\n" + "You are able to meet your financial obligations on your own.")
        st.progress(40)
    elif assets_cash >= int(6 * necessary_expenses):
        st.progress(20)
        st.info("__Financial Stability__" + "\n\n" + "You have an emergency fund of a few months expenses, repaid high-interest debt and are continuing to live within your means.\n\nWhile stability does not require you to be debt-free—as you may still have a mortgage, student loans, or even credit card debt, you'll have a savings buffer to ensure that you won't go into debt if you encounter an emergency or unexpected expense.")
    elif assets_cash >= 0:
        st.progress(10)
        st.info("__Financial Solvency__" + "\n\n" + "You are able to meet your financial obligations on your own.")
    else:
        st.progress(0)
        st.info("__Financial Dependence__" + "\n\n" + "If you rely on a parent, a significant other, or someone else to pay your living expenses.\n\nThis stage starts from childhood.")

    st.write("#### Useful resources")
    st.write("Evaluate your plan:\n\n", "- Rich, broke or dead? https://engaging-data.com/will-money-last-retire-early")
