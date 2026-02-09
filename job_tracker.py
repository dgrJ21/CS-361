"""
Job Tracker Application - Sprint 1

User Stories:
1. Log new job application
2. Update existing application
3. Log new networking contact
"""

#library imports needed for code
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

#file to save applications data 
APPLICATIONS_FILE = "applications.json"

#file to save contacts data
CONTACTS_FILE = "contacts.json"

#returns a list of the data in the file path that was passed
def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            return json.load(f)
        
    return []

#saves data in the form of a list to the file path that was passed
def save_data(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=2)


#generates an ID
def generate_id(data_list):
    if not data_list:  # Empty list
        return 1

    return max(item['id'] for item in data_list) + 1



