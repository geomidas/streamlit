import streamlit as st
import auth_functions
import firebase_admin
import json
import pages.shared.functions as sf


# cred = firebase_admin.credentials.Certificate("perfin-db-firebase-adminsdk.json")
# ref = firebase_admin.db.reference("/", url=st.secrets['DB_URL'])
# data = {"UserID": {"testkey": "value"}}
# ref.set(data)

st.set_page_config("PerFin", page_icon="💰")
st.markdown("### Personal Finance")

# Not logged in -----------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    sf.login_box()

# Logged in --------------------------------------------------------------------------------------
else:
    # Delete all data. Users do not yet have personal data stored in a db.
    for key in st.session_state.keys():
        del st.session_state[key]

    tab1, tab2 = st.tabs([
        "__🏠 Home__",
        "__⚙️ Account__",
    ])

    with tab1:
        st.write("""
            - Tracking Income & Expenses
            - Budgeting
            - Tracking Asset Value
            - Estimating Financial Freedom
        """)
        st.image("https://www.theglobeandmail.com/files/dev/www/cache-long/arc-site-team/for-you-package/banner-desktop-900.png")
        st.divider()

        st.write("### Path to Financial Independence")
        st.graphviz_chart("""
            digraph {
                "Track Expenses" -> "Emergency Fund"
                "Emergency Fund" -> "Pay bad debt"
                "Pay bad debt" -> "Save"
                "Pay bad debt" -> "Pension"
                "Pay bad debt" -> "Extra Investments"
                "Pension" -> "FI"
                "Extra Investments" -> "FI"
            }
            """,
            use_container_width=True
        )

    with tab2:
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
                "__Verified:__ `" + str(st.session_state.user_info["emailVerified"]) + "`"
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
