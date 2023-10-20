import streamlit as st

st.set_page_config(layout="centered")

# Load variables
cgt = st.session_state["cgt"]
curr_symbol = st.session_state["curr_symbol"]
assets_cash = st.session_state["assets_cash"]
assets_shares_net = st.session_state["assets_shares_net"]
assets_net_worth = st.session_state["assets_net_worth"]

st.markdown("# Perfin")
st.markdown("### Financial Independence 🌴")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "__📦 Emergency Fund__",
    "__🏖️ Retirement__",
    "__👑 Financial Status__",
    "__🏵️ Evaluation__",
    "__🏵️ Other data__",
    ])

with tab1:
    st.write("##### Emergency fund")
    st.write("Cash sum:", curr_symbol, assets_cash)
    st.write("Months of all necessary expenses covered:", 2)

with tab2:
    st.write("##### Retirement")
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        st.number_input("Withrawal rate (%):", min_value=0)
        st.number_input("Expected return rate (from all types of investments) (%):", min_value=0)
        st.write("Current Capital Gains Tax:", cgt * 100, "%")
        st.number_input("Expected CGT in retirement (%):", min_value=0)
    with col2:
        st.number_input('Desired monthly "income":', min_value=0)
        st.number_input('Desired yearly "income":', min_value=0)
        st.write("You can retire when your Net investments reach", curr_symbol, 1000000)
        st.write("Years untill retirement:", curr_symbol, 100)
    st.divider()
    st.write("##### If you retired now")
    st.write('Monthly "salary":', curr_symbol, 100)
    st.write('Yearly "salary":', curr_symbol, 1200)

with tab3:
    st.write("##### Financial status")
    st.write("Net Worth:", curr_symbol, assets_net_worth)
    st.write("Net Investments:", assets_shares_net)
    st.write("Yearly added investments:", 0)
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

with tab4:
    st.write("##### Evaluate your plan")
    st.link_button("Rich, broke or dead?", "https://engaging-data.com/will-money-last-retire-early")

with tab5:
    st.write("##### Other")
    st.write("Investments as years of all necessary expenses covered:", 2)
    st.write("Current investment profit:", curr_symbol, 100)
    st.write("Money made by working:", curr_symbol, 10000)
