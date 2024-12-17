import customtkinter as ctk
from login import create_login_window
from admin import admin_page
from menu import create_menu_window
from database import creat_DataBase
def main():
    global window
    window = ctk.CTk()
    window.title("Library Management System")   
    window.geometry('850x650')
    creat_DataBase()
    window.iconbitmap("images/iconwindow.ico")
    ctk.set_appearance_mode("Dark")
    
    create_login_window(window, redirect_to_page)

    window.mainloop()
    
    
def redirect_to_page(role ,employee_id ):
    for widget in window.winfo_children():  
        widget.destroy()

    if role == "admin":
        admin_page(window)
    elif role == "emp":
        create_menu_window(window , employee_id)

if __name__ == "__main__":
    main()
