"""
main.py
--------
This is the setup entry point for UrbanEye AI.
Running this file will:
1. Create the required folders (database, assets) if they do not exist.
2. Create the SQLite database and tables.

After running this file, start the actual web app using:
    streamlit run app/Home.py
"""

import os
from database.database import create_tables


def setup_folders():
    """
    Creates the folders needed by the project if they are missing.
    """
    folders_needed = ["database", "assets", "screenshots"]

    for folder in folders_needed:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")


def main():
    """
    Runs all the setup steps for the UrbanEye AI project.
    """
    print("Setting up UrbanEye AI project...")

    # Step 1: Make sure all required folders exist
    setup_folders()

    # Step 2: Create the SQLite database and tables
    create_tables()
    print("Database and tables created successfully.")

    print("\nSetup complete!")
    print("Now run the app using this command:")
    print("    streamlit run app/Home.py")


# This makes sure main() only runs when this file is executed directly
if __name__ == "__main__":
    main()
