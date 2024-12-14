import customtkinter as ctk
import sqlite3
from tkinter import ttk
from PIL import Image

def create_author_window(root, menu_frame, empid):
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
                            font=("Arial", 14))  
            style.map("Treeview", background=[("selected", "#4CAF50")])
            style.configure("Treeview.Heading", 
                            background="#212121", 
                            foreground="white", 
                            font=("Arial", 16))   
            style.map("Treeview.Heading", background=[("active", "#212121")])
            title.configure(text_color="white")

        else:

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview", 
                            background="#FFFFFF",  # Light background
                            foreground="#000000",  # Dark text color
                            rowheight=25, 
                            fieldbackground="#FFFFFF",  # Light background for fields
                            font=("Arial", 14))  
            style.map("Treeview", background=[("selected", "#4CAF50")])  # Keep the selected color as it is

            style.configure("Treeview.Heading", 
                            background="#F1F1F1",  # Lighter background for the header
                            foreground="#000000",  # Dark text color for the header
                            font=("Arial", 16))   
            style.map("Treeview.Heading", background=[("active", "#F1F1F1")])  # Keep header active state as light
            title.configure(text_color="black")

    
    def initialize_database():
        con = sqlite3.connect('library.db')
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Author (
                Author_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Author_Name TEXT NOT NULL,
                Nationality TEXT
            )
        """)
        con.commit()
        con.close()

    initialize_database()

   

    def clear_fields():
        name_entry.delete(0, "end")
        nationality_entry.delete(0, "end")
        update_status("Fields cleared")

    def load_authors(filter_name=""):
        for child in tree.get_children():
            tree.delete(child)

        con = sqlite3.connect('library.db')
        cur = con.cursor()
        
        if filter_name.strip():
            cur.execute("SELECT * FROM Author WHERE Author_Name LIKE ? ORDER BY Author_Name", (f"%{filter_name}%",))
        else:
            cur.execute("SELECT * FROM Author ORDER BY Author_Name")
        
        rows = cur.fetchall()
        con.close()

        for row in rows:
            tree.insert("", "end", values=row)

        if filter_name.strip():
            update_status(f"Search completed. Found {len(rows)} results.")
        
    def add_author():
        author_name = name_entry.get()
        nationality = nationality_entry.get()

        if not author_name.strip():
            update_status("Error: Author name is required!", error=True)
            return

        con = sqlite3.connect('library.db')
        cur = con.cursor()
        cur.execute("INSERT INTO Author (Author_Name, Nationality, Employee_ID) VALUES (?, ?, ?)", (author_name, nationality, empid))
        con.commit()
        con.close()

        clear_fields()
        load_authors()
        update_status("Author added successfully.")

    def update_author():
        selected = tree.focus()
        if not selected:
            update_status("Error: Please select an author to update.", error=True)
            return

        author_id = tree.item(selected)["values"][0]
        author_name = name_entry.get()
        nationality = nationality_entry.get()

        if not author_name.strip():
            update_status("Error: Author name is required!", error=True)
            return

        con = sqlite3.connect('library.db')
        cur = con.cursor()
        cur.execute("""
            UPDATE Author SET Author_Name = ?, Nationality = ? WHERE Author_ID = ?
        """, (author_name, nationality, author_id))
        con.commit()
        con.close()

        clear_fields()
        load_authors()
        update_status("Author updated successfully.")

    def delete_author():
        selected = tree.focus()
        if not selected:
            update_status("Error: Please select an author to delete.", error=True)
            return

        author_id = tree.item(selected)["values"][0]

        con = sqlite3.connect('library.db')
        cur = con.cursor()
        cur.execute("DELETE FROM Author WHERE Author_ID = ?", (author_id,))
        con.commit()
        con.close()

        clear_fields()
        load_authors()
        update_status("Author deleted successfully.")

    def search_authors():
        filter_name = search_entry.get()
        load_authors(filter_name)

    def clear_search():
        search_entry.delete(0, "end")
        load_authors()
        update_status("Search cleared. All authors loaded.")

    def on_tree_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, "values")
            name_entry.delete(0, "end")
            name_entry.insert(0, values[1])
            nationality_entry.delete(0, "end")
            nationality_entry.insert(0, values[2])
            update_status("Selected author loaded into fields.")

    def update_status(message, error=False):
        """Update the status label with a message."""
        if error:
            status_label.configure(text=message, text_color="red")
        else:
            status_label.configure(text=message, text_color="green")
    
    def go_back():
        menu_frame.destroy()    
        create_menu_window(root, empid)
    
    menu_frame = ctk.CTkFrame(master=root) 
    menu_frame.place(relwidth=1, relheight=1)
        
    exit_icon = Image.open("images/back.png") 

    exit_photo = ctk.CTkImage(light_image=exit_icon, dark_image=exit_icon, size=(30, 30))
    exit_button = ctk.CTkButton(
        master=menu_frame,
        text="",
        width=25,
        height=30,
        font=("Arial", 16),
        image=exit_photo,
        command=go_back
    )
    exit_button.place(relx=0.03, rely=0.03, anchor="nw")
    
    title = ctk.CTkLabel(menu_frame, text="Author Management",  font=("Arial", 24, "bold"))
    title.pack(pady=10)

    form_frame = ctk.CTkFrame(menu_frame)
    form_frame.pack(pady=30, fill="x", padx=30)


    name_label = ctk.CTkLabel(form_frame, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    name_entry = ctk.CTkEntry(form_frame, width=200)
    name_entry.grid(row=0, column=1, padx=10, pady=10)


    nationality_label = ctk.CTkLabel(form_frame, text="Nationality:")
    nationality_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    nationality_entry = ctk.CTkEntry(form_frame, width=200)
    nationality_entry.grid(row=1, column=1, padx=10, pady=10)


    status_label = ctk.CTkLabel(menu_frame, text="", font=("Arial", 12))
    status_label.pack(pady=5)


    button_frame = ctk.CTkFrame(menu_frame)
    button_frame.pack(pady=10, fill="x", padx=30)

    add_button = ctk.CTkButton(button_frame, text="Add", command=add_author)
    add_button.grid(row=0, column=0, padx=10)

    update_button = ctk.CTkButton(button_frame, text="Update", command=update_author)
    update_button.grid(row=0, column=1, padx=10)

    delete_button = ctk.CTkButton(button_frame, text="Delete", command=delete_author)
    delete_button.grid(row=0, column=2, padx=10)


    search_frame = ctk.CTkFrame(menu_frame)
    search_frame.pack(pady=10, fill="x", padx=30)

    search_label = ctk.CTkLabel(search_frame, text="Search by Name:")
    search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    search_entry = ctk.CTkEntry(search_frame, width=200)
    search_entry.grid(row=0, column=1, padx=10, pady=10)

    search_button = ctk.CTkButton(search_frame, text="Search", command=search_authors)
    search_button.grid(row=0, column=2, padx=10)

    clear_search_button = ctk.CTkButton(search_frame, text="Clear Search", command=clear_search)
    clear_search_button.grid(row=0, column=3, padx=10)


    table_frame = ctk.CTkFrame(menu_frame)
    table_frame.pack(pady=30, fill="both", expand=True, padx=20)


    columns = ("Author_ID", "Author_Name", "Nationality","Employee ID")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)
    
    tree.bind("<Double-1>", on_tree_select)
    check_mood_status()
    load_authors()

