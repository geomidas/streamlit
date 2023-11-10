import streamlit as st
import pandas as pd
import datetime
import locale
import pages.shared.functions as sf


st.set_page_config("PerFin", page_icon="💰")
st.markdown("### Financial Freedom")

if "user_info" not in st.session_state:
    sf.login_box()
elif "assets_cash" not in st.session_state:
    st.write("Please follow the page order, so variables can get initialized.")
else:
    locale.setlocale( locale.LC_ALL, 'en_US' )
    def curr_fmt(val):
        return locale.currency(val, symbol=False, grouping=True)

    # Load variables
    curr_symbol = st.session_state["curr_symbol"]
    assets_cash = st.session_state["assets_cash"]
    assets_shares_net = st.session_state["assets_shares_net"]
    assets_crypto_net = st.session_state["assets_crypto_net"]
    assets_net_worth = st.session_state["assets_net_worth"]
    assets_net_investments = st.session_state["assets_net_investments"]
    necessary_expenses = st.session_state["necessary_expenses"]
    monthly_debt = st.session_state["monthly_debt"]

    tab1, = st.tabs([
        "__🏖️ Retirement__",
        ])

    with tab1:
        col1, col2 = st.columns([1,1], gap="medium")
        with col1:
            retire_monthly_sal = st.number_input("Monthly budget in retirement (in " + curr_symbol + ")", min_value=0, value=2000)
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
                future_nw.T[row]["Projected Net Investments"] = int(assets_net_investments_compounder)
                if assets_net_investments_compounder >= retire_target:
                    target_hit_date = str(year_counter)
                    break
            future_nw = future_nw.dropna()
            st.dataframe(future_nw, hide_index=True, height=296, use_container_width=True)

        with col1:
            if target_hit_date != "Never":
                st.info("Year of retirement: __" + target_hit_date + "__")
                st.info("Years until retirement: __" + str(int(target_hit_date) - year) + "__")
            else:
                st.warning("You won't have enough investments in " + str(years_to_project) + " years")

        st.area_chart(future_nw, x="Year", y="Projected Net Investments", height=320)

        st.write("#### Current Financial Status")
        col1, col2 = st.columns([1,1], gap="medium")
        with col1:
            if assets_net_investments >= retire_monthly_sal * 600:
                st.info("__Financial Freedom__" + "\n\n" + "You have more money than you'll ever need.\n\nYou don't have to worry about money, even in economic downturns.")
            elif assets_net_investments >= retire_monthly_sal * 480:
                st.info("__Financial Independence__" + "\n\n" + "Your investment income or passive income is enough to cover your basic needs, you've achieved financial independence.\n\nA financially independent person can retire at any time without worrying about how to cover their costs of living, even if they may have to downsize their lifestyle a bit.")
            elif assets_net_investments >= retire_monthly_sal * 240:
                st.info("__Financial Security__" + "\n\n" + "You have eliminated your debt (or have enough assets to pay off all your debt) and could weather a period of unemployment without worry.\n\nAt this point, money is not just a safety net, but also a tool you can use to build the future you've been planning.\n\nAt this point, you may consider investing in other assets besides retirement accounts — a taxable account, rental real estate, or even your own small business.")
            elif assets_net_investments >= retire_monthly_sal * 120:
                st.info("__Barista FI__" + "\n\n" + "You are able to meet your financial obligations on your own.")
            elif assets_cash >= int(6 * necessary_expenses):
                st.info("__Financial Stability__" + "\n\n" + "You have an emergency fund of a few months expenses, repaid high-interest debt and are continuing to live within your means.\n\nWhile stability does not require you to be debt-free—as you may still have a mortgage, student loans, or even credit card debt, you'll have a savings buffer to ensure that you won't go into debt if you encounter an emergency or unexpected expense.")
            elif assets_cash >= 0:
                st.info("__Financial Solvency__" + "\n\n" + "You are able to meet your financial obligations on your own.")
            else:
                st.progress(0)
                st.info("__Financial Dependence__" + "\n\n" + "If you rely on a parent, a significant other, or someone else to pay your living expenses.\n\nThis stage starts from childhood.")
        with col2:
            retirement_progress = assets_net_investments/retire_target
            st.progress(retirement_progress, text="Retirement Progress")
            st.info("__" + curr_fmt(retirement_progress*100) + "%__ of the " + curr_symbol + curr_fmt(retire_target) + " needed.")

        st.write("#### Useful resources")
        st.write("Evaluate your plan:\n\n", "- Rich, broke or dead? https://engaging-data.com/will-money-last-retire-early")
