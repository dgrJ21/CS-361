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

class JobTrackerApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Job Tracker - Sprint 1")  # Window title
        self.root.geometry("900x600")  # Window size: 900 pixels wide, 600 tall
        
        self.applications = load_data(APPLICATIONS_FILE)
        self.contacts = load_data(CONTACTS_FILE)
        
        self.main_frame = ttk.Frame(root)

        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.applications_tab = ttk.Frame(self.notebook)
        self.contacts_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.applications_tab, text="Job Applications")
        self.notebook.add(self.contacts_tab, text="Networking Contacts")
        
        self.build_applications_tab()
        self.build_contacts_tab()

    def build_applications_tab(self):

        header = ttk.Frame(self.applications_tab)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header, text="Job Applications", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        ttk.Button(header, text="+ Add New", command=self.show_add_application_modal).pack(side=tk.RIGHT)
        
        columns = ('company', 'role', 'status', 'date_applied', 'salary', 'last_updated')
        
        self.app_tree = ttk.Treeview(self.applications_tab, columns=columns, show='headings', height=20)
        
        self.app_tree.heading('company', text='Company')
        self.app_tree.heading('role', text='Role')
        self.app_tree.heading('status', text='Status')
        self.app_tree.heading('date_applied', text='Date Applied')
        self.app_tree.heading('salary', text='Salary Range')
        self.app_tree.heading('last_updated', text='Last Updated')
        
        self.app_tree.column('company', width=150)
        self.app_tree.column('role', width=150)
        self.app_tree.column('status', width=150)
        self.app_tree.column('date_applied', width=100)
        self.app_tree.column('salary', width=120)
        self.app_tree.column('last_updated', width=100)

        scrollbar = ttk.Scrollbar(self.applications_tab, orient=tk.VERTICAL, command=self.app_tree.yview)
        self.app_tree.configure(yscrollcommand=scrollbar.set)
        
        self.app_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.app_tree.bind('<Double-1>', self.show_application_detail)

        self.refresh_applications_list()
    
    
    def refresh_applications_list(self):

        for item in self.app_tree.get_children():
            self.app_tree.delete(item)
        
        for app in self.applications:
            self.app_tree.insert('', tk.END, iid=app['id'], values=(
                app['company'],
                app['role'],
                app['status'],
                app['date_applied'],
                app['salary_range'],
                app['last_updated']
            ))