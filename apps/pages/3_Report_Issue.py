"""
3_Report_Issue.py
------------------
This Streamlit page allows a logged-in user to report a civic issue.
The user uploads a photo, the YOLOv8 model detects the issue type,
the app calculates a severity level, and the complaint is saved
in the SQLite database.
"""

import streamlit as st
import sys
import os

# Add the project's root folder to the system path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.database import add_complaint
from models.yolo_detector import detect_issue
from utils.severity_utils import calculate_severity
from utils.image_utils import save_uploaded_image, load_image

# Set up the page title
st.set_page_config(page_title="Report Issue - UrbanEye AI", page_icon="📷")

st.title("📷 Report a Civic Issue")

# Make sure session_state variables exist
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Step 1: Check that the user is logged in before allowing them to report an issue
if not st.session_state["logged_in"]:
    st.warning("Please log in first to report an issue.")
    st.stop()  # Stops the rest of the page from running

st.write("Upload a photo of the issue you want to report, then enter the location.")

# Step 2: Let the user upload an image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Step 3: Let the user enter the location manually
location = st.text_input("Enter the location of the issue (e.g. street name, area)")

# Step 4: Show a button to submit the complaint
submit_button = st.button("Detect Issue and Submit Complaint")

if submit_button:

    # Check that an image was uploaded
    if uploaded_file is None:
        st.error("Please upload an image before submitting.")

    # Check that a location was entered
    elif not location.strip():
        st.error("Please enter the location of the issue.")

    else:
        with st.spinner("Analyzing the image using YOLOv8..."):

            # Step 5: Save the uploaded image to disk
            username = st.session_state["username"]
            image_path = save_uploaded_image(uploaded_file, username)

            # Step 6: Run YOLOv8 detection on the saved image
            issue_type, confidence_score = detect_issue(image_path)

        # Step 7: Show the uploaded image to the user
        st.image(load_image(image_path), caption="Uploaded Image", use_column_width=True)

        if issue_type == "unknown":
            st.error("Could not confidently detect a civic issue in this image. "
                      "Please try uploading a clearer photo.")
        else:
            # Step 8: Calculate the severity level based on issue type and confidence
            severity = calculate_severity(issue_type, confidence_score)

            # Step 9: Show the detection results to the user
            st.success("Issue detected successfully!")
            st.write(f"**Detected Issue:** {issue_type}")
            st.write(f"**Confidence Score:** {confidence_score:.2f}")
            st.write(f"**Severity Level:** {severity}")

            # Step 10: Save the complaint in the database
            user_id = st.session_state["user_id"]
            add_complaint(user_id, image_path, issue_type, confidence_score, location, severity)

            st.success("Your complaint has been submitted successfully!")
            st.info("You can check the status of your complaint on the 'Complaint History' page.")
