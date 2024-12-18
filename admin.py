import customtkinter as ctk
from PIL import Image
import sqlite3
from tkinter import ttk

def admin_page(root):
    
    

    def check_mood_status():

        if ctk.get_appearance_mode() == "Dark":
            style = ttk.Style()
            style.theme_use("clam")  
            style.configure("Treeview", 
                            background="#2b2b2b", 
                            foreground="white", 
                            rowheight=25, 
                            fieldbackground="#2b2b2b", 
                            font=("Arial", 14))  
            style.map("Treeview", background=[("selected", "#4CAF50")])
            style.configure("Treeview.Heading", 
                            background="#212121", 
                            foreground="white", 
                            font=("Arial", 16))   
            style.map("Treeview.Heading", background=[("active", "#212121")])
            admin_label.configure(text_color="white")

        else:

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview", 
                            background="#FFFFFF",  
                            foreground="#000000",  
                            rowheight=25, 
                            fieldbackground="#FFFFFF",  
                            font=("Arial", 14))  
            style.map("Treeview", background=[("selected", "#4CAF50")])  

            style.configure("Treeview.Heading", 
                            background="#F1F1F1",  
                            foreground="#000000",  
                            font=("Arial", 16))   
            style.map("Treeview.Heading", background=[("active", "#F1F1F1")])  
            admin_label.configure(text_color="black")




    
    
    exit_icon = Image.open("images/exit.png") 

    exit_photo = ctk.CTkImage(light_image=exit_icon, dark_image=exit_icon, size=(30, 30))
    exit_button = ctk.CTkButton(
        master=root,
        text="",
        width=25,
        height=30,
        font=("Arial", 16),
        image=exit_photo,
        command=root.quit
    )
    exit_button.place(relx=0.03, rely=0.03, anchor="nw")

    admin_label = ctk.CTkLabel(
        master=root,
        text="Administrator",
        font=("Arial", 24, "bold"),
        text_color="white"
    )
    admin_label.place(relx=0.5, rely=0.03, anchor="n")

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employee (
        Employee_ID INTEGER PRIMARY KEY,
        First_name TEXT NOT NULL,
        Last_name TEXT NOT NULL,
        Email TEXT,
        Manager_ID INTEGER,
        FOREIGN KEY (Manager_ID) REFERENCES Employee(Employee_ID)
    )
    """)
    conn.commit()

    def update_status(message, color="red"):
        status_label.configure(text=message, text_color=color, font=("Arial", 14))

    def add_or_update_employee():
        First_name = First_name_var.get()
        Last_name = Last_name_var.get()
        Email = Email_var.get()
        Manager_ID = Manager_ID_var.get() or None  

        if not (First_name and Last_name and Email):
            update_status("Error: First Name, Last Name, and Email are required.", "red")
            return

        if Manager_ID:
            cursor.execute("SELECT Employee_ID FROM Employee WHERE Employee_ID =?", (Manager_ID,))
            if not cursor.fetchone():
                update_status("Error: Invalid Manager ID.", "red")
                return

        try:
            if selected_Employee_ID.get():
                cursor.execute("""
                    UPDATE Employee 
                    SET First_name=?, Last_name=?, Email=?, Manager_ID=?
                    WHERE Employee_ID=?
                """, (First_name, Last_name, Email, Manager_ID, selected_Employee_ID.get()))
                update_status("Employee updated successfully!", "green")
            else:
                cursor.execute("""
                    INSERT INTO Employee (First_name, Last_name, Email, Manager_ID) 
                    VALUES (?, ?, ?, ?)
                """, (First_name, Last_name, Email, Manager_ID))
                update_status("Employee added successfully!", "green")

            conn.commit()
            First_name_var.set("")
            Last_name_var.set("")
            Email_var.set("")
            Manager_ID_var.set("1")
            search_var.set("")
            selected_Employee_ID.set("")
            display_employees()
        except sqlite3.IntegrityError:
            update_status("Error: Email must be unique.", "red")

    def edit_employee():
        selected_item = tree.focus()
        if not selected_item:
            update_status("Error: No employee selected.", "red")
            return

        values = tree.item(selected_item, "values")
        selected_Employee_ID.set(values[0])
        First_name_var.set(values[1])
        Last_name_var.set(values[2])
        Email_var.set(values[3])
        Manager_ID_var.set(values[4] if values[4] != "None" else "")


    def delete_employee():
        selected_item = tree.focus()
        if not selected_item:
            update_status("Error: No employee selected.", "red")
            return

        employee_id = tree.item(selected_item)["values"][0]

        # Connect to the database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        
        #foreign key constraints 
        cursor.execute("PRAGMA foreign_keys = ON;")

        try:
            cursor.execute("DELETE FROM Employee WHERE Employee_ID=?", (employee_id,))
            
            conn.commit()

            update_status("Employee deleted successfully!", "green")
            
            # Refresh the display of employees
            display_employees()

        except sqlite3.IntegrityError as e:
            # Handle foreign key constraint 
            update_status(f"Error: {e}", "red")
        
        finally:
            conn.close()

    def search_employee():
        search_term = search_var.get()
        if not search_term:
            update_status("Error: Please enter a term to search.", "red")
            return

        cursor.execute("""
            SELECT * FROM Employee 
            WHERE First_name LIKE ? OR Last_name LIKE ? OR Email LIKE ? OR Manager_ID LIKE ? OR Employee_ID LIKE ?
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        rows = cursor.fetchall()
        update_tree(rows)
        update_status(f"Search complete: {len(rows)} result(s) found.", "green")

    def display_employees():
        cursor.execute("SELECT * FROM Employee")
        rows = cursor.fetchall()
        update_tree(rows)

    def update_tree(rows):
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", "end", values=row)

    def clear_fields():
        First_name_var.set("")
        Last_name_var.set("")
        Email_var.set("")
        Manager_ID_var.set("1")
        search_var.set("")
        selected_Employee_ID.set("")
        update_status("Fields cleared.", "green")

    def clear_search():
        search_var.set("")
        display_employees()
        update_status("Search cleared.", "green")

    First_name_var = ctk.StringVar()
    Last_name_var = ctk.StringVar()
    Email_var = ctk.StringVar()
    Manager_ID_var = ctk.StringVar(value="1")
    search_var = ctk.StringVar()
    selected_Employee_ID = ctk.StringVar()

    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.place(relx=0.5, rely=0.56, anchor="center")

    ctk.CTkLabel(frame, text="First Name:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    ctk.CTkEntry(frame, textvariable=First_name_var, font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(frame, text="Last Name:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    ctk.CTkEntry(frame, textvariable=Last_name_var, font=("Arial", 14)).grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(frame, text="Email:", font=("Arial", 14)).grid(row=0, column=2, padx=10, pady=10, sticky="e")
    ctk.CTkEntry(frame, textvariable=Email_var, font=("Arial", 14)).grid(row=0, column=3, padx=10, pady=10)

    ctk.CTkLabel(frame, text="Manager ID:", font=("Arial", 14)).grid(row=1, column=2, padx=10, pady=10, sticky="e")
    ctk.CTkEntry(frame, textvariable=Manager_ID_var, font=("Arial", 14)).grid(row=1, column=3, padx=10, pady=10)

    ctk.CTkButton(frame, text="Add/Save", font=("Arial", 14), command=add_or_update_employee).grid(row=2, column=0, padx=10, pady=10)
    ctk.CTkButton(frame, text="Edit", font=("Arial", 14), command=edit_employee).grid(row=2, column=1, padx=10, pady=10)
    ctk.CTkButton(frame, text="Clear Fields", font=("Arial", 14), command=clear_fields).grid(row=2, column=2, padx=10, pady=10)
    ctk.CTkButton(frame, text="Delete", font=("Arial", 14), command=delete_employee).grid(row=2, column=3, padx=10, pady=10)

    status_label = ctk.CTkLabel(frame, text="", font=("Arial", 12), text_color="red")
    status_label.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    ctk.CTkEntry(frame, textvariable=search_var, placeholder_text="Search...", font=("Arial", 18)).grid(row=4, column=0, padx=10, pady=10, columnspan=2, sticky="ew")    
    ctk.CTkButton(frame, text="Search", font=("Arial", 14), command=search_employee).grid(row=4, column=2, padx=10, pady=10)
    ctk.CTkButton(frame, text="Clear Search", font=("Arial", 14), command=clear_search).grid(row=4, column=3, padx=10, pady=10)

    tree_frame = ctk.CTkFrame(frame)
    tree_frame.grid(row=5, column=0, columnspan=5, padx=10, pady=20, sticky="nsew")

    columns = ("Employee ID", "First Name", "Last Name", "Email", "Manager ID")

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)


    for col in columns:
        tree.heading(col, text=col)
        if col == "Email":
            tree.column(col, width=300)
        elif col == "Employee ID":
            tree.column(col, width=80)
        else:
            tree.column(col, width=150)

    tree.pack(fill="both", expand=True)
    check_mood_status()
    display_employees()
