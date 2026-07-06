"""
5_Dashboard.py
---------------
This Streamlit page shows a simple dashboard with charts summarizing
all the complaints submitted by all users. It uses Matplotlib to create:
1. A bar chart of complaint counts by issue type
2. A pie chart of complaint status breakdown
3. A bar chart of severity level breakdown
"""

import streamlit as st
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# Add the project's root folder to the system path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.database import get_all_complaints

# Set up the page title
st.set_page_config(page_title="Dashboard - UrbanEye AI", page_icon="📊")

st.title("📊 Complaints Dashboard")

# Step 1: Fetch all complaints from the database
complaints = get_all_complaints()

# Step 2: Check if there are any complaints to show
if len(complaints) == 0:
    st.info("No complaints have been submitted yet. The dashboard will update as complaints come in.")
    st.stop()

# Step 3: Convert the complaints into a Pandas DataFrame for easy analysis
# The columns in the complaints table are:
# id, user_id, image_path, issue_type, confidence, location, severity, status, created_at
column_names = [
    "id", "user_id", "image_path", "issue_type",
    "confidence", "location", "severity", "status", "created_at"
]
complaints_df = pd.DataFrame(complaints, columns=column_names)

# Show some overall numbers at the top of the page
total_complaints = len(complaints_df)
pending_count = len(complaints_df[complaints_df["status"] == "Pending"])
in_progress_count = len(complaints_df[complaints_df["status"] == "In Progress"])
resolved_count = len(complaints_df[complaints_df["status"] == "Resolved"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Complaints", total_complaints)
col2.metric("Pending", pending_count)
col3.metric("In Progress", in_progress_count)
col4.metric("Resolved", resolved_count)

st.divider()

# Chart 1: Bar chart of complaint counts by issue type
st.subheader("Complaints by Issue Type")

issue_counts = complaints_df["issue_type"].value_counts()

fig1, ax1 = plt.subplots()
ax1.bar(issue_counts.index, issue_counts.values, color="steelblue")
ax1.set_xlabel("Issue Type")
ax1.set_ylabel("Number of Complaints")
ax1.set_title("Complaints by Issue Type")
plt.xticks(rotation=30)
st.pyplot(fig1)

st.divider()

# Chart 2: Pie chart of complaint status breakdown
st.subheader("Complaint Status Breakdown")

status_counts = complaints_df["status"].value_counts()

fig2, ax2 = plt.subplots()
ax2.pie(status_counts.values, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
ax2.set_title("Complaint Status Breakdown")
ax2.axis("equal")  # Makes the pie chart a perfect circle
st.pyplot(fig2)

st.divider()

# Chart 3: Bar chart of severity level breakdown
st.subheader("Severity Level Breakdown")

severity_counts = complaints_df["severity"].value_counts()

fig3, ax3 = plt.subplots()
colors_for_severity = {"Low": "green", "Medium": "orange", "High": "red"}
bar_colors = [colors_for_severity.get(level, "gray") for level in severity_counts.index]

ax3.bar(severity_counts.index, severity_counts.values, color=bar_colors)
ax3.set_xlabel("Severity Level")
ax3.set_ylabel("Number of Complaints")
ax3.set_title("Severity Level Breakdown")
st.pyplot(fig3)

st.divider()

# Step 4: Show the full complaints table at the bottom
st.subheader("All Complaints (Raw Data)")
st.dataframe(complaints_df[["id", "issue_type", "confidence", "location", "severity", "status", "created_at"]])
