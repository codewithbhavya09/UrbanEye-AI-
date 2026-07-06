"""
Home.py
--------
This is the main landing page of the UrbanEye AI Streamlit app.
It shows a welcome message and explains how to use the app.
It also manages the login session using Streamlit's session_state.
"""

import streamlit as st

# Set the page title and icon shown in the browser tab
st.set_page_config(
    page_title="UrbanEye AI",
    page_icon="🏙️",
    layout="centered"
)

# Initialize session_state variables if they do not already exist
# session_state keeps track of whether a user is logged in across pages
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None


def show_welcome_message():
    """
    Displays the main welcome section of the home page.
    """
    st.title("🏙️ UrbanEye AI")
    st.subheader("Intelligent Civic Issue Detection and Resolution Platform")

    st.write("""
    UrbanEye AI helps citizens report civic issues quickly and easily.
    Simply upload a photo of a problem such as a pothole, garbage pile,
    water leak, broken streetlight, or damaged road — our AI model will
    automatically detect the issue and help you file a complaint.
    """)


def show_login_status():
    """
    Shows whether the user is currently logged in or not,
    and gives instructions on what to do next.
    """
    st.divider()

    if st.session_state["logged_in"]:
        st.success(f"You are logged in as **{st.session_state['username']}**")
        st.write("Use the sidebar to report an issue, view your complaint history, or check the dashboard.")
    else:
        st.warning("You are not logged in.")
        st.write("Please use the sidebar to **Register** or **Login** before reporting an issue.")


def show_how_it_works():
    """
    Displays a short step-by-step explanation of how the app works.
    """
    st.divider()
    st.subheader("How It Works")

    st.write("""
    1. **Register / Login** to your account.
    2. **Upload a photo** of the civic issue you want to report.
    3. Our **YOLOv8 AI model** detects the issue type automatically.
    4. **Enter the location** of the issue manually.
    5. The app calculates a **severity level** (Low, Medium, High).
    6. Your complaint is saved and you can **track its status** anytime.
    7. View overall statistics on the **Dashboard** page.
    """)


# Run all the display functions in order
show_welcome_message()
show_login_status()
show_how_it_works()

# Sidebar navigation hint for the user
st.sidebar.title("Navigation")
st.sidebar.info("Use the pages listed above to move through the app.")
