"""
6_Admin_Panel.py
------------------
This Streamlit page allows an administrator to view all complaints
from all users and update their status (Pending, In Progress, Resolved).

Access is protected by a simple admin password stored in the .env file.
This is a beginner-friendly approach and not a full security system.
"""

import streamlit as st
import sys
import os

# Add the project's root folder to the system path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from database.database import get_all_complaints, update_complaint_status
from utils.image_utils import load_image

# Load environment variables from .env file
load_dotenv()

# Get the admin password from .env, or use a default password if not set
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# Set up the page title
st.set_page_config(page_title="Admin Panel - UrbanEye AI", page_icon="🛠️")

st.title("🛠️ Admin Panel")
st.write("This page is for administrators to manage and update complaint statuses.")

# Initialize session_state variable to track admin login
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# Step 1: If the admin is not logged in yet, show a password field
if not st.session_state["is_admin"]:
    entered_password = st.text_input("Enter Admin Password", type="password")
    login_button = st.button("Login as Admin")

    if login_button:
        if entered_password == ADMIN_PASSWORD:
            st.session_state["is_admin"] = True
            st.success("Admin login successful!")
            st.rerun()
        else:
            st.error("Incorrect admin password.")

else:
    # Step 2: Show a logout button for the admin
    if st.button("Logout from Admin"):
        st.session_state["is_admin"] = False
        st.rerun()

    st.divider()

    # Step 3: Fetch all complaints from the database
    complaints = get_all_complaints()

    if len(complaints) == 0:
        st.info("No complaints have been submitted yet.")
    else:
        st.write(f"Total complaints in the system: **{len(complaints)}**")
        st.divider()

        # Step 4: Loop through each complaint and let the admin update its status
        # The columns in the complaints table are:
        # id, user_id, image_path, issue_type, confidence, location, severity, status, created_at
        for complaint in complaints:
            complaint_id = complaint[0]
            image_path = complaint[2]
            issue_type = complaint[3]
            confidence = complaint[4]
            location = complaint[5]
            severity = complaint[6]
            current_status = complaint[7]
            created_at = complaint[8]

            # Create a two-column layout: image on the left, details on the right
            col1, col2 = st.columns([1, 2])

            with col1:
                if os.path.exists(image_path):
                    st.image(load_image(image_path), use_column_width=True)
                else:
                    st.write("Image not found")

            with col2:
                st.write(f"**Complaint ID:** {complaint_id}")
                st.write(f"**Issue Type:** {issue_type}")
                st.write(f"**Confidence Score:** {confidence:.2f}")
                st.write(f"**Location:** {location}")
                st.write(f"**Severity:** {severity}")
                st.caption(f"Submitted on: {created_at}")

                # Dropdown to select a new status for this complaint
                status_options = ["Pending", "In Progress", "Resolved"]
                selected_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=status_options.index(current_status),
                    key=f"status_{complaint_id}"
                )

                # Button to save the new status
                update_button = st.button("Update Status", key=f"update_{complaint_id}")

                if update_button:
                    update_complaint_status(complaint_id, selected_status)
                    st.success(f"Complaint {complaint_id} status updated to '{selected_status}'.")
                    st.rerun()

            st.divider()
