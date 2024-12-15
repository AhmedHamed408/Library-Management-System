import customtkinter as ctk
from tkinter import ttk, messagebox
from login import create_login_window
from PIL import Image 
import sqlite3


def create_book_window(root , menu_frame,employee_id_value):
    from menu import create_menu_window 
    ###############################

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


    # =========================Frames=========================
    main_frame = ctk.CTkFrame(root)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    fr1 = ctk.CTkFrame(main_frame)
    fr1.place(relx=0, rely=0, relwidth=1, relheight=0.4)

    fr2 = ctk.CTkFrame(main_frame)
    fr2.place(relx=0, rely=0.4, relwidth=1, relheight=0.6)

    # ===============================fuction=====================
    def reset():
        entry_auther.delete(0, 'end')
        entry_title.delete(0, 'end')
        entry_pub_year.delete(0, 'end')
        entry_isbn.delete(0, 'end')
        combo_category.set("novels")
        entry_searsh_title.delete(0, 'end')
    def go_back():
        
        main_frame.destroy()
        create_menu_window(root , employee_id_value)
 
    back_icon = Image.open("images/back.png")  # Ensure the path is correct


   
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

    

    entry_auther = ctk.CTkEntry(fr1, placeholder_text="Author ID")
    entry_auther.place(relx=0.25, rely=0.20, relwidth=0.2)

    entry_pub_year = ctk.CTkEntry(fr1, placeholder_text="Publication Year (int)")
    entry_pub_year.place(relx=0.25, rely=0.35, relwidth=0.2)

    entry_title = ctk.CTkEntry(fr1, placeholder_text="Book Title")
    entry_title.place(relx=0.25, rely=0.50, relwidth=0.2)


    entry_isbn = ctk.CTkEntry(fr1, placeholder_text="ISBN (int)")
    entry_isbn.place(relx=0.8, rely=0.35, relwidth=0.2)

    
  

    entry_searsh_title = ctk.CTkEntry(fr1, placeholder_text="title")
    entry_searsh_title.place(relx=0.85, rely=0.8, relwidth=0.15)
    op=["novels","scientific books","fiction books","Religious-books","childerns-books"]


    combo_category = ctk.CTkOptionMenu(fr1, values=op)
    combo_category.place(relx=0.8, rely=0.20, relwidth=0.2)
    combo_category.set("novels")



    # ==========================Labels==========================
    label= ctk.CTkLabel(fr1, text="book" , font=("Arial", 24,"bold"))
    label.place(relx=0.5, rely=0.05)

    label_auther = ctk.CTkLabel(fr1, text="Author ID:" , font=("", 12))
    label_auther.place(relx=0.1, rely=0.20)

    label_pup_year = ctk.CTkLabel(fr1, text="Publishe _Year:", text_color='#0c9f15', font=("", 12))
    label_pup_year.place(relx=0.1, rely=0.35)

    label_title = ctk.CTkLabel(fr1, text="Title:", font=("", 12))
    label_title.place(relx=0.1, rely=0.50)

    label_category= ctk.CTkLabel(fr1, text="category" , font=("", 12))
    label_category.place(relx=0.65, rely=0.20)


    label_isbn = ctk.CTkLabel(fr1, text="ISBN :" , font=("", 12))
    label_isbn.place(relx=0.65, rely=0.35)

    label_masege=ctk.CTkLabel (fr1, text=" ", font=("", 12))
    label_masege.place(relx=0.8, rely=0.50)   
  
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

            entry_auther.delete(0, 'end')
            entry_auther.insert(0, values[3])

            entry_pub_year.delete(0, 'end')
            entry_pub_year.insert(0, values[4])


            entry_searsh_title.delete(0, 'end')
            entry_searsh_title.insert(0, values[1])
    def masge(x,y):
            label_masege.configure(text=x,text_color=y)
     
    def addtree():
