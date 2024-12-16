import sqlite3

def creat_DataBase():
 
    db_file = "library.db"

   
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON;")  
    cursor = conn.cursor()
    

    cursor.executescript("""
    -- إنشاء جدول الموظفين
    CREATE TABLE IF NOT EXISTS Employee (
        Employee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First_name TEXT NOT NULL,
        Last_name TEXT NOT NULL,
        Email TEXT NOT NULL,
        Manager_ID INTEGER,
        FOREIGN KEY (Manager_ID) REFERENCES Employee(Employee_ID) ON DELETE RESTRICT
    );

    -- إنشاء جدول المؤلفين
    CREATE TABLE IF NOT EXISTS Author (
        Author_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Author_Name TEXT NOT NULL,
        Nationality TEXT,
        Employee_ID INTEGER,
        FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON DELETE RESTRICT
    );

    -- إنشاء جدول تفاصيل الكتب
    CREATE TABLE IF NOT EXISTS Book_Details (
        ISBN TEXT PRIMARY KEY,
        Title TEXT NOT NULL,
        Category TEXT,
        Author_ID INTEGER,
        Publish_year INTEGER,
        Copies_available INTEGER,
        Copies_Borrowed INTEGER,
        Employee_ID INTEGER,
        FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON DELETE RESTRICT,
        FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID) ON DELETE SET NULL
    );

    -- إنشاء جدول نسخ الكتب
    CREATE TABLE IF NOT EXISTS Book_Copy (
        Book_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Status TEXT CHECK (Status IN ('Available', 'Borrowed')) NOT NULL,
        ISBN TEXT NOT NULL,
        Employee_ID INTEGER,
        FOREIGN KEY (ISBN) REFERENCES Book_Details(ISBN) ON DELETE RESTRICT,
        FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON DELETE RESTRICT
    );

    -- إنشاء جدول الأعضاء
    CREATE TABLE IF NOT EXISTS Member (
        Member_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First_name TEXT NOT NULL,
        Last_name TEXT NOT NULL,
        Address TEXT,
        Phone TEXT,
        Email TEXT,
        Employee_ID INTEGER,
        FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON DELETE RESTRICT
    );
    -- إنشاء جدول الإعارات
        CREATE TABLE IF NOT EXISTS Borrow (
        Borrow_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Borrow_date TEXT NOT NULL,
        Due_date TEXT,
        Return_date TEXT,
        Borrow_Duration INTEGER,
        Book_ID INTEGER NOT NULL,
        Returned TEXT CHECK (Returned IN ('Yes', 'No')) NOT NULL,
        Employee_ID INTEGER,
        Member_ID INTEGER NOT NULL,
        FOREIGN KEY (Book_ID) REFERENCES Book_Copy(Book_ID) ON DELETE RESTRICT,
        FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON DELETE RESTRICT,
        FOREIGN KEY (Member_ID) REFERENCES Member(Member_ID) ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS Book_Authors (
    ISBN TEXT NOT NULL,
    Author_ID INTEGER,
    FOREIGN KEY (ISBN) REFERENCES Book_Details(ISBN) ON DELETE SET NULL,
    FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID) ON DELETE SET NULL
);
""")
    employees = [
        (1, "Ahmed", "Hamed", "ah456408@gmail.com", None),
        (2, "Ahmed", "Aly", "Ahmedaly@gmail.com", 1),
        (3, "Ahmed", "Abdelkader", "Ahmedabdelkader@gmail.com", 1),
        (4, "Attia", "mansour", "Attiamansour@gmail.com", 1),
        (5, "Mohamed", "Hassan", "Mohamedhassan@gmail.com", 1),
        (6, "باشااا البلد", "Ahmed Hamed", "emp", 1)
    ]   

    authors = [
        (1, "George Orwell", "British", 1),
        (2, "J.K. Rowling", "British", 2),
        (3, "Mark Twain", "American", 3)
    ]

    book_details = [
        ("9780451524935", "1984", "Dystopian", 1, 1949, 5, 0, 1),
        ("9780747532743", "Harry Potter and the Philosopher's Stone", "Fantasy", 2, 1997, 3, 1, 2),
        ("9780486280615", "The Adventures of Huckleberry Finn", "Adventure", 3, 1884, 2, 0, 3)
    ]

    book_copies = [
        (1, "Available", "9780451524935", 1),
        (2, "Available", "9780451524935", 1),
        (3, "Available", "9780747532743", 2),
        (4, "Available", "9780747532743", 2),
        (5, "Available", "9780486280615", 3)
    ]

    members = [
        (1, "John", "Doe", "123 Elm Street", "555-1234", "john.doe@example.com", 1),
        (2, "Emily", "Clark", "456 Oak Avenue", "555-5678", "emily.clark@example.com", 2),
        (3, "Michael", "Smith", "789 Pine Road", "555-9012", "michael.smith@example.com", 3)
    ]

    borrows = [
        (1, "2024-12-01","2024-12-11", "2024-12-10", 10, 2,'Yes', 1, 1),
        (2, "2024-12-05" ,"2024-12-15", "2024-12-15", 10, 4,'Yes', 2, 2),
        (3, "2024-12-07","2024-12-21", None, 14, 5,'No', 3, 3)  # لا تزال مستعارة
    ]
    def insert_data():
        cursor.executemany("INSERT OR IGNORE INTO Employee VALUES (?, ?, ?, ?, ?)", employees)
        cursor.executemany("INSERT OR IGNORE INTO Author VALUES (?, ?, ?, ?)", authors)
        cursor.executemany("INSERT OR IGNORE INTO Book_Details VALUES (?, ?, ?, ?, ?, ?, ?, ?)", book_details)
        cursor.executemany("INSERT OR IGNORE INTO Book_Copy VALUES (?, ?, ?, ?)", book_copies)
        cursor.executemany("INSERT OR IGNORE INTO Member VALUES (?, ?, ?, ?, ?, ?, ?)", members)
        cursor.executemany("INSERT OR IGNORE INTO Borrow VALUES (?,?, ?, ?, ?, ?, ?, ?,?)", borrows)
    insert_data()

    conn.commit()
    conn.close()

    print("Database created and data inserted successfully!")
