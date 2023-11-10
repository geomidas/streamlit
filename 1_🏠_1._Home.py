import streamlit as st
import auth_functions
import pages.shared.functions as sf

st.set_page_config("PerFin", page_icon="💰")
st.markdown("### PerFin")

# Not logged in -----------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    sf.login_box()

# Logged in --------------------------------------------------------------------------------------
else:
    tab1, tab2, tab3 = st.tabs([
        "__🏠 Home__",
        "__🎯 Priorities__",
        "__⚙️ Account__",
    ])

    with tab1:
        st.write("### Personal Finance")
        st.write("""
            - Tracking Income & Expenses
            - Budgeting
            - Tracking Asset Value
            - Estimating Financial Freedom
        """)
        st.image("https://www.theglobeandmail.com/files/dev/www/cache-long/arc-site-team/for-you-package/banner-desktop-900.png")

    with tab2:
        st.write("### Priorities")
        st.graphviz_chart("""
            digraph {
                "Track Expenses" -> "Emergency Fund"
                "Emergency Fund" -> "Pay bad debt"
                "Pay bad debt" -> "Save"
                "Pay bad debt" -> "Pension"
                "Pay bad debt" -> "Invest"
            }
            """,
            use_container_width=True
        )

    with tab3:
        st.write("#### Settings")
        col1, col2 = st.columns([1,1], gap="medium")
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
        with col2:
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
        st.divider()
        st.write("#### Account")
        col1, col2 = st.columns([1,1], gap="medium")
        with col1:
            st.info(
                "__Email:__ `" + st.session_state.user_info["email"] + "`\n\n" + 
                "__Verified:__ `" + str(st.session_state.user_info["emailVerified"]) + "`\n\n" +
                "__User ID:__ `" + st.session_state.user_info["localId"] + "`"
            )
        with col2:
            # Sign out
            st.write("Sign out:")
            st.button(label='Sign Out',on_click=auth_functions.sign_out,type='primary')
            st.divider()
            # Delete Account
            st.write('Delete account:')
            password = st.text_input(label='Confirm your password',type='password')
            st.button(label='Delete Account',on_click=auth_functions.delete_account,args=[password],type='primary')
