"""
image_utils.py
---------------
This file contains helper functions to save and load images
that users upload when reporting a civic issue.
"""

import os
from datetime import datetime
from PIL import Image

# Folder where uploaded complaint images will be stored
UPLOAD_FOLDER = "assets/uploaded_images"


def save_uploaded_image(uploaded_file, username):
    """
    Saves an uploaded Streamlit image file to disk and returns the file path.

    Parameters:
    - uploaded_file: the file object returned by st.file_uploader
    - username: the name of the user uploading the image (used in the filename)

    Returns:
    - image_path: string, the path where the image was saved
    """

    # Create the upload folder if it does not already exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Create a unique filename using the username and current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = uploaded_file.name.split(".")[-1]
    file_name = f"{username}_{timestamp}.{file_extension}"

    # Build the full path where the image will be saved
    image_path = os.path.join(UPLOAD_FOLDER, file_name)

    # Open the uploaded file using PIL and save it to the folder
    image = Image.open(uploaded_file)
    image.save(image_path)

    return image_path


def load_image(image_path):
    """
    Loads an image from disk using PIL and returns it.
    Used to display previously saved complaint images.
    """
    image = Image.open(image_path)
    return image
