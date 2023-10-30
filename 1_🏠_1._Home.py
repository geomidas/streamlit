import streamlit as st
# import streamlit_authenticator as stauth

st.set_page_config("PerFin", page_icon="💎")

st.markdown("### PerFin")

import streamlit as st
import auth_functions

## -------------------------------------------------------------------------------------------------
## Not logged in -----------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    col1,col2,col3 = st.columns([1,2,1])

    # Authentication form layout
    do_you_have_an_account = col2.selectbox(label='Do you have an account?',options=('Yes','No','I forgot my password'))
    auth_form = col2.form(key='Authentication form',clear_on_submit=False)
    email = auth_form.text_input(label='Email')
    password = auth_form.text_input(label='Password',type='password') if do_you_have_an_account in {'Yes','No'} else auth_form.empty()
    auth_notification = col2.empty()

    # Sign In
    if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Signing in'):
            auth_functions.sign_in(email,password)

    # Create Account
    elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Creating account'):
            auth_functions.create_account(email,password)

    # Password Reset
    elif do_you_have_an_account == 'I forgot my password' and auth_form.form_submit_button(label='Send Password Reset Email',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Sending password reset link'):
            auth_functions.reset_password(email)

    # Authentication success and warning messages
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif 'auth_warning' in st.session_state:
        auth_notification.warning(st.session_state.auth_warning)
        del st.session_state.auth_warning

## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    # Show user information
    st.header('User information:')
    st.write(st.session_state.user_info)

    # Sign out
    st.header('Sign out:')
    st.button(label='Sign Out',on_click=auth_functions.sign_out,type='primary')

    # Delete Account
    st.header('Delete account:')
    password = st.text_input(label='Confirm your password',type='password')
    st.button(label='Delete Account',on_click=auth_functions.delete_account,args=[password],type='primary')

    tab1, tab2 = st.tabs([
        "__🏠 Home__",
        "__⚙️ Settings__",
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
