"""
1_Register.py
--------------
This Streamlit page allows a new user to create an account.
It collects the user's full name, username, email, and password,
then saves the account details in the SQLite database.
"""

import streamlit as st
import sys
import os

# Add the project's root folder to the system path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.database import add_user, get_user_by_username
from utils.auth_utils import hash_password, is_valid_email, is_valid_username

# Set up the page title
st.set_page_config(page_title="Register - UrbanEye AI", page_icon="📝")

st.title("📝 Create a New Account")
st.write("Fill in the details below to register for UrbanEye AI.")

# Create a form so all fields are submitted together
with st.form("register_form"):
    full_name = st.text_input("Full Name")
    username = st.text_input("Username")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # The submit button for the form
    submit_button = st.form_submit_button("Register")

# This code runs only when the user clicks the Register button
if submit_button:

    # Step 1: Check that no fields are empty
    if not full_name or not username or not email or not password:
        st.error("Please fill in all the fields.")

    # Step 2: Check that the username is valid (no spaces, not empty)
    elif not is_valid_username(username):
        st.error("Username should not contain spaces or be empty.")

    # Step 3: Check that the email looks valid
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")

    # Step 4: Check that the two passwords match
    elif password != confirm_password:
        st.error("Passwords do not match.")

    # Step 5: Check that the password is long enough
    elif len(password) < 6:
        st.error("Password should be at least 6 characters long.")

    else:
        # Step 6: Check if the username is already taken
        existing_user = get_user_by_username(username)

        if existing_user is not None:
            st.error("This username is already taken. Please choose another one.")
        else:
            # Step 7: Hash the password before saving it
            hashed_password = hash_password(password)

            # Step 8: Save the new user in the database
            success = add_user(full_name, username, email, hashed_password)

            if success:
                st.success("Account created successfully! Please go to the Login page to sign in.")
            else:
                st.error("Something went wrong. Please try again.")
