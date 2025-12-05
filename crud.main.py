# main.py
"""
Entry point for the Quiz CRUD Application (Project 2).
This file imports the CRUD UI module and starts the main window.
"""

from crud_ui import run_crud_app  # impo



 rt the main window function from CRUD interface

def main():
    """Start the CRUD interface window."""
    run_crud_app()  # call the GUI function that creates and runs the Tkinter window

if __name__ == "__main__":  # check if this file is executed as the main script
    main()  # execute the main function to start the app
