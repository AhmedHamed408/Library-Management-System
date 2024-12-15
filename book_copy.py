import customtkinter as ctk
from PIL import Image
import sqlite3
from tkinter import ttk  

def create_book_copy_window(root , menu_frame,emp_id):
    from menu import create_menu_window 
    from book import create_book_window
    copy_frame = ctk.CTkFrame(master=root)   
    copy_frame.place(relwidth=1, relheight=1)
    

  
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    def go_back():

        menu_frame.destroy()    
        create_menu_window(root , emp_id)

        

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
            book_copy_label.configure(text_color="white")

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
            book_copy_label.configure(text_color="black")




    def update_status(message, color="red"):
        status_label.configure(text=message, text_color=color, font=("Arial", 14))

    def add_or_update_book_copy():
        isbn = isbn_var.get()
        num_copies = num_copies_var.get()

        if not (isbn and num_copies.isdigit()):
            update_status("ISBN and Number of Copies are required.", "red")
            return

        num_copies = int(num_copies)
        if not member_exists(isbn):
            status_label.configure(text="ISBN not found! Please add exist ISBN or go to Book Details to add new ISBN.", text_color="red")
            add_book_details_button.grid(row=3, column=2, pady=2)
            return

        try:
           
            cursor.execute("SELECT MAX(Book_ID) FROM Book_Copy")
            max_book_id = cursor.fetchone()[0]

            if max_book_id :
                next_book_id = int(max_book_id) + 1
            else:
                next_book_id= 1
                
                
            for i in range(num_copies):
                book_id = next_book_id + i
                cursor.execute(
                    """
                    INSERT INTO Book_Copy (Book_ID, ISBN, Status, Employee_ID)
                    VALUES (?, ?, ?,?)
                    """,
                    (book_id, isbn, "Available",emp_id)
                )
        
            conn.commit()
           
            update_status(f"{num_copies} Book Copies added successfully!", "green")
            clear_fields()
            display_book_copies()
        
        except sqlite3.IntegrityError:
            update_status("Error: Duplicate Book ID or ISBN. Could not add copies.", "red")
        except ValueError:
            update_status("Error: Invalid input. Please check the Book ID format.", "red")
        except Exception as e:
            update_status(f"Unexpected error: {str(e)}", "red")

    def member_exists(isbn):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Book_Details WHERE ISBN = ?", (isbn,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def delete_book():
        selected_item = tree.focus()
        if not selected_item:
            update_status("Error: No Book Copy selected.", "red")
            return

        book_id = tree.item(selected_item)["values"][0]

        cursor.execute("SELECT COUNT(*) FROM Borrow WHERE Book_ID=?", (book_id,))
        borrowed_count = cursor.fetchone()[0]

        if borrowed_count > 0:
            update_status("Error: Book cannot be deleted because it is currently borrowed or borrowed befor.", "red")
            return

        cursor.execute("DELETE FROM Book_Copy WHERE Book_ID=?", (book_id,))
        conn.commit()

        update_status("Book deleted successfully!", "green")
        display_book_copies()
            
    def search_book_copy():
        search_term = search_var.get()
        if not search_term:
            update_status("Please enter a term to search.", "red")
            return

        cursor.execute(
            """
            SELECT BC.Book_ID, BD.Title, BC.ISBN, BC.Status
            FROM Book_Copy BC
            LEFT JOIN Book_Details BD ON BC.ISBN = BD.ISBN
            WHERE BC.Book_ID LIKE ? OR BD.Title LIKE ? OR BC.ISBN LIKE ? OR BC.Status LIKE ?
            """,
            (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
        )
        rows = cursor.fetchall()
        update_tree(rows)

    def display_book_copies():
        cursor.execute(
            """
            SELECT BC.Book_ID, BD.Title, BC.ISBN, BC.Status , BC.Employee_ID
            FROM Book_Copy BC
            LEFT JOIN Book_Details BD ON BC.ISBN = BD.ISBN
            """
        )
        rows = cursor.fetchall()
        update_tree(rows)


    def update_tree(rows):
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", "end", values=row)

    def clear_fields():
        """
        Clears input fields without resetting the status label.
        """
        book_id_var.set("")
        isbn_var.set("")
        num_copies_var.set("")
        search_var.set("")
        selected_book_copy_ID.set("")

    def clear_search():
        search_var.set("")
        display_book_copies()
        update_status("Search cleared.", "green")
    
    back_icon = Image.open("images/back.png")  

   
    back_photo = ctk.CTkImage(light_image=back_icon, dark_image=back_icon, size=(30, 30))
    back_button = ctk.CTkButton(
        master=copy_frame,
        text="",
        width=25,
        height=30,
        font=("Arial", 16),
        image=back_photo,
        command=go_back
    )
    back_button.place(relx=0.03, rely=0.03, anchor="nw")  

    
    book_copy_label = ctk.CTkLabel(
        master=copy_frame,
        text="Book Copy",
        font=("Arial", 24, "bold"),
        text_color="white"  
    )
    book_copy_label.place(relx=0.5, rely=0.04, anchor="n")   
     
    book_id_var = ctk.StringVar()
    isbn_var = ctk.StringVar()
    num_copies_var = ctk.StringVar()
    search_var = ctk.StringVar()
    selected_book_copy_ID = ctk.StringVar()

    
    frame = ctk.CTkFrame(copy_frame, corner_radius=10)
    frame.place(relx=0.5, rely=0.56, anchor="center")

    
    ctk.CTkLabel(frame, text="ISBN:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    ctk.CTkEntry(frame, textvariable=isbn_var, font=("Arial", 14)).grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(frame, text="Number of Copies:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    ctk.CTkEntry(frame, textvariable=num_copies_var, font=("Arial", 14)).grid(row=2, column=1, padx=10, pady=10)

     
    ctk.CTkButton(frame, text="Add", font=("Arial", 14), command=add_or_update_book_copy).grid(row=3, column=0, padx=10, pady=10)
    ctk.CTkButton(frame, text="Delete", font=("Arial", 14), command=delete_book).grid(row=3, column=1, padx=10, pady=10)

     
    status_label = ctk.CTkLabel(frame, text="", font=("Arial", 12), text_color="red")
    status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

  
    ctk.CTkEntry(frame, textvariable=search_var, placeholder_text="Search...", font=("Arial", 14)).grid(row=5, column=0, padx=10, pady=10)
    ctk.CTkButton(frame, text="Search", font=("Arial", 14), command=search_book_copy).grid(row=5, column=1, padx=10, pady=10)
    ctk.CTkButton(frame, text="Clear Search", font=("Arial", 14), command=clear_search).grid(row=5, column=2, padx=10, pady=10)
    add_book_details_button = ctk.CTkButton(frame, text="Add Book Details", command=lambda: create_book_window(root, menu_frame,emp_id))
    add_book_details_button.grid(row=6, column=0, pady=2)
    add_book_details_button.grid_forget()

    
    tree_frame = ctk.CTkFrame(frame)
    tree_frame.grid(row=6, column=0, columnspan=3, padx=25, pady=20, sticky="nsew")
    
 

    columns = ("Book ID", "Title", "ISBN", "Status","Employee ID")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=200)

    tree.pack(fill="both", expand=True)

    check_mood_status()
    display_book_copies()
