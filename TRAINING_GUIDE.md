# Training a Custom YOLOv8 Model for Civic Issues

This guide explains, in simple steps, how to train your own YOLOv8 model
to detect civic issues such as potholes, garbage, water leaks,
broken streetlights, and damaged roads.

---

## Step 1: Collect Images

Gather images for each issue type you want to detect. For example:
- Potholes
- Garbage piles
- Water leaks
- Broken streetlights
- Damaged roads

You can:
- Take your own photos
- Use free datasets from sites like Kaggle or Roboflow Universe
- Search "pothole dataset", "garbage detection dataset", etc.

Aim for at least 100–200 images per category for a basic working model.

---

## Step 2: Label the Images

Each image needs bounding boxes drawn around the issue, along with a label
(e.g. "pothole"). You can use free tools such as:

- **Roboflow** (https://roboflow.com) – easiest for beginners, works in browser
- **LabelImg** – a free desktop tool for drawing bounding boxes
- **CVAT** – another free browser-based labeling tool

These tools export labels in YOLO format automatically.

---

## Step 3: Organize Your Dataset

YOLOv8 expects your dataset in this folder structure:
