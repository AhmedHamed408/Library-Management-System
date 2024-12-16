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
        (1, "Naguib Mahfouz", "Egyptian", 2),
        (2, "Taha Hussein", "Egyptian", 3),
        (3, "Youssef Idris", "Egyptian", 4),
        (4, "Ibrahim Aslan", "Egyptian", 5),
        (5, "Radwa Ashour", "Egyptian", 6),
        (6, "Sonallah Ibrahim", "Egyptian", 2),
        (7, "Alaa Al Aswany", "Egyptian", 3),
        (8, "Mahmoud El-Wardany", "Egyptian", 4),
        (9, "Monir Al-Mahdy", "Egyptian", 5),
        (10, "Maha Hassan", "Egyptian", 6)
    ]

    book_details = [
        ("9789997476813", "موسم الهجرة إلى الشمال", "Fiction", 1, 1966, 10, 2, 2),
        ("9789770911167", "الأيام", "Biography", 2, 1929, 7, 3, 3),
        ("9789775052162", "جمهورية كأن", "Drama", 3, 1967, 5, 1, 4),
        ("9789775231981", "تحت سقف واحد", "Fiction", 4, 1992, 8, 4, 5),
        ("9789774893264", "الجنرال في متاهة", "Historical Fiction", 5, 2002, 6, 2, 6),
        ("9789772563541", "الشرف", "Drama", 6, 1996, 12, 0, 2),
        ("9789776438436", "عمارة يعقوبيان", "Fiction", 7, 2002, 15, 5, 3),
        ("9789776394655", "أشياء خافتة", "Poetry", 8, 2001, 4, 1, 4),
        ("9789771430561", "عائلة هاربين من الرياح", "Novel", 9, 1999, 11, 3, 5),
        ("9789775690989", "حكايتي مع البحر", "Adventure", 10, 2008, 9, 0, 6)
    ]

    book_copies = [
        (1, "Available", "9789997476813", 2),
        (2, "Available", "9789997476813", 2),
        (3, "Available", "9789770911167", 3),
        (4, "Available", "9789770911167", 3),
        (5, "Available", "9789775052162", 4),
        (6, "Available", "9789775052162", 4),
        (7, "Available", "9789775231981", 5),
        (8, "Available", "9789775231981", 5),
        (9, "Available", "9789774893264", 6),
        (10, "Available", "9789774893264", 6),
        (11, "Available", "9789772563541", 2),
        (12, "Available", "9789772563541", 2),
        (13, "Available", "9789776438436", 3),
        (14, "Available", "9789776438436", 3),
        (15, "Available", "9789776394655", 4),
        (16, "Available", "9789776394655", 4),
        (17, "Available", "9789771430561", 5),
        (18, "Available", "9789771430561", 5),
        (19, "Available", "9789775690989", 6),
        (20, "Available", "9789775690989", 6)
    ]

    members = [
        (1, "Omar", "Hassan", "El-Maadi, Cairo", "01112345678", "omar.hassan@library.com", 2),
        (2, "Mona", "Gamal", "Nasr City, Cairo", "01098765432", "mona.gamal@library.com", 3),
        (3, "Ali", "Mahmoud", "Helwan, Cairo", "01234567890", "ali.mahmoud@library.com", 4),
        (4, "Sara", "Ahmed", "Zamalek, Cairo", "01011223344", "sara.ahmed@library.com", 5),
        (5, "Hossam", "El-Banna", "Dokki, Cairo", "01155667788", "hossam.elbanna@library.com", 6),
        (6, "Laila", "Fahmy", "Mohandessin, Cairo", "01022334455", "laila.fahmy@library.com", 2),
        (7, "Amira", "Mohamed", "New Cairo, Cairo", "01177665544", "amira.mohamed@library.com", 3),
        (8, "Mohamed", "El-Sayed", "6th of October, Giza", "01233445566", "mohamed.elsayed@library.com", 4),
        (9, "Tarek", "El-Shazly", "Maadi, Cairo", "01188776655", "tarek.elshazly@library.com", 5),
        (10, "Mariam", "Rashad", "Nasr City, Cairo", "01022334488", "mariam.rashad@library.com", 6)
    ]

    borrows = [
        (1, "2024-12-01", "2024-12-11", "2024-12-10", 10, 2, 'Yes', 2, 1),
        (2, "2024-12-05", "2024-12-15", "2024-12-15", 10, 4, 'Yes', 3, 2),
        (3, "2024-12-07", "2024-12-21", None, 14, 5, 'No', 4, 3),
        (4, "2024-12-10", "2024-12-20", None, 10, 6, 'No', 5, 4),
        (5, "2024-12-12", "2024-12-22", None, 10, 7, 'No', 6, 5),
        (6, "2024-12-15", "2024-12-25", None, 10, 8, 'No', 2, 6),
        (7, "2024-12-18", "2024-12-28", None, 10, 9, 'No', 3, 7),
        (8, "2024-12-20", "2024-12-30", None, 10, 10, 'No', 4, 8),
        (9, "2024-12-23", "2024-12-31", None, 10, 11, 'No', 5, 9),
        (10, "2024-12-25", "2025-01-04", None, 10, 12, 'No', 6, 10)
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
