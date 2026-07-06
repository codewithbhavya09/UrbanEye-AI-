"""
yolo_detector.py
------------------
This file handles loading the YOLOv8 model and running detection
on an uploaded civic issue image.

It uses the Ultralytics YOLO library to detect issues like:
potholes, garbage, water leaks, broken streetlights, and damaged roads.
"""

import os
from ultralytics import YOLO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the path to the YOLO model from .env, or use a default path
MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "assets/yolov8_civic_model.pt")

# Get the minimum confidence score needed to accept a detection
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.4))

# This variable will hold the loaded model so we don't reload it every time
_loaded_model = None


def load_model():
    """
    Loads the YOLOv8 model from disk.
    The model is only loaded once and reused for all future detections.
    """
    global _loaded_model

    if _loaded_model is None:
        _loaded_model = YOLO(MODEL_PATH)

    return _loaded_model


def detect_issue(image_path):
    """
    Runs YOLOv8 detection on the given image.

    Parameters:
    - image_path: string, path to the image file to analyze

    Returns:
    - issue_type: string, the name of the detected issue (e.g. "pothole")
    - confidence_score: float, how confident the model is (between 0 and 1)

    If no issue is detected above the confidence threshold,
    returns ("unknown", 0.0)
    """

    # Load the YOLO model (or reuse it if already loaded)
    model = load_model()

    # Run the model on the image
    results = model(image_path)

    best_issue_type = "unknown"
    best_confidence_score = 0.0

    # Loop through all detected objects in the image
    for result in results:
        boxes = result.boxes

        for box in boxes:
            # Get the confidence score of this detection
            confidence_score = float(box.conf[0])

            # Get the class ID and convert it to a class name
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # Keep track of the detection with the highest confidence
            if confidence_score > best_confidence_score:
                best_confidence_score = confidence_score
                best_issue_type = class_name

    # If the best detection is below our confidence threshold, treat it as unknown
    if best_confidence_score < CONFIDENCE_THRESHOLD:
        return "unknown", 0.0

    return best_issue_type, best_confidence_score
