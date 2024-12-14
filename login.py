import customtkinter as ctk
from PIL import Image
import sqlite3
def create_login_window(master, redirect_callback):
  
    state = {"password_visible": False}

    def mood_button_clicked():
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            text_label_main.configure(text_color="black")
        else:
            ctk.set_appearance_mode("Dark")
            text_label_main.configure(text_color="white")
            

    def toggle_password():
        if state["password_visible"]:
            pass_entry.configure(show="●")
            eye_button.configure(image=eye_icon)
            state["password_visible"] = False
        else:
            pass_entry.configure(show="")
            eye_button.configure(image=eye_icon_closed)
            state["password_visible"] = True

    def login_button_clicked():
        conn = sqlite3.connect("library.db")
        cur = conn.cursor()

       
        input_email = user_entry.get()
        input_password = pass_entry.get()

       
       
        
        try:
           
            cur.execute("SELECT Employee_ID FROM Employee WHERE Email = ?", (input_email,))
            result = cur.fetchone()

            if result and str(result[0]) == input_password:   
                if int(result[0]) == 1: 
                    redirect_callback("admin" , result[0])
                else:
                    redirect_callback("emp" , result[0])
            else:
                
                invalid_login_label.grid(row=3, column=0, columnspan=2, padx=1, pady=1)
        except sqlite3.Error as e:
            
            print("Database error:", e)
            invalid_login_label.grid(row=3, column=0, columnspan=2, padx=1, pady=1)
        finally:
            
            conn.close()

   
    image_path_main = "images/learning-management-system.png"
    img_main = Image.open(image_path_main)
    photo_main = ctk.CTkImage(light_image=img_main, dark_image=img_main, size=(60, 60))
    image_label = ctk.CTkLabel(master=master, image=photo_main, text="")
    image_label.pack(pady=10)

    text_label_main = ctk.CTkLabel(
        master=master, 
        text="Library Management System", 
        font=("Arial", 26, "bold")
    )
    text_label_main.pack(pady=10)

    
    
     
    frame_login_external = ctk.CTkFrame(
        master=master, 
        width=8000, 
        height=550, 
        border_color="#87CEEB", 
        border_width=0.6
    )
    frame_login_external.place(relx=0.5, rely=0.5, anchor="center")
    
    frame_login = ctk.CTkFrame(master=frame_login_external)
    frame_login.pack(pady=10, padx=10, expand=True, fill="both")
    
    login_label = ctk.CTkLabel(master=frame_login, text="Login", font=("Arial", 24, "bold"))
    login_label.grid(row=0, column=0, columnspan=3, pady=30)

    user_label = ctk.CTkLabel(master=frame_login, text="E-Mail:", font=("Arial", 16))
    user_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    user_entry = ctk.CTkEntry(master=frame_login, width=170, font=("Arial", 16))
    user_entry.grid(row=1, column=1, padx=10, pady=10)

    pass_label = ctk.CTkLabel(master=frame_login, text="ID:", font=("Arial", 16))
    pass_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    pass_entry = ctk.CTkEntry(master=frame_login, show="●", width=170 , font=("Arial", 16))
    pass_entry.grid(row=2, column=1, padx=10, pady=10)

    
    eye_icon = ctk.CTkImage(Image.open("images/eye.png"), size=(20, 20))
    eye_icon_closed = ctk.CTkImage(Image.open("images/hidden.png"), size=(20, 20))
    eye_button = ctk.CTkButton(master=frame_login, image=eye_icon, text="", width=30, command=toggle_password)
    eye_button.grid(row=2, column=2, padx=10, pady=10)

    
    invalid = "*Invalid Username or Password"
    invalid_login_label = ctk.CTkLabel(master=frame_login, text=invalid, font=("Arial", 16, "bold"))
    invalid_login_label.configure(text_color="red")

    
    image_path = "images/login-icon-3042.png"
    img = Image.open(image_path)
    photo = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))

    login_button = ctk.CTkButton(
        master=frame_login, 
        text="Login", 
        width=150, 
        height=50, 
        font=("Arial", 16), 
        image=photo, 
        command=login_button_clicked
    )
    login_button.grid(row=4, column=0, columnspan=3, pady=30)

     
    image_mood_main = "images/brightness-and-contrast.png"
    img_mood = Image.open(image_mood_main)
    photo_mood = ctk.CTkImage(light_image=img_mood, dark_image=img_mood, size=(20, 20))
    mood_button = ctk.CTkButton(
        master=master, 
        text="", 
        width=25, 
        height=30, 
        font=("Arial", 16), 
        image=photo_mood, 
        command=mood_button_clicked
    )
    mood_button.place(x=20, y=20)

