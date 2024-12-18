import customtkinter as ctk
from tkinter import ttk, messagebox
from login import create_login_window
from PIL import Image 
import sqlite3


def create_book_window(root , menu_frame,employee_id_value):
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
                            font=("Arial", 12))   
            style.map("Treeview.Heading", background=[("active", "#F1F1F1")]) 

    ###############################  
    # =========================Frames=========================
    main_frame = ctk.CTkFrame(root)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    fr1 = ctk.CTkFrame(main_frame)
    fr1.place(relx=0, rely=0, relwidth=1, relheight=0.4)

    fr2 = ctk.CTkFrame(main_frame)
    fr2.place(relx=0, rely=0.4, relwidth=1, relheight=0.6)

    # ===============================fuction=====================
    def reset():
        entry_author.delete(0, 'end')
        entry_author2.delete(0, 'end')
        entry_title.delete(0, 'end')
        entry_pub_year.delete(0, 'end')
        entry_isbn.delete(0, 'end')
        combo_category.set("novels")
        entry_search_title.delete(0, 'end')
    def go_back():
        
        main_frame.destroy()
        create_menu_window(root , employee_id_value)
 
    back_icon = Image.open("images/back.png")  


   
    back_photo = ctk.CTkImage(light_image=back_icon, dark_image=back_icon, size=(30, 30))
    back_button = ctk.CTkButton(
        master=fr1,
        text="",
        width=25,
        height=30,
        font=("Arial", 16),
        image=back_photo,
        command=go_back
    )
    back_button.place(relx=0.03, rely=0.03, anchor="nw")  


    

    entry_author = ctk.CTkEntry(fr1, placeholder_text="Author ID")
    entry_author.place(relx=0.25, rely=0.20, relwidth=0.2)
    
    entry_author2 = ctk.CTkEntry(fr1, placeholder_text="Another Author ID")
    entry_author2.place(relx=0.25, rely=0.35, relwidth=0.2)

    entry_pub_year = ctk.CTkEntry(fr1, placeholder_text="Publication Year (int)")
    entry_pub_year.place(relx=0.25, rely=0.50, relwidth=0.2)

    entry_title = ctk.CTkEntry(fr1, placeholder_text="Book Title")
    entry_title.place(relx=0.8, rely=0.35, relwidth=0.2)


    entry_isbn = ctk.CTkEntry(fr1, placeholder_text="ISBN (int)")
    entry_isbn.place(relx=0.8, rely=0.5, relwidth=0.2)

    
  

    entry_search_title = ctk.CTkEntry(fr1, placeholder_text="title")
    entry_search_title.place(relx=0.85, rely=0.8, relwidth=0.15)
    op=["novels","scientific books","fiction books","Religious-books","childerns-books"]


    combo_category = ctk.CTkOptionMenu(fr1, values=op)
    combo_category.place(relx=0.8, rely=0.20, relwidth=0.2)
    combo_category.set("novels")



    # ==========================Labels==========================
    label= ctk.CTkLabel(fr1, text="Book Details" , font=("Arial", 24,"bold"))
    label.place(relx=0.5, rely=0.05)

    label_author = ctk.CTkLabel(fr1, text="Author ID:" )
    label_author.place(relx=0.1, rely=0.20)

    label_pup_year = ctk.CTkLabel(fr1, text="Publishe Year:")
    label_pup_year.place(relx=0.1, rely=0.50)

    label_title = ctk.CTkLabel(fr1, text="Title:")
    label_title.place(relx=0.65, rely=0.35)

    label_category= ctk.CTkLabel(fr1, text="Category" )
    label_category.place(relx=0.65, rely=0.20)


    label_isbn = ctk.CTkLabel(fr1, text="ISBN :" )
    label_isbn.place(relx=0.65, rely=0.50)

    label_masege=ctk.CTkLabel (fr1, text=" ")
    label_masege.place(relx=0.3, rely=0.65)   
  
    # ===========================Functions=======================   
    def on_tree_select(event):
        selected_item = tree.focus()
        if not selected_item:
            return

        values = tree.item(selected_item, "values")  
        if values:

            entry_isbn.delete(0, 'end')
            entry_isbn.insert(0, values[0])

            entry_title.delete(0, 'end')
            entry_title.insert(0, values[1])

            
            combo_category.set(values[2])

            entry_author.delete(0, 'end')
            entry_author.insert(0, values[7])

            entry_author2.delete(0, 'end')
            entry_author2.insert(0,values[8])


            entry_pub_year.delete(0, 'end')
            entry_pub_year.insert(0, values[3])


            entry_search_title.delete(0, 'end')
            entry_search_title.insert(0, values[1])
    def masge(x,y):
            label_masege.configure(text=x,text_color=y)
     
    def addtree():
    #################################
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
    
    
        cursor.execute("""
        SELECT 
            bd.ISBN, 
            bd.Title, 
            bd.Category,
            bd.Publish_year, 
            bd.Copies_available, 
            bd.Copies_Borrowed, 
            bd.Employee_ID,
            GROUP_CONCAT(ba.Author_ID) AS Authors
        FROM 
            Book_Details AS bd
        LEFT JOIN 
            Book_Authors AS ba
        ON 
            bd.ISBN = ba.ISBN
        GROUP BY 
            bd.ISBN
    """)
    
        rows = cursor.fetchall()
    
        for item in tree.get_children():
           tree.delete(item)
    
        for row in rows:
        
           authors = row[-1].split(",") if row[-1] else []
           author_id1 = authors[0] if len(authors) > 0 else None
           author_id2 = authors[1] if len(authors) > 1 else None
        
        
           tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], author_id1, author_id2))
    
        conn.commit()
        conn.close()
 

    def search():
        for item in tree.get_children():
            tree.delete(item)
        found=False
        name = entry_search_title.get().strip().lower()
        conn=sqlite3.connect("library.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Book_Details WHERE Title LIKE ? OR ISBN LIKE ?", (f'%{name}%', f'%{name}%'))
        rows=cursor.fetchall()
        if rows:
            found =True
            for row in rows:
                tree.insert("","end",values=row)
            masge("the book is found",'green')
        if not found:
            masge("the book not found",'red')
            addtree()
            return            
        conn.commit()
        conn.close()


    def add():
        author = entry_author.get().strip()
        author2 = entry_author2.get().strip() 
        title = entry_title.get().strip()
        pub_year = entry_pub_year.get()
        category = combo_category.get()
        isbn = entry_isbn.get().strip()

        for item in tree.get_children():
            tree.delete(item)

        if not isbn or not pub_year or not author or not title:
            masge("Must enter all required values", "red")
            addtree()
            return

        try:
            author = int(author)
            pub_year = int(pub_year)
        except ValueError:
            masge("Author ID and Publish Year must be integers", 'red')
            addtree()
            return
        if not author_exists(author):
            masge("Author ID didn't exist", 'red')   
            addtree()
            return
        if author2:
            if not author_exists(author2):
                masge("Another Author ID didn't exist", 'red') 
                addtree()      
                return
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Book_Details WHERE ISBN =? OR Title=?", (isbn, title))
            if cursor.fetchall():
                masge("A book with this ISBN or Title already exists", 'red')
                addtree()
                return

            cursor.execute('''INSERT INTO Book_Details 
                            (ISBN, Title, Category, Publish_year, Copies_available, Copies_Borrowed, Employee_ID) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (isbn, title, category, pub_year, 0, 0, employee_id_value))

            cursor.execute("INSERT INTO Book_Authors (ISBN, Author_ID) VALUES (?, ?)", (isbn, author))

            if author2:
                try:
                    author2 = int(author2)
                    cursor.execute("INSERT INTO Book_Authors (ISBN, Author_ID) VALUES (?, ?)", (isbn, author2))
                except ValueError:
                    masge("Optional Author ID must be an integer", "red")
                    addtree()
                    return

            conn.commit()
            masge(f"The book '{title}' has been added successfully!", "green")
            reset()
        except sqlite3.Error as e:
            masge(f"Database Error: {e}", "red")
        finally:
            conn.close()
            addtree()
    def author_exists(author_id):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Author WHERE Author_ID LIKE  ?", (author_id,))
        exists = cursor.fetchone() is not None
        conn.commit()
        conn.close()
        return exists
    
    def delete():
        name = entry_search_title.get().strip().upper()
        if not name:
            masge("please enter the ISBN or title", 'red')
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        try:
           
            cursor.execute("DELETE FROM Book_Details WHERE Title LIKE ? OR ISBN LIKE ?", (f'%{name}%', f'%{name}%'))
            conn.commit()
           
            masge("the book is deleted", "green")
            entry_search_title.delete(0, 'end')
            for item in tree.get_children():
                tree.delete(item)
            addtree()
            reset()

        except sqlite3.IntegrityError as e:
            
            masge(f"Error: {e}", "red")

        finally:
            conn.close()
    def update():
        try:
            isbn = entry_isbn.get().strip()
            title = entry_title.get().strip()
            pub_year = entry_pub_year.get().strip()
            category = combo_category.get()
            author_id = entry_author.get().strip()  
            author_id2 = entry_author2.get().strip()  
            item = tree.get_children()[0]
            if item !=isbn:
                masge("isbn cannot update",'red')
                return
            if not isbn or not title or not pub_year or not author_id:
                masge("ISBN, Title, Publication Year, and Author ID are required", "red")
                return

            pub_year = int(pub_year)
            author_id = int(author_id)
            author_id2 = int(author_id2) if author_id2 else None
            if author_id2:
                if not author_exists(author_id2):
                    masge("Author ID didn't exist", 'red')   
                    addtree()
                    return
            if not author_exists(author_id):
                masge("Another Author ID didn't exist", 'red') 
                addtree()   
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
         
            cursor.execute("""
                UPDATE Book_Details
                SET Title = ?, Publish_year = ?, Category = ?
                WHERE ISBN = ?
            """, (title, pub_year, category, isbn))

            cursor.execute("DELETE FROM Book_Authors WHERE ISBN = ?", (isbn,))  

            cursor.execute("""
                INSERT INTO Book_Authors (ISBN, Author_ID)
                VALUES (?, ?)
            """, (isbn, author_id))

            if author_id2 and author_id2 != author_id:
                cursor.execute("""
                    INSERT INTO Book_Authors (ISBN, Author_ID)
                    VALUES (?, ?)
                """, (isbn, author_id2))

            conn.commit()
            conn.close()

            for item in tree.get_children():
                tree.delete(item)
            addtree()
            reset()
            masge("The book and authors were updated successfully", "green")

        except ValueError:
            masge("Publication Year and Author IDs must be integers", "red")
        except sqlite3.Error as e:
            masge(f"Database error: {e}", "red")

    # ===========================Treeview==========================
    columns = ("ISBN", "Title", "Category", "Publish Year", "Copies Available", "Borrowed Copies", "Employee ID", "Author ID1", "Author ID2")
    tree = ttk.Treeview(fr2, columns=columns, show="headings", height=10)

    tree.heading("ISBN", text="Isbn")
    tree.heading("Title", text="Title")
    tree.heading("Category", text="category")
    tree.heading("Publish Year", text="Publisher_year")
    tree.heading("Copies Available", text="Copies_available")
    tree.heading("Borrowed Copies", text="Borrowed_copies")
    tree.heading("Employee ID", text="Employes_id")
    tree.heading("Author ID1", text="author_id1")
    tree.heading("Author ID2", text="author_id2")


    tree.bind("<<TreeviewSelect>>", on_tree_select)

    for col in columns:
        tree.heading(col, text=col)
        if col == "Title":
            tree.column(col, width=170)
        elif col == "Publish Year":
            tree.column(col, width=100)
        elif col == "Copies Available":
            tree.column(col, width=130)
        elif col == "Author ID1":
            tree.column(col, width=82)
        elif col == "Author ID2":
            tree.column(col, width=85)
        elif col == "Category":
            tree.column(col, width=100)
        elif col == "Employee ID":
            tree.column(col, width=80)
        else:
            tree.column(col, width=150)



    tree.pack(fill="both", expand=True)


    # ==================Buttons====================================
    but_addbook = ctk.CTkButton(fr1, text="Add Book", command=add)
    but_addbook.place(relx=0.05, rely=0.8, relwidth=0.15)

    but_update = ctk.CTkButton(fr1, text="Update",command=update)
    but_update.place(relx=0.45, rely=0.8, relwidth=0.15)

    but_delete = ctk.CTkButton(fr1, text="Delete",command=delete)
    but_delete.place(relx=0.25, rely=0.8, relwidth=0.15)

    but_search = ctk.CTkButton(fr1, text="Search",command=search)
    but_search.place(relx=0.65, rely=0.8, relwidth=0.15)

    conn=sqlite3.connect("library.db")
    cursor=conn.cursor()
    cursor.execute("SELECT ISBN FROM Book_Details")
    isbns = cursor.fetchall()

    for isbn_t in isbns:
        isbn = isbn_t[0]  
        cursor.execute("""
           SELECT COUNT(Book_ID) 
           FROM Book_Copy 
            WHERE ISBN = ? AND Status = ?
             """, (isbn, 'Available'))
        count = cursor.fetchone()[0] 

        cursor.execute("""
        UPDATE Book_Details 
        SET Copies_Available = ? 
        WHERE ISBN = ?
         """, (count, isbn))
        cursor.execute("""
           SELECT COUNT(Book_ID) 
           FROM Book_Copy 
            WHERE ISBN = ? AND Status = ?
             """, (isbn, 'Borrowed'))
        count = cursor.fetchone()[0] 

        cursor.execute("""
        UPDATE Book_Details 
        SET Copies_Borrowed = ? 
        WHERE ISBN = ?
         """, (count, isbn))

    conn.commit()
    conn.close()
    check_mood_status()
    addtree()

    

