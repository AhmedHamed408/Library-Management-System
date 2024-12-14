import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime, timedelta
from PIL import Image 
import sqlite3


def create_transaction_window(window, menu_frame, employee_ID):
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
                            font=("Arial", 12))   
            style.map("Treeview.Heading", background=[("active", "#212121")])
            borrow_label.configure(text_color="white")

        else:

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview", 
                            background="#FFFFFF",  # Light background
                            foreground="#000000",  # Dark text color
                            rowheight=25, 
                            fieldbackground="#FFFFFF",  # Light background for fields
                            font=("Arial", 12))  
            style.map("Treeview", background=[("selected", "#4CAF50")])  # Keep the selected color as it is

            style.configure("Treeview.Heading", 
                            background="#F1F1F1",  # Lighter background for the header
                            foreground="#000000",  # Dark text color for the header
                            font=("Arial", 14))   
            style.map("Treeview.Heading", background=[("active", "#F1F1F1")])  # Keep header active state as light
            borrow_label.configure(text_color="black")


    
    def member_exists(member_id):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Member WHERE Member_ID = ?", (member_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    def book_id_exists(book_id):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Book_Copy WHERE Book_ID = ?", (book_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    def Is_book_Available(book_id):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        # Fetch the Status column for the given Book_ID
        cursor.execute("SELECT Status FROM Book_Copy WHERE Book_ID = ?", (book_id,))
        result = cursor.fetchone() 
        conn.close()
        # If a record is found, return the Status; otherwise, return None
        return result[0]== "Available"
    
    def save_to_database(member_id, book_id, days_of_borrowing, employee_ID):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        borrow_date = datetime.today()
        due_date =(borrow_date + timedelta(days=days_of_borrowing))
        borrow_date = borrow_date.strftime('%Y-%m-%d')
        Due_date = due_date.strftime('%Y-%m-%d')
        # Insert into Borrow table
        cursor.execute('''INSERT INTO Borrow (Borrow_date,Due_date, Return_date, Borrow_Duration, Book_ID, Employee_ID, Member_ID,Returned) 
                        VALUES (?, ?, ?, ?, ?, ?,?,?)''',
                       (borrow_date,Due_date, None, days_of_borrowing, book_id, employee_ID, member_id,'No'))
        # Update Returned status in Book_Copy
        cursor.execute("UPDATE Book_Copy SET Status = ? WHERE Book_ID = ?", ('Borrowed', book_id))
        conn.commit()
        conn.close()

    def load_data_into_table():
        # فتح الاتصال بقاعدة البيانات
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # استعلام لتحميل البيانات من جداول Borrow و Book_Copy
        cursor.execute('''
            SELECT b.Borrow_ID,  b.Borrow_date,b.Due_date , b.Return_date, b.Borrow_Duration, b.Member_ID, b.Employee_ID, b.Book_ID, b.Returned
            FROM Borrow b
        ''')
        
        # استرجاع جميع الصفوف
        rows = cursor.fetchall()
        conn.close()

        # مسح البيانات القديمة من الجدول
        for item in table.get_children():
            table.delete(item)

        # إضافة البيانات الجديدة إلى الجدول
        for row in rows:
            table.insert("", "end", values=row)

# تأكد من أن هذه الدالة يتم استدعاؤها بعد عملية الحفظ أو تحديث حالة الكتاب
    def go_back():
        menu_frame.destroy()
        create_menu_window(window , employee_ID)
        frame_inside_borrow.destroy()
        table_frame.destroy()
        

    def save_data():
        member_id = member_id_entry.get().strip()
        book_id = book_id_entry.get().strip()
        days_of_borrowing = days_of_borrowing_entry.get().strip()

        if not member_id or not book_id or not days_of_borrowing:
            status_label.configure(text="Please fill all fields!", text_color="red")
            return

        try:
            member_id = int(member_id)
            book_id = int(book_id)
            days_of_borrowing = int(days_of_borrowing)
        except ValueError:
            status_label.configure(text="Please enter valid numbers!", text_color="red")
            return

        if not member_exists(member_id):
            status_label.configure(text="Member ID not found!", text_color="red")
            return
        if not book_id_exists(book_id):
            status_label.configure(text="Book not found!", text_color="red")
            return
        if not Is_book_Available(book_id) :
            status_label.configure(text="This Book is Borrowed.", text_color="red")
            return
        

        save_to_database(member_id, book_id, days_of_borrowing, employee_ID)
        
        # تحميل البيانات بعد عملية الحفظ
        load_data_into_table()

        member_id_entry.delete(0, 'end')
        book_id_entry.delete(0, 'end')
        days_of_borrowing_entry.delete(0, 'end')
        status_label.configure(text="Saved successfully!", text_color="green")


    def update_returned_status():
        borrowing_id = search_entry.get().strip()
        if not borrowing_id.isdigit():
            search_status_label.configure(text="Borrowing ID not valid!", text_color="red")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Book_ID , Returned FROM Borrow WHERE Borrow_ID = ?", (borrowing_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            search_status_label.configure(text="No borrowing record found!", text_color="red")
            return

        Book_ID = row[0]
        Returned = row[1]
        if Returned == 'Yes':
            search_status_label.configure(text="Book already returned!", text_color="red")
            return

        today_date = datetime.today().strftime('%Y-%m-%d')
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE Borrow SET Return_date = ?,Returned = ? WHERE Borrow_ID = ?", (today_date,'Yes', borrowing_id))
        cursor.execute("UPDATE Book_Copy SET Status = ? WHERE Book_ID = ?", ('Available', Book_ID))
        conn.commit()
        conn.close()

        search_status_label.configure(text="Returned successfully!", text_color="green")
        load_data_into_table()
        return_button.configure(state="disabled")
    
    def search_borrowing():
        borrowing_id = search_entry.get().strip()
        if not borrowing_id.isdigit():
            search_status_label.configure(text="Enter Borrowing ID!", text_color="red")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT b.Borrow_ID,b.Borrow_date, b.Due_date, b.Return_date, b.Borrow_Duration, b.Member_ID, b.Employee_ID, b.Book_ID, b.Returned 
                        FROM Borrow b
                        WHERE Borrow_ID = ?''', (borrowing_id,))
        row = cursor.fetchone()
        conn.close()

        for item in table.get_children():
            table.delete(item)

        if row:
            table.insert("", "end", values=row)
            search_status_label.configure(text="Search completed!", text_color="green")
            return_button.configure(state="normal")
        else:
            search_status_label.configure(text="No data found!", text_color="red")
            return_button.configure(state="disabled")

    def handle_row_select(event):
        selected_item = table.selection()
        if selected_item:
            item_data = table.item(selected_item, "values")
            search_entry.delete(0, 'end')
            search_entry.insert(0, item_data[0])
            search_status_label.configure(text=f"Selected Borrowing ID: {item_data[0]}", text_color="blue")
            return_button.configure(state="normal")

    def return_selected_book():
        borrowing_id = search_entry.get().strip()
        if not borrowing_id:
            search_status_label.configure(text="Enter a Borrowing ID!", text_color="red")
            return
        update_returned_status()

    def clear_search():
        search_entry.delete(0, 'end')
        search_status_label.configure(text="")
        load_data_into_table()

    

    frame_inside_borrow = ctk.CTkFrame(window)
    frame_inside_borrow.place(relwidth=1, relheight=1)

    
        
    back_image = Image.open("images/back.png")
    back_photo = ctk.CTkImage(light_image=back_image, dark_image=back_image, size=(25, 25))
    back_button = ctk.CTkButton(
        master=frame_inside_borrow,
        text="",
        width=25,
        height=30,
        font=("Arial", 16),
        image=back_photo,
        command=go_back
    )
    back_button.place(x=20, y=20)


    borrow_label = ctk.CTkLabel(frame_inside_borrow, text="Borrow", font=("Arial", 30))
    borrow_label.grid(row=0, column=1, pady=2)

    member_id_label = ctk.CTkLabel(frame_inside_borrow, text="Member ID:")
    member_id_label.grid(row=2, column=0, pady=2)
    member_id_entry = ctk.CTkEntry(frame_inside_borrow)
    member_id_entry.grid(row=2, column=1, pady=2)

    book_id_label = ctk.CTkLabel(frame_inside_borrow, text="Book ID:")
    book_id_label.grid(row=3, column=0, pady=2)
    book_id_entry = ctk.CTkEntry(frame_inside_borrow)
    book_id_entry.grid(row=3, column=1, pady=2)

    days_of_borrowing_label = ctk.CTkLabel(frame_inside_borrow, text="Days of borrowing:")
    days_of_borrowing_label.grid(row=4, column=0, pady=2)
    days_of_borrowing_entry = ctk.CTkEntry(frame_inside_borrow)
    days_of_borrowing_entry.grid(row=4, column=1, pady=2)

    save_button = ctk.CTkButton(frame_inside_borrow, text="Save", command=save_data)
    save_button.grid(row=6, column=1, pady=2)

    status_label = ctk.CTkLabel(frame_inside_borrow, text="")
    status_label.grid(row=5, column=1)

    search_label = ctk.CTkLabel(frame_inside_borrow, text="Search by ID:")
    search_label.grid(row=2, column=2, pady=2)
    search_entry = ctk.CTkEntry(frame_inside_borrow, placeholder_text="Borrowing ID")
    search_entry.grid(row=2, column=3, pady=2)

    search_button = ctk.CTkButton(frame_inside_borrow, text="Search", command=search_borrowing)
    search_button.grid(row=4, column=3, pady=2)

    clear_search_button = ctk.CTkButton(frame_inside_borrow, text="Clear Search", command=clear_search)
    clear_search_button.grid(row=5, column=3, pady=2)

    search_status_label = ctk.CTkLabel(frame_inside_borrow, text="")
    search_status_label.grid(row=3, column=3)

    return_button = ctk.CTkButton(frame_inside_borrow, text="Return Book", command=return_selected_book, state="disabled")
    return_button.grid(row=4, column=2, pady=2)

    table_frame = ctk.CTkFrame(frame_inside_borrow)
    table_frame.grid(row=8, column=0, columnspan=4, padx=2, pady=2, sticky="nsew")
    
    frame_inside_borrow.grid_rowconfigure(8, weight=1)
    frame_inside_borrow.grid_columnconfigure(0, weight=1)
    frame_inside_borrow.grid_columnconfigure(1, weight=1)
    frame_inside_borrow.grid_columnconfigure(2, weight=1)

    table = ttk.Treeview(table_frame, columns=("Borrowing ID", "Borrow Date", "Due Date", "Return Date", "Days of borrowing", "Member ID", "Employee ID", "Book ID", "Returned"),
                         show="headings")
    table.pack(fill="both", expand=True)

    table.heading("Borrowing ID", text="Borrowing ID")
    table.heading("Borrow Date", text="Borrow Date")
    table.heading("Due Date", text="Due Date")
    table.heading("Return Date", text="Return Date")
    table.heading("Days of borrowing", text="Borrowing Period")
    table.heading("Member ID", text="Member ID")
    table.heading("Employee ID", text="Employee ID")
    table.heading("Book ID", text="Book ID")
    table.heading("Returned", text="Returned")

    table.column("Borrowing ID", width=50)
    table.column("Borrow Date", width=70)
    table.column("Due Date", width=70)
    table.column("Return Date", width=70)
    table.column("Days of borrowing", width=80)
    table.column("Member ID", width=50)
    table.column("Employee ID", width=50)
    table.column("Book ID", width=30)
    table.column("Returned", width=50)

    table.bind("<<TreeviewSelect>>", handle_row_select)
    check_mood_status()
    load_data_into_table()