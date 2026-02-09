
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

APPLICATIONS_FILE = "applications.json"
CONTACTS_FILE = "contacts.json"

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []


def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def generate_id(data_list):
    if not data_list:
        return 1
    return max(item['id'] for item in data_list) + 1

class JobTrackerApp:
    """Main application class - holds all app data and functions together."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Job Tracker - Sprint 1")
        self.root.geometry("900x600")
        
        self.applications = load_data(APPLICATIONS_FILE)
        self.contacts = load_data(CONTACTS_FILE)
        
        self.status_options = ["Applied", "Interviewing", "Offer", "Rejected", "Withdrawn"]
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        welcome_frame = ttk.Frame(self.main_frame)
        welcome_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(welcome_frame, 
                  text="Track your job applications and networking contacts in one place. Double-click any row to view details.",
                  font=('Arial', 10), foreground='gray').pack(anchor=tk.W)
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.applications_tab = ttk.Frame(self.notebook)
        self.contacts_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.applications_tab, text="Job Applications")
        self.notebook.add(self.contacts_tab, text="Networking Contacts")
        
        self.build_applications_tab()
        self.build_contacts_tab()
        
        self.root.bind('<Control-n>', lambda e: self.add_new_shortcut())  # Ctrl+N to add new
        self.root.bind('<Control-q>', lambda e: self.root.quit())  # Ctrl+Q to quit
    
    
    def add_new_shortcut(self):
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:  
            self.show_add_application_modal()
        else:
            self.show_add_contact_modal()
    
    def build_applications_tab(self):
        """Build the Job Applications list view."""
        header = ttk.Frame(self.applications_tab)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header, text="Job Applications", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        add_btn = ttk.Button(header, text="+ Add New (Ctrl+N)", command=self.show_add_application_modal)
        add_btn.pack(side=tk.RIGHT)
        
        ttk.Button(header, text="⚙ Add Status", command=self.add_custom_status).pack(side=tk.RIGHT, padx=(0, 5))
        
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
        self.app_tree.column('status', width=100)
        self.app_tree.column('date_applied', width=100)
        self.app_tree.column('salary', width=120)
        self.app_tree.column('last_updated', width=120)
        
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
    
    
    def add_custom_status(self):
        new_status = simpledialog.askstring("Add Custom Status", 
                                            "Enter a new status option:",
                                            parent=self.root)
        if new_status and new_status.strip():
            new_status = new_status.strip()
            if new_status not in self.status_options:
                self.status_options.append(new_status)
                messagebox.showinfo("Success", f"Status '{new_status}' added!")
            else:
                messagebox.showinfo("Info", f"Status '{new_status}' already exists.")
    
    
    def show_add_application_modal(self):
        modal = tk.Toplevel(self.root)
        modal.title("Add New Application")
        modal.geometry("400x500")
        modal.transient(self.root)
        modal.grab_set()
        modal.geometry("+%d+%d" % (self.root.winfo_x() + 250, self.root.winfo_y() + 50))
        
        ttk.Label(modal, text="Add New Application", font=('Arial', 14, 'bold')).pack(pady=(20, 5))
        ttk.Label(modal, text="Track a new job you've applied to", 
                  font=('Arial', 9), foreground='gray').pack(pady=(0, 15))
        
        form_frame = ttk.Frame(modal)
        form_frame.pack(padx=30, fill=tk.X)
        
        ttk.Label(form_frame, text="Company Name *").pack(anchor=tk.W)
        company_var = tk.StringVar()
        company_entry = ttk.Entry(form_frame, textvariable=company_var, width=40)
        company_entry.pack(fill=tk.X, pady=(0, 10))
        company_entry.focus()  # Start with cursor here
        
        ttk.Label(form_frame, text="Job Title *").pack(anchor=tk.W)
        title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=title_var, width=40).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Salary Range").pack(anchor=tk.W)
        salary_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=salary_var, width=40).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Application Date").pack(anchor=tk.W)
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form_frame, textvariable=date_var, width=40).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Status").pack(anchor=tk.W)
        status_var = tk.StringVar(value="Applied")
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, width=37, values=self.status_options)
        status_combo.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Notes").pack(anchor=tk.W)
        notes_text = tk.Text(form_frame, height=3, width=40)
        notes_text.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = ttk.Frame(modal)
        button_frame.pack(pady=20)
        
        def save_application():
            if not company_var.get().strip():
                messagebox.showerror("Error", "Company Name is required")
                return
            if not title_var.get().strip():
                messagebox.showerror("Error", "Job Title is required")
                return
            
            new_app = {
                'id': generate_id(self.applications),
                'company': company_var.get().strip(),
                'role': title_var.get().strip(),
                'salary_range': salary_var.get().strip(),
                'date_applied': date_var.get().strip(),
                'status': status_var.get(),
                'notes': notes_text.get("1.0", tk.END).strip(),
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            self.applications.append(new_app)
            save_data(APPLICATIONS_FILE, self.applications)
            self.refresh_applications_list()
            
            full_path = os.path.abspath(APPLICATIONS_FILE)
            messagebox.showinfo("Success", f"Application saved!\n\nData stored in:\n{full_path}")
            modal.destroy()
        
        def cancel():
            has_data = (company_var.get().strip() or title_var.get().strip() or 
                       notes_text.get("1.0", tk.END).strip())
            if has_data:
                if messagebox.askyesno("Discard Changes?", 
                                       "You have unsaved changes. Are you sure you want to close?"):
                    modal.destroy()
            else:
                modal.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_application).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)
        
        modal.bind('<Return>', lambda e: save_application())  # Enter to save
        modal.bind('<Escape>', lambda e: cancel())  # Escape to cancel
        
        modal.protocol("WM_DELETE_WINDOW", cancel)
    
    
    def show_application_detail(self, event=None):
        selection = self.app_tree.selection()
        if not selection:
            return
        
        app_id = int(selection[0])
        app = next((a for a in self.applications if a['id'] == app_id), None)
        if not app:
            return
        
        detail = tk.Toplevel(self.root)
        detail.title(f"Application - {app['company']}")
        detail.geometry("450x550")
        detail.transient(self.root)
        detail.grab_set()
        detail.geometry("+%d+%d" % (self.root.winfo_x() + 225, self.root.winfo_y() + 25))
        
        header = ttk.Frame(detail)
        header.pack(fill=tk.X, padx=20, pady=(15, 10))
        ttk.Button(header, text="← Back", command=detail.destroy).pack(side=tk.LEFT)
        ttk.Label(header, text="Application Details", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=20)
        
        form_frame = ttk.Frame(detail)
        form_frame.pack(padx=30, fill=tk.X, pady=10)
        
        ttk.Label(form_frame, text="Company Name *").pack(anchor=tk.W)
        company_var = tk.StringVar(value=app['company'])
        ttk.Entry(form_frame, textvariable=company_var, width=45).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Job Title *").pack(anchor=tk.W)
        title_var = tk.StringVar(value=app['role'])
        ttk.Entry(form_frame, textvariable=title_var, width=45).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Salary Range").pack(anchor=tk.W)
        salary_var = tk.StringVar(value=app['salary_range'])
        ttk.Entry(form_frame, textvariable=salary_var, width=45).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Application Date").pack(anchor=tk.W)
        date_var = tk.StringVar(value=app['date_applied'])
        ttk.Entry(form_frame, textvariable=date_var, width=45).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Status").pack(anchor=tk.W)
        status_var = tk.StringVar(value=app['status'])
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, width=42, values=self.status_options)
        status_combo.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Notes").pack(anchor=tk.W)
        notes_text = tk.Text(form_frame, height=4, width=45)
        notes_text.insert("1.0", app.get('notes', ''))
        notes_text.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Last Updated").pack(anchor=tk.W)
        ttk.Label(form_frame, text=app['last_updated'], foreground='gray').pack(anchor=tk.W, pady=(0, 10))
        
        def update_application():
            if not company_var.get().strip():
                messagebox.showerror("Error", "Company Name is required")
                return
            if not title_var.get().strip():
                messagebox.showerror("Error", "Job Title is required")
                return
            
            app['company'] = company_var.get().strip()
            app['role'] = title_var.get().strip()
            app['salary_range'] = salary_var.get().strip()
            app['date_applied'] = date_var.get().strip()
            app['status'] = status_var.get()
            app['notes'] = notes_text.get("1.0", tk.END).strip()
            app['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            save_data(APPLICATIONS_FILE, self.applications)
            self.refresh_applications_list()
            messagebox.showinfo("Success", "Application updated!")
            detail.destroy()
        
        ttk.Button(detail, text="Update", command=update_application).pack(pady=15)
        
        detail.bind('<Return>', lambda e: update_application())
        detail.bind('<Escape>', lambda e: detail.destroy())
        
    def build_contacts_tab(self):
        header = ttk.Frame(self.contacts_tab)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header, text="Networking Contacts", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header, text="+ Add New (Ctrl+N)", command=self.show_add_contact_modal).pack(side=tk.RIGHT)
        
        columns = ('name', 'company', 'role', 'relationship', 'last_updated')
        self.contact_tree = ttk.Treeview(self.contacts_tab, columns=columns, show='headings', height=20)
        
        self.contact_tree.heading('name', text='Name')
        self.contact_tree.heading('company', text='Company')
        self.contact_tree.heading('role', text='Role')
        self.contact_tree.heading('relationship', text='Relationship')
        self.contact_tree.heading('last_updated', text='Last Updated')
        
        self.contact_tree.column('name', width=150)
        self.contact_tree.column('company', width=150)
        self.contact_tree.column('role', width=150)
        self.contact_tree.column('relationship', width=120)
        self.contact_tree.column('last_updated', width=120)
        
        scrollbar = ttk.Scrollbar(self.contacts_tab, orient=tk.VERTICAL, command=self.contact_tree.yview)
        self.contact_tree.configure(yscrollcommand=scrollbar.set)
        
        self.contact_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.contact_tree.bind('<Double-1>', self.show_contact_detail)
        self.refresh_contacts_list()
    
    
    def refresh_contacts_list(self):
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        
        for contact in self.contacts:
            self.contact_tree.insert('', tk.END, iid=contact['id'], values=(
                contact['name'],
                contact['company'],
                contact['role'],
                contact['relationship'],
                contact['last_updated']
            ))
    
    
    def show_add_contact_modal(self):
        modal = tk.Toplevel(self.root)
        modal.title("Add New Contact")
        modal.geometry("400x450")
        modal.transient(self.root)
        modal.grab_set()
        modal.geometry("+%d+%d" % (self.root.winfo_x() + 250, self.root.winfo_y() + 75))
        
        ttk.Label(modal, text="Add New Contact", font=('Arial', 14, 'bold')).pack(pady=(20, 5))
        ttk.Label(modal, text="Save a networking contact for your job search", 
                  font=('Arial', 9), foreground='gray').pack(pady=(0, 15))
        
        form_frame = ttk.Frame(modal)
        form_frame.pack(padx=30, fill=tk.X)
        
        ttk.Label(form_frame, text="Name *").pack(anchor=tk.W)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=40)
        name_entry.pack(fill=tk.X, pady=(0, 10))
        name_entry.focus()
        
        ttk.Label(form_frame, text="Company").pack(anchor=tk.W)
        company_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=company_var, width=40).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Job Title").pack(anchor=tk.W)
        title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=title_var, width=40).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Relationship").pack(anchor=tk.W)
        relationship_var = tk.StringVar(value="New Connection")
        relationship_combo = ttk.Combobox(form_frame, textvariable=relationship_var, width=37,
                                           values=["New Connection", "Had Coffee Chat", "Warm Contact", 
                                                   "Referral Source", "Close Contact"])
        relationship_combo.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Notes").pack(anchor=tk.W)
        notes_text = tk.Text(form_frame, height=3, width=40)
        notes_text.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = ttk.Frame(modal)
        button_frame.pack(pady=20)
        
        def save_contact():
            if not name_var.get().strip():
                messagebox.showerror("Error", "Name is required")
                return
            
            new_contact = {
                'id': generate_id(self.contacts),
                'name': name_var.get().strip(),
                'company': company_var.get().strip(),
                'role': title_var.get().strip(),
                'relationship': relationship_var.get(),
                'notes': notes_text.get("1.0", tk.END).strip(),
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            self.contacts.append(new_contact)
            save_data(CONTACTS_FILE, self.contacts)
            self.refresh_contacts_list()
            
            full_path = os.path.abspath(CONTACTS_FILE)
            messagebox.showinfo("Success", f"Contact saved!\n\nData stored in:\n{full_path}")
            modal.destroy()
        
        def cancel():
            has_data = (name_var.get().strip() or company_var.get().strip() or 
                       notes_text.get("1.0", tk.END).strip())
            if has_data:
                if messagebox.askyesno("Discard Changes?", 
                                       "You have unsaved changes. Are you sure you want to close?"):
                    modal.destroy()
            else:
                modal.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)
        
        modal.bind('<Return>', lambda e: save_contact())
        modal.bind('<Escape>', lambda e: cancel())
        modal.protocol("WM_DELETE_WINDOW", cancel)
    
    
    def show_contact_detail(self, event=None):
        selection = self.contact_tree.selection()
        if not selection:
            return
        
        contact_id = int(selection[0])
        contact = next((c for c in self.contacts if c['id'] == contact_id), None)
        if not contact:
            return
        
        detail = tk.Toplevel(self.root)
        detail.title(f"Contact - {contact['name']}")
        detail.geometry("400x450")
        detail.transient(self.root)
        detail.grab_set()
        detail.geometry("+%d+%d" % (self.root.winfo_x() + 250, self.root.winfo_y() + 75))
        
        header = ttk.Frame(detail)
        header.pack(fill=tk.X, padx=20, pady=(15, 10))
        ttk.Button(header, text="← Back", command=detail.destroy).pack(side=tk.LEFT)
        ttk.Label(header, text="Contact Details", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=20)
        
        form_frame = ttk.Frame(detail)
        form_frame.pack(padx=30, fill=tk.X, pady=10)
        
        ttk.Label(form_frame, text="Name", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(form_frame, text=contact['name']).pack(anchor=tk.W)
        
        ttk.Label(form_frame, text="Company", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(form_frame, text=contact['company'] or "—").pack(anchor=tk.W)
        
        ttk.Label(form_frame, text="Job Title", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(form_frame, text=contact['role'] or "—").pack(anchor=tk.W)
        
        ttk.Label(form_frame, text="Relationship", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(form_frame, text=contact['relationship']).pack(anchor=tk.W)
        
        ttk.Label(form_frame, text="Notes", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(form_frame, text=contact.get('notes', '') or "—", wraplength=300).pack(anchor=tk.W)
        
        ttk.Label(form_frame, text="Last Updated", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(form_frame, text=contact['last_updated'], foreground='gray').pack(anchor=tk.W)
        
        ttk.Label(detail, text="(Editing contacts will be available in Sprint 2)", 
                  foreground='gray', font=('Arial', 9, 'italic')).pack(pady=20)
        
        detail.bind('<Escape>', lambda e: detail.destroy())


if __name__ == "__main__":
    root = tk.Tk()
    app = JobTrackerApp(root)
    root.mainloop()