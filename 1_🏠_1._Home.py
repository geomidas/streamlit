import streamlit as st
# import streamlit_authenticator as stauth

st.set_page_config("PerFin", page_icon="💎")

st.markdown("### PerFin")

tab1, tab2 = st.tabs([
    "__🏠 Home__",
    "__⚙️ Settings__",
])

with tab1:
    st.image("https://www.theglobeandmail.com/files/dev/www/cache-long/arc-site-team/for-you-package/banner-desktop-900.png", caption="Personal Finance")

with tab2:
    col1, col2 = st.columns([1,2], gap="medium")
    with col1:
        selected_currency=st.selectbox("Currency:", options=("EUR","GBP","USD"))
        if "selected_currency" not in st.session_state:
            st.session_state["selected_currency"] = selected_currency
        if selected_currency == "EUR":
            curr_symbol = "€"
        elif selected_currency == "GBP":
            curr_symbol = "£"
        elif selected_currency == "GBP":
            curr_symbol = "$"
        else:
            curr_symbol = selected_currency
        if "curr_symbol" not in st.session_state:
            st.session_state["curr_symbol"] = curr_symbol

        cgt_base=st.number_input(
            "Capital Gains Tax (%):",
            min_value = 0,
            max_value = 100,
            value = 33,
            format = "%d",
        )
        cgt = cgt_base/100
        if "cgt" not in st.session_state:
            st.session_state["cgt"] = cgt
