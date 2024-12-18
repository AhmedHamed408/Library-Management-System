import sqlite3

def creat_DataBase():
 
    db_file = "library.db"

   
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON;")  
    cursor = conn.cursor()
    

    cursor.executescript("""
    
    CREATE TABLE IF NOT EXISTS Employee (
        Employee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First_name TEXT NOT NULL,
        Last_name TEXT NOT NULL,
        Email TEXT NOT NULL,
        Manager_ID INTEGER,
        FOREIGN KEY (Manager_ID) REFERENCES Employee(Employee_ID) ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS Author (
        Author_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Author_Name TEXT NOT NULL,
        Nationality TEXT,
        Employee_ID INTEGER,
        FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS Book_Details (
        ISBN TEXT PRIMARY KEY,
        Title TEXT NOT NULL,
        Category TEXT,
        Publish_year INTEGER,
        Copies_available INTEGER,
        Copies_Borrowed INTEGER,
        Employee_ID INTEGER,
        FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS Book_Copy (
        Book_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Status TEXT CHECK (Status IN ('Available', 'Borrowed')) NOT NULL,
        ISBN TEXT NOT NULL,
        Employee_ID INTEGER,
        FOREIGN KEY (ISBN) REFERENCES Book_Details(ISBN) ON DELETE RESTRICT,
        FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON DELETE RESTRICT
    );

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
        PRIMARY KEY (ISBN, Author_ID),
        FOREIGN KEY (ISBN) REFERENCES Book_Details(ISBN) ON DELETE CASCADE,
        FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID) ON DELETE RESTRICT
    );
    """)


    employees = [
        (1, "Admin", "Admin", "admin@gmail.com", None),
        (2, "Librarian", "Test", "emp@gmail.com", 1)
    ]   

    authors = [
        (1, 'Naguib Mahfouz', 'Egyptian', 2),
        (2, 'Taha Hussein', 'Egyptian', 2),
        (3, 'Youssef Ziedan', 'Egyptian', 2),
        (4, 'Sonallah Ibrahim', 'Egyptian', 2),
        (5, 'Alaa Al Aswany', 'Egyptian', 2),
        (6, 'Mohammed Makhzangi', 'Egyptian', 2),
        (7, 'Zaynab Fawwaz', 'Egyptian', 2),
        (8, 'Ibrahim Abdel Meguid', 'Egyptian', 2),
        (9, 'Gamila Shams', 'Egyptian', 2),
        (10, 'Ahmed Zewail', 'Egyptian', 2)
    ]

    book_details = [
        ('978-977-16-5514-2', 'Palace Walk', 'Fiction', 1956, 10, 2, 2),
        ('978-977-16-1165-9', 'The Days', 'Biography', 1954, 8, 3, 2),
        ('978-977-72-1883-7', 'Azazeel', 'Historical Fiction', 2008, 15, 5, 2),
        ('978-977-05-5890-5', 'The Yacoubian Building', 'Drama', 2002, 12, 3, 2),
        ('978-977-51-7280-5', 'The Invisible Man', 'Fiction', 2006, 20, 4, 2),
        ('978-977-04-4136-9', 'The Cairo Trilogy', 'Fiction', 2002, 8, 2, 2),
        ('978-977-21-2053-3', 'In the Eye of the Sun', 'Drama', 1992, 10, 1, 2),
        ('978-977-16-5545-7', 'The Miramar', 'Fiction', 1967, 5, 1, 2),
        ('978-977-21-8231-3', 'Midaq Alley', 'Novel', 1947, 9, 4, 2),
        ('978-977-16-0400-9', 'The Road to Faiyum', 'Fiction', 1997, 7, 2, 2)
    ]

    book_copies = [
        (1, 'Available', '978-977-16-5514-2', 2),
        (2, 'Borrowed', '978-977-16-5514-2', 2),
        (3, 'Available', '978-977-16-1165-9', 2),
        (4, 'Available', '978-977-72-1883-7', 2),
        (5, 'Borrowed', '978-977-72-1883-7', 2),
        (6, 'Available', '978-977-05-5890-5', 2),
        (7, 'Borrowed', '978-977-05-5890-5', 2),
        (8, 'Available', '978-977-51-7280-5', 2),
        (9, 'Available', '978-977-04-4136-9', 2),
        (10, 'Borrowed', '978-977-21-2053-3', 2)
    ]

    members = [
        (1, "Omar", "Hassan", "El-Maadi, Cairo", "01112345678", "omar.hassan@library.com", 2),
        (2, "Mona", "Gamal", "Nasr City, Cairo", "01098765432", "mona.gamal@library.com", 2),
        (3, "Ali", "Mahmoud", "Helwan, Cairo", "01234567890", "ali.mahmoud@library.com", 2),
        (4, "Sara", "Ahmed", "Zamalek, Cairo", "01011223344", "sara.ahmed@library.com", 2),
        (5, "Hossam", "El-Banna", "Dokki, Cairo", "01155667788", "hossam.elbanna@library.com", 2),
        (6, "Laila", "Fahmy", "Mohandessin, Cairo", "01022334455", "laila.fahmy@library.com", 2),
        (7, "Amira", "Mohamed", "New Cairo, Cairo", "01177665544", "amira.mohamed@library.com", 2),
        (8, "Mohamed", "El-Sayed", "6th of October, Giza", "01233445566", "mohamed.elsayed@library.com", 2),
        (9, "Tarek", "El-Shazly", "Maadi, Cairo", "01188776655", "tarek.elshazly@library.com", 2),
        (10, "Mariam", "Rashad", "Nasr City, Cairo", "01022334488", "mariam.rashad@library.com", 2),
        (11, 'Ahmed', 'Ali', 'Cairo, Egypt', '01023456789', 'ahmedali@example.com', 2),
        (12, 'Mona', 'Hassan', 'Giza, Egypt', '01234567890', 'monahassan@example.com', 2),
        (13, 'Mohamed', 'Salah', 'Alexandria, Egypt', '01122334455', 'mohamedsalah@example.com', 2),
        (14, 'Fatima', 'Mohamed', 'Cairo, Egypt', '01098765432', 'fatimamohamed@example.com', 2),
        (15, 'Youssef', 'Fayad', 'Tanta, Egypt', '01566543210', 'yousseffayad@example.com', 2),
        (16, 'Sara', 'Abdelkader', 'Aswan, Egypt', '01234569876', 'saraabdelkader@example.com', 2),
        (17, 'Omar', 'Hussein', 'Cairo, Egypt', '01011223344', 'omarhussein@example.com', 2),
        (18, 'Rania', 'El-Shazly', 'Giza, Egypt', '01022334455', 'raniaelshazly@example.com', 2),
        (19, 'Yasmine', 'Tarek', 'Cairo, Egypt', '01066778899', 'yasminetarek@example.com', 2),
        (20, 'Hassan', 'Gamal', 'Alexandria, Egypt', '01124567890', 'hassangamal@example.com', 2)
    ]

    borrows = [
        (1, '2024-12-01', '2024-12-15', '2024-12-10', 14, 1, 'Yes', 2, 1),
        (2, '2024-12-02', '2024-12-16', '2024-12-12', 14, 2, 'Yes', 2, 2),
        (3, '2024-12-03', '2024-12-17', None, 14, 3, 'No', 2, 3),
        (4, '2024-12-04', '2024-12-18', None, 14, 4, 'No', 2, 4),
        (5, '2024-12-05', '2024-12-19', None, 14, 5, 'No', 2, 5),
        (6, '2024-12-06', '2024-12-20', None, 14, 6, 'No', 2, 6),
        (7, '2024-12-07', '2024-12-21', None, 14, 7, 'No', 2, 7),
        (8, '2024-12-08', '2024-12-22', None, 14, 8, 'No', 2, 8),
        (9, '2024-12-09', '2024-12-23', None, 14, 9, 'No', 2, 9),
        (10, '2024-12-10', '2024-12-24', None, 14, 10, 'No', 2, 10)
    ]
    Book_Authors = [
        ('978-977-16-5514-2', 1),
        ('978-977-16-1165-9', 2),
        ('978-977-72-1883-7', 3),
        ('978-977-05-5890-5', 4),
        ('978-977-51-7280-5', 5),
        ('978-977-04-4136-9', 6),
        ('978-977-21-2053-3', 7),
        ('978-977-16-5545-7', 8),
        ('978-977-21-8231-3', 9),
        ('978-977-16-0400-9', 10) 
    ]

    def insert_data():
        cursor.executemany("INSERT OR IGNORE INTO Employee VALUES (?, ?, ?, ?, ?)", employees)
        cursor.executemany("INSERT OR IGNORE INTO Author VALUES (?, ?, ?, ?)", authors)
        cursor.executemany("INSERT OR IGNORE INTO Book_Details VALUES ( ?, ?, ?, ?, ?, ?, ?)", book_details)
        cursor.executemany("INSERT OR IGNORE INTO Book_Copy VALUES (?, ?, ?, ?)", book_copies)
        cursor.executemany("INSERT OR IGNORE INTO Member VALUES (?, ?, ?, ?, ?, ?, ?)", members)
        cursor.executemany("INSERT OR IGNORE INTO Borrow VALUES (?,?, ?, ?, ?, ?, ?, ?,?)", borrows)
        cursor.executemany("INSERT OR IGNORE INTO Book_Authors VALUES (?,?)", Book_Authors)
    
    insert_data()

    conn.commit()
    conn.close()

    print("Database Connected Successfully")
