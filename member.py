import customtkinter as ctk
import sqlite3
from tkinter import ttk
import re
from PIL import Image

def create_member_window(root, menu_frame, employee_id_value):
    from menu import create_menu_window
    def check_mood_status():

        if ctk.get_appearance_mode() == "Dark":
            style = ttk.Style()
            style.theme_use("clam")  
            style.configure("Treeview", 
                            background="#2b2b2b", 
                            foreground="white", 
                            rowheight=25, 
                            fieldbackground="#2b2b2b", 
                            font=("Arial", 12))  
            style.map("Treeview", background=[("selected", "#4CAF50")])
            style.configure("Treeview.Heading", 
                            background="#212121", 
                            foreground="white", 
                            font=("Arial", 14))   
            style.map("Treeview.Heading", background=[("active", "#212121")])
            title.configure(text_color="white")

        else:

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview", 
                            background="#FFFFFF",  
                            foreground="#000000",  
                            rowheight=25, 
                            fieldbackground="#FFFFFF",  
                            font=("Arial", 12))  
            style.map("Treeview", background=[("selected", "#4CAF50")])  

            style.configure("Treeview.Heading", 
                            background="#F1F1F1",  
                            foreground="#000000",  
                            font=("Arial", 14))   
            style.map("Treeview.Heading", background=[("active", "#F1F1F1")])  
            title.configure(text_color="black")


    def database():
        con = sqlite3.connect('library.db')
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Member (
                Member_ID INTEGER PRIMARY KEY,
                First_name TEXT NOT NULL,
                Last_name TEXT NOT NULL,
                Address TEXT,
                Phone TEXT,
                Email TEXT,
                Employee_ID INTEGER,
                FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
            )
        """)
        con.commit()
        con.close()

    database()
 
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def clear_fields():
        for entry in entries.values():
            entry.delete(0, "end")

    def load_members():
        for child in tree.get_children():
            tree.delete(child)

        con = sqlite3.connect('library.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM Member ORDER BY First_name")
        rows = cur.fetchall()
        con.close()

        for row in rows:
            tree.insert("", "end", values=row)   

    def populate_employee_id():
        """Populate Employee ID if Member ID exists in the database."""
        member_id = member_id_entry.get()
        if not member_id:
            return

        try:
            con = sqlite3.connect('library.db')
            cur = con.cursor()
            cur.execute("SELECT Employee_ID FROM Member WHERE Member_ID = ?", (member_id,))
            result = cur.fetchone()
            con.close()

            if result:
                entries["Employee ID"].delete(0, "end")
                entries["Employee ID"].insert(0, result[0]) 
        except Exception as e:
            print("")

   
    def add_member():
        member_id = member_id_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()

        
        if not member_id or not first_name or not last_name or not email:
            status_label.configure(text="Error: Required fields missing!", text_color="red")
            return

        if not is_valid_email(email):
            status_label.configure(text="Error: Invalid email format!", text_color="red")
            return

        if not phone.isdigit():
            status_label.configure(text="Error: Phone number should contain only digits!", text_color="red")
            return

        try:
            con = sqlite3.connect('library.db')
            cur = con.cursor()
            cur.execute("""
                INSERT INTO Member (Member_ID, First_name, Last_name, Address, Phone, Email, Employee_ID)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (member_id, first_name, last_name, address, phone, email, employee_id_value))
            con.commit()
            status_label.configure(text="Success: Member added successfully!", text_color="green")
            load_members()
            clear_fields()
        except sqlite3.IntegrityError:
            status_label.configure(text="Error: Member ID or Email already exists!", text_color="red")
        except Exception as e:
            status_label.configure(text=f"Error: {e}", text_color="red")
        finally:
            if con:
                con.close()


    def update_member():
        selected = tree.focus()
        if not selected:
            print("Error: Please select a member to update!")
            return

        member_id = tree.item(selected)["values"][0]
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()

        if not first_name or not last_name or not email:
            print("Error: First Name, Last Name, and Email are required!")
            return

        try:
            con = sqlite3.connect('library.db')
            cur = con.cursor()
            cur.execute("""
                UPDATE Member
                SET First_name = ?, Last_name = ?, Address = ?, Phone = ?, Email = ?, Employee_ID = ?
                WHERE Member_ID = ?
            """, (first_name, last_name, address, phone, email, employee_id_value, member_id))
            con.commit()
            print("Success: Member updated successfully!")
            load_members()
            clear_fields()
        except Exception as e:
            print(f"Error updating member: {e}")
        finally:
            if con:
                con.close()

    def delete_member():
        selected = tree.focus()
        if not selected:
            status_label.configure(text="Error: Please select a member to delete!", text_color="red")
            return

        member_id = tree.item(selected)["values"][0]

        try:
       
            con = sqlite3.connect('library.db')
            cur = con.cursor()

            
            cur.execute("PRAGMA foreign_keys = ON;")

           
            cur.execute("DELETE FROM Member WHERE Member_ID = ?", (member_id,))
            
            
            con.commit()

            
            status_label.configure(text="Success: Member deleted successfully!", text_color="green")

            
            load_members()

            
            clear_fields()

        except sqlite3.IntegrityError as e:
            
            status_label.configure(text=f"Error: {e}", text_color="red")
        
        except Exception as e:
            
            status_label.configure(text=f"Error: {e}", text_color="red")

        finally:
            
            if con:
                con.close()

    def clear_status():
        status_label.configure(text="")

        status_label.after(3000, clear_status)              

    def search_anything():
        search_term = universal_search_entry.get().strip()
        if not search_term:
            print("Error: Please enter a Member ID!")
            return

        if not search_term.isdigit():
            print("Error: Member ID should only contain digits!")
            return

       
        for child in tree.get_children():
            tree.delete(child)

       
        con = sqlite3.connect('library.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM Member WHERE Member_ID = ?", (search_term,))
        rows = cur.fetchall()
        con.close()

         
        if not rows:
            print("Search: No member found with the given Member ID.")
        else:
            for row in rows:
                tree.insert("", "end", values=row)

    def clear_search():
        """Clear the search field and reload all members."""
        universal_search_entry.delete(0, "end")  
        load_members()  

    def go_back():
        create_menu_window(root, employee_id_value)
        tree_frame.destroy()
        frame_2.destroy()

    def on_tree_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, "values")
            member_id_entry.delete(0, "end")
            member_id_entry.insert(0, values[0])
            first_name_entry.delete(0, "end")
            first_name_entry.insert(0, values[1])
            last_name_entry.delete(0, "end")
            last_name_entry.insert(0, values[2])
            address_entry.delete(0, "end")
            address_entry.insert(0, values[3])
            phone_entry.delete(0, "end")
            phone_entry.insert(0, values[4])
            email_entry.delete(0, "end")
            email_entry.insert(0, values[5])

            
            populate_employee_id()

   

    frame_2 = ctk.CTkFrame(master=root)
    frame_2.place(relx=0, rely=0, relwidth=1, relheight=1)

    title = ctk.CTkLabel(frame_2, text="Member Management", font=("Arial", 20 , "bold"))
    title.pack(pady=10)

   


    form_frame = ctk.CTkFrame(frame_2)
    form_frame.pack(fill="x", padx=70, pady=20)

    
    back_image = Image.open("images/back.png")
    back_photo = ctk.CTkImage(light_image=back_image, dark_image=back_image, size=(30, 30))
    back_button = ctk.CTkButton(
        master=frame_2,
        text="",
        width=25,
        height=30,
        font=("Arial", 16),
        image=back_photo,
        command=go_back
    )
    back_button.place(x=20, y=20)
    
    fields = ["Member ID", "First Name", "Last Name", "Address", "Phone", "Email"]
    entries = {}
    for i, field in enumerate(fields):
        label = ctk.CTkLabel(form_frame, text=field)
        label.grid(row=i // 3 * 2, column=i % 3, padx=30, pady=5, sticky="w") 
        entry = ctk.CTkEntry(form_frame)
        entry.grid(row=i // 3 * 2 + 1, column=i % 3, padx=30, pady=5, sticky="ew")  
        entries[field] = entry
    status_label = ctk.CTkLabel(frame_2, text="", font=("Arial", 14), text_color="green")
    status_label.pack(fill="x", padx=20, pady=5)

    member_id_entry = entries["Member ID"]
    first_name_entry = entries["First Name"]
    last_name_entry = entries["Last Name"]
    address_entry = entries["Address"]
    phone_entry = entries["Phone"]
    email_entry = entries["Email"]

    member_id_entry.bind("<FocusOut>", lambda event: populate_employee_id())

   

    btn_frame = ctk.CTkFrame(frame_2)
    btn_frame.pack(fill="x", pady=10,padx=70)

    add_btn = ctk.CTkButton(btn_frame, text="Add", command=add_member)
    add_btn.grid(row=0, column=0, padx=50)

    update_btn = ctk.CTkButton(btn_frame, text="Update", command=update_member)
    update_btn.grid(row=0, column=1, padx=10)

    delete_btn = ctk.CTkButton(btn_frame, text="Delete", command=delete_member)
    delete_btn.grid(row=0, column=2, padx=10)

    search_frame = ctk.CTkFrame(frame_2)
    search_frame.pack(fill="x", padx=70, pady=10)

    universal_search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search Member ID...")
    universal_search_entry.grid(row=0, column=0, padx=50, pady=5, sticky="ew")

    
    search_btn = ctk.CTkButton(search_frame, text="Search", command=search_anything)
    search_btn.grid(row=0, column=1, padx=10, pady=5)

     
    clear_search_btn = ctk.CTkButton(search_frame, text="Clear Search", command=clear_search)
    clear_search_btn.grid(row=0, column=2, padx=10, pady=5)


    tree_frame = ctk.CTkFrame(frame_2)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("Member ID", "First Name", "Last Name", "Address", "Phone", "Email", "Employee ID")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center", width=120)


    tree.bind("<Double-1>", on_tree_select)
    check_mood_status()
    load_members()
