# UrbanEye-AI-
# UrbanEye AI – Intelligent Civic Issue Detection and Resolution Platform

UrbanEye AI is a beginner-friendly web application that helps citizens report civic issues
such as potholes, garbage, water leaks, broken streetlights, and damaged roads.
The app uses YOLOv8 to automatically detect the issue from an uploaded photo,
calculates a severity level, and stores the complaint in a database so it can be tracked
until it is resolved.

---

## Features

- User Registration and Login (SQLite based)
- Upload a photo of a civic issue
- Automatic issue detection using YOLOv8 (potholes, garbage, water leaks, broken streetlights, damaged roads)
- Confidence score shown for every detection
- Manual location entry
- Automatic severity level calculation (Low, Medium, High)
- Complaint storage in SQLite database
- Complaint history view for each user
- Complaint status tracking (Pending, In Progress, Resolved)
- Dashboard with Matplotlib charts (issue counts, status breakdown, severity breakdown)

---

## Tech Stack

| Purpose            | Technology       |
|--------------------|------------------|
| Frontend           | Streamlit        |
| Database           | SQLite           |
| Object Detection   | YOLOv8 (Ultralytics) |
| Image Processing   | OpenCV           |
| Data Handling      | Pandas, NumPy    |
| Charts             | Matplotlib       |
| Config Management  | python-dotenv    |
| HTTP Requests      | Requests         |

---

## Project Structure