#################################
        conn=sqlite3.connect("library.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Book_Details ")
        rows=cursor.fetchall()
        for row in rows:
            tree.insert("","end",values=row)
        conn.commit()
        conn.close()
  ################

    def searsh():
        for item in tree.get_children():
            tree.delete(item)
        found=False
        name = entry_searsh_title.get().strip().lower()
        conn=sqlite3.connect("library.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Book_Details WHERE Title  =? or ISBN =? ",(name,name,))
        rows=cursor.fetchall()
        if rows:
            found =True
            for row in rows:
                tree.insert("","end",values=row)
        if not found:
            masge("the book not found",'red')
            return            
        conn.commit()
        conn.close()


    def add():
        author = entry_auther.get().strip()
        title = entry_title.get().strip()
        pub_year = entry_pub_year.get()
        category = combo_category.get()
        isbn=entry_isbn.get().strip()
        
        for item in tree.get_children():
            tree.delete(item)

        if  not isbn or not pub_year or not pub_year or not author or not title:
            masge("must be enter all values","red")
            addtree()
            return
        try:
            author= int(author)
            pub_year= int(pub_year)
    
        except ValueError:
           masge(" Author_ID copies and pup_year must be integer" ,'red')
           addtree()
           return

        conn=sqlite3.connect("library.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Book_Details WHERE ISBN =? OR Title=?",(isbn,title,))
        rows=cursor.fetchall()
        if rows:
            masge("a book that alreedy exists",'red')
            addtree()
            return
        cursor.execute("SELECT * FROM Book_Details WHERE Author_ID =? ",(int(author),))
        rows=cursor.fetchall()
        if rows:
            masge("the Author_ID is exists",'red')
            addtree()
            return
        cursor.execute('''INSERT INTO Book_Details  (ISBN,Title,Category,Author_ID, Publish_year, Copies_available ,Copies_Borrowed,Employee_ID)  VALUES (?, ?,?,?,?, ?, ?,?)''', (isbn, title,category,author,pub_year,"0","0",employee_id_value))
        conn.commit()
        conn.close()
        masge(f"the {title} is added","green")  
        addtree()
        reset()


    def delete():

        name = entry_searsh_title.get().strip().lower()
        if not name:
            masge("please enter the ISBN or title",'red')
            return
        conn=sqlite3.connect("library.db")
        cursor=conn.cursor()
        
        cursor.execute("DELETE FROM Book_Details WHERE Title =? OR ISBN =?",(name,name,))
        conn.commit()
        conn.close()
        entry_searsh_title.delete(0, 'end')
        masge("the book is deleted ","green")
        for item in tree.get_children():
           tree.delete(item)
        addtree()
        reset()
    def updete():
        try:
           auther = int(entry_auther.get())
           title = entry_title.get()
           pub_year = entry_pub_year.get()
           category = combo_category.get()
           isbn=entry_isbn.get().strip()
           conn=sqlite3.connect("library.db")
           cursor=conn.cursor()
           cursor.execute(  """UPDATE Book_Details
                    SET Title=?, Author_ID=? , Publish_year=?,  Category=?
                    WHERE ISBN=?
                 """, (title, auther,pub_year,category,isbn))
           conn.commit()
           conn.commit()

           for item in tree.get_children():
              tree.delete(item)  
           addtree()
           reset()
           masge("the book is aupdet","green")
        except ValueError:
           masge("the book is not updet","red")

    # ===========================Treeview==========================
    columns=("Isbn", "title","category", "auther","pub_year","Copies_available","borrowed_copies","Employes_id")
    tree = ttk.Treeview(fr2, columns=columns ,show="headings",height=10)

    tree.heading("Isbn", text="ISBN")
    tree.heading("title", text="Title")
    tree.heading("category", text="category")
    tree.heading("auther", text="Author_ID")
    tree.heading("pub_year", text="Publisher_Year")
    tree.heading("Copies_available", text="Copies_available")
    tree.heading("borrowed_copies", text="Borrowed Copies")
    tree.heading("Employes_id", text="Employes_id")
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    for col in columns:
        tree.heading(col, text=col)
        if col == "title":
            tree.column(col, width=300)
        elif col == "pub_year":
            tree.column(col, width=100)
        elif col == "auther":
            tree.column(col, width=80)
        elif col == "category":
            tree.column(col, width=100)
        elif col == "Employes_id":
            tree.column(col, width=80)
        else:
            tree.column(col, width=150)



    tree.pack(fill="both", expand=True)
    
    # ==================Buttons====================================
    but_addbook = ctk.CTkButton(fr1, text="Add Book", command=add)
    but_addbook.place(relx=0.65, rely=0.8, relwidth=0.15)

    but_update = ctk.CTkButton(fr1, text="Update",command=updete)
    but_update.place(relx=0.45, rely=0.8, relwidth=0.15)

    but_delete = ctk.CTkButton(fr1, text="Delete",command=delete)
    but_delete.place(relx=0.25, rely=0.8, relwidth=0.15)

    but_search = ctk.CTkButton(fr1, text="Search",command=searsh)
    but_search.place(relx=0.05, rely=0.8, relwidth=0.15)

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

    

