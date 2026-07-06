"""
2_Login.py
-----------
This Streamlit page allows an existing user to log in.
It checks the username and password against the SQLite database
and updates the session_state so the user stays logged in
while using other pages of the app.
"""

import streamlit as st
import sys
import os

# Add the project's root folder to the system path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.database import get_user_by_username
from utils.auth_utils import check_password

# Set up the page title
st.set_page_config(page_title="Login - UrbanEye AI", page_icon="🔑")

st.title("🔑 Login to Your Account")

# Make sure session_state variables exist (in case this page loads first)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_id"] = None
    st.session_state["username"] = None

# If the user is already logged in, show a message instead of the login form
if st.session_state["logged_in"]:
    st.success(f"You are already logged in as **{st.session_state['username']}**")
    st.write("Go to the sidebar to report an issue or view your complaint history.")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state["username"] = None
        st.rerun()

else:
    # Show the login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    # This code runs only when the user clicks the Login button
    if submit_button:

        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            # Fetch the user row from the database
            user_row = get_user_by_username(username)

            if user_row is None:
                st.error("No account found with this username.")
            else:
                # The columns in the users table are:
                # id, full_name, username, email, password, created_at
                stored_password = user_row[4]

                if check_password(password, stored_password):
                    # Login successful, save details in session_state
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user_row[0]
                    st.session_state["username"] = user_row[2]

                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")
