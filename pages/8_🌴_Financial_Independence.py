import streamlit as st

st.set_page_config(layout="centered")

# Load variables
cgt = st.session_state["cgt"]
curr_symbol = st.session_state["curr_symbol"]
assets_cash = st.session_state["assets_cash"]

st.markdown("# Perfin")
st.markdown("### Financial Independence 🌴")

tab1, tab2, tab3, tab4 = st.tabs([
    "__📦 Emergency Fund__",
    "__🏖️ Retirement__",
    "__👑 Financial Status__",
    "__🏵️ Other__"
    ])

with tab1:
    st.write("##### Emergency fund")
    st.write("Cash sum:", curr_symbol, assets_cash)
    st.write("Months of all necessary expenses covered: ")

with tab2:
    st.write("##### Retirement")
    st.number_input("Withrawal rate (%):", min_value=0)
    st.write("Current Capital Gains Tax:", cgt * 100, "%")
    st.number_input("Expected CGT in retirement (%):", min_value=0)
    st.number_input('Desired monthly "income":', min_value=0)
    st.number_input('Desired yearly "income":', min_value=0)
    st.write("You can retire when your Net investments reach", curr_symbol, 1000000)
    st.write("Years untill retirement:", curr_symbol, 100)
    st.divider()
    st.write("If you retired now:")
    st.write('Monthly "salary":', curr_symbol, 100)
    st.write('Yearly "salary":', curr_symbol, 1200)

with tab3:
    st.write("Net Worth:")
    st.write("Net Investments:")
    st.write("Yearly added investments:")
    st.write("Expected return rate (from all types of investments):")
    st.divider()
    st.write("Financial Status:", [
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
    st.divider()
    st.write("Projected Net Worth of Investments. Chart.")

with tab4:
    st.write("##### Other")
    st.write("Investments as years of expenses: ")
    st.write("Current investment profit: ")
    st.write("Money made by working: ")
    st.divider()
    st.write("##### Evaluate your plan")
    st.link_button("Rich, broke or dead?", "https://engaging-data.com/will-money-last-retire-early")
