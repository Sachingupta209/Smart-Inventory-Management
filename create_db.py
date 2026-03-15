import sqlite3

def setup_database():
    conn = sqlite3.connect("ims.db")
    cursor = conn.cursor()

    # Employee Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee(
            E_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            E_mail TEXT,
            Gender TEXT,
            Contact TEXT,
            DOB TEXT,
            DOJ TEXT,
            Password TEXT,
            UType TEXT,
            Address TEXT,
            Salary TEXT
        )
    """)

    # Supplier Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS supplier (
            Sup_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            Invoice_No TEXT UNIQUE, 
            Name TEXT, 
            Contact TEXT, 
            Description TEXT
        )
    """)

    # Category Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            C_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            Name TEXT UNIQUE
        )
    """)

    # Products Table with Foreign Keys
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            supplier_id INTEGER,
            name TEXT UNIQUE,
            price REAL,
            qty INTEGER,
            status TEXT,
            FOREIGN KEY (category_id) REFERENCES category(C_ID),
            FOREIGN KEY (supplier_id) REFERENCES supplier(Sup_id)
        )
    """)

    # Invoice Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT UNIQUE,
            customer_name TEXT,
            total_amount REAL,
            date TEXT
        )
    """)

    # Bill Details Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT,
            product TEXT,
            quantity INTEGER,
            price REAL,
            discount REAL,
            tax REAL,
            total REAL,
            FOREIGN KEY (invoice_no) REFERENCES invoices(invoice_no)
        )
    """)


    conn.commit()
    conn.close()

# Run the database setup
setup_database()
