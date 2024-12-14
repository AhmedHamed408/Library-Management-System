import customtkinter as ctk
from PIL import Image
from member import create_member_window
from borrow import create_transaction_window
from book import create_book_window
from book_copy import create_book_copy_window
from author import create_author_window
import sqlite3

def create_menu_window(menu_window , employee_id ):
   
    def mood_button_clicked():
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def exit_button_clicked():
        menu_window.destroy()
        
    def button1_action():
        create_member_window(menu_window ,menu_frame , employee_id)

    def button2_action():
       create_transaction_window(menu_window ,menu_frame , employee_id)

    def button3_action():
        create_book_window(menu_window , menu_frame , employee_id)
   
    def button4_action():
       create_author_window(menu_window ,menu_frame , employee_id)

    def button5_action():
        create_book_copy_window(menu_window , menu_frame , employee_id)
        
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT First_name from Employee WHERE Employee_ID = ?", (employee_id,))
    user_nameF = cur.fetchall()
    user_name = user_nameF[0][0]
    
    
    menu_frame = ctk.CTkFrame(master=menu_window)  
    menu_frame.place(relwidth=1, relheight=1)
    mood_image = Image.open("images/brightness-and-contrast.png")
    mood_photo = ctk.CTkImage(light_image=mood_image, dark_image=mood_image, size=(25, 25))
    mood_button = ctk.CTkButton(
        master=menu_frame,
        text="",
        width=25,
        height=30,
        font=("Arial", 16),
        image=mood_photo,
        command=mood_button_clicked
    )
    mood_button.place(x=20, y=20)
    
    exit_image = Image.open("images/exit.png")
    exit_photo = ctk.CTkImage(light_image=exit_image, dark_image=exit_image, size=(25, 25))
    exit_button = ctk.CTkButton(
        master=menu_frame,
        text="",
        width=25,
        height=30,
        font=("Arial", 16),
        image=exit_photo,
        command=exit_button_clicked
    )
    exit_button.place(x=20, y=60)
    title_label = ctk.CTkLabel(master=menu_frame, text="Menu", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

  
    user_frame = ctk.CTkFrame(master=menu_frame, width=180, height=100)  
    user_frame.place(relx=1.0, x=-15, y=15, anchor="ne")

    user_image = Image.open("images/user.png")
    user_photo = ctk.CTkImage(light_image=user_image, dark_image=user_image, size=(30, 30))  
    user_icon_label = ctk.CTkLabel(master=user_frame, image=user_photo, text="")
    user_icon_label.pack(pady=5)   

    welcome_label = ctk.CTkLabel(master=user_frame, text=f"Welcome, "+user_name, font=("Arial", 12 , "bold"))  
    welcome_label.pack(pady=0, padx=5)  


    frame1 = ctk.CTkFrame(master=menu_frame, width=250, height=250, border_color="#A9A9A9", border_width=2)
    frame1.place(relx=0.2, rely=0.35, anchor="center")

    content_frame1 = ctk.CTkFrame(master=frame1)
    content_frame1.pack(pady=10, padx=10, expand=True, fill="both")

    empty_label1 = ctk.CTkLabel(master=content_frame1, text="", width=200, height=0)
    empty_label1.pack(pady=10)

    img1 = Image.open("images/button2_image.png")
    photo1 = ctk.CTkImage(light_image=img1, dark_image=img1, size=(100, 100))
    image_label1 = ctk.CTkLabel(master=content_frame1, image=photo1, text="")
    image_label1.pack(pady=10)

    button1 = ctk.CTkButton(master=content_frame1, text="Members", font=("Arial", 16), width=150, height=40, command=button1_action)
    button1.pack(pady=10)

    frame2 = ctk.CTkFrame(master=menu_frame, width=250, height=250, border_color="#A9A9A9", border_width=2)
    frame2.place(relx=0.5, rely=0.35, anchor="center")

    content_frame2 = ctk.CTkFrame(master=frame2)
    content_frame2.pack(pady=10, padx=10, expand=True, fill="both")

    empty_label2 = ctk.CTkLabel(master=content_frame2, text="", width=200, height=0)
    empty_label2.pack(pady=10)

    img2 = Image.open("images/button1_image.png")
    photo2 = ctk.CTkImage(light_image=img2, dark_image=img2, size=(100, 100))
    image_label2 = ctk.CTkLabel(master=content_frame2, image=photo2, text="")
    image_label2.pack(pady=10)

    button2 = ctk.CTkButton(master=content_frame2, text="Borrow", font=("Arial", 16), width=150, height=40, command=button2_action)
    button2.pack(pady=10)

    frame3 = ctk.CTkFrame(master=menu_frame, width=250, height=250, border_color="#A9A9A9", border_width=2)
    frame3.place(relx=0.8, rely=0.35, anchor="center")

    content_frame3 = ctk.CTkFrame(master=frame3)
    content_frame3.pack(pady=10, padx=10, expand=True, fill="both")

    empty_label3 = ctk.CTkLabel(master=content_frame3, text="", width=200, height=0)
    empty_label3.pack(pady=10)

    img3 = Image.open("images/button3_image.png")
    photo3 = ctk.CTkImage(light_image=img3, dark_image=img3, size=(100, 100))
    image_label3 = ctk.CTkLabel(master=content_frame3, image=photo3, text="")
    image_label3.pack(pady=10)

    button3 = ctk.CTkButton(master=content_frame3, text="Books", font=("Arial", 16), width=150, height=40, command=button3_action)
    button3.pack(pady=10)

    frame4 = ctk.CTkFrame(master=menu_frame, width=250, height=250, border_color="#A9A9A9", border_width=2)
    frame4.place(relx=0.35, rely=0.75, anchor="center")

    content_frame4 = ctk.CTkFrame(master=frame4)
    content_frame4.pack(pady=10, padx=10, expand=True, fill="both")

    empty_label4 = ctk.CTkLabel(master=content_frame4, text="", width=200, height=0)
    empty_label4.pack(pady=10)

    img4 = Image.open("images/Author.png")
    photo4 = ctk.CTkImage(light_image=img4, dark_image=img4, size=(100, 100))
    image_label4 = ctk.CTkLabel(master=content_frame4, image=photo4, text="")
    image_label4.pack(pady=10)

    button4 = ctk.CTkButton(master=content_frame4, text="Authors", font=("Arial", 16), width=150, height=40, command=button4_action)
    button4.pack(pady=10)

    frame5 = ctk.CTkFrame(master=menu_frame, width=250, height=250, border_color="#A9A9A9", border_width=2)
    frame5.place(relx=0.65, rely=0.75, anchor="center")

    content_frame5 = ctk.CTkFrame(master=frame5)
    content_frame5.pack(pady=10, padx=10, expand=True, fill="both")

    empty_label5 = ctk.CTkLabel(master=content_frame5, text="", width=200, height=0)
    empty_label5.pack(pady=10)

    img5 = Image.open("images/bookcopy.png")
    photo5 = ctk.CTkImage(light_image=img5, dark_image=img5, size=(100, 100))
    image_label5 = ctk.CTkLabel(master=content_frame5, image=photo5, text="")
    image_label5.pack(pady=10)

    button5 = ctk.CTkButton(master=content_frame5, text="Book Copies", font=("Arial", 16), width=150, height=40, command=button5_action)
    button5.pack(pady=10)
