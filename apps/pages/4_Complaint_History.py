"""
4_Complaint_History.py
------------------------
This Streamlit page shows the complaint history for the logged-in user.
It displays each complaint's image, issue type, confidence score,
location, severity level, status, and the date it was submitted.
"""

import streamlit as st
import sys
import os
import pandas as pd

# Add the project's root folder to the system path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.database import get_complaints_by_user
from utils.image_utils import load_image

# Set up the page title
st.set_page_config(page_title="Complaint History - UrbanEye AI", page_icon="📋")

st.title("📋 Your Complaint History")

# Make sure session_state variables exist
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Step 1: Check that the user is logged in
if not st.session_state["logged_in"]:
    st.warning("Please log in first to view your complaint history.")
    st.stop()

# Step 2: Fetch all complaints for this user from the database
user_id = st.session_state["user_id"]
complaints = get_complaints_by_user(user_id)

# Step 3: Check if the user has any complaints
if len(complaints) == 0:
    st.info("You have not submitted any complaints yet. Go to the 'Report Issue' page to submit one.")
else:
    st.write(f"You have submitted **{len(complaints)}** complaint(s).")
    st.divider()

    # Step 4: Loop through each complaint and display its details
    # The columns in the complaints table are:
    # id, user_id, image_path, issue_type, confidence, location, severity, status, created_at
    for complaint in complaints:
        complaint_id = complaint[0]
        image_path = complaint[2]
        issue_type = complaint[3]
        confidence = complaint[4]
        location = complaint[5]
        severity = complaint[6]
        status = complaint[7]
        created_at = complaint[8]

        # Create a two-column layout: image on the left, details on the right
        col1, col2 = st.columns([1, 2])

        with col1:
            # Show the complaint image if the file still exists
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

            # Show the status with a color based on its value
            if status == "Pending":
                st.warning(f"**Status:** {status}")
            elif status == "In Progress":
                st.info(f"**Status:** {status}")
            else:
                st.success(f"**Status:** {status}")

            st.caption(f"Submitted on: {created_at}")

        st.divider()
