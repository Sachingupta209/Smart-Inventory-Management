import sqlite3
import bcrypt
import tkinter as tk
from tkinter import Toplevel, messagebox
from dashbord import IMS  # Import your dashboard

# Function to hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Function to check password
def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

# Setup DB and default admin
def setup_database():
    conn = sqlite3.connect("ims.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            E_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            E_mail TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL,
            UType TEXT CHECK(UType IN ('Admin', 'Staff')) NOT NULL
        )
    """)
    admin_email = "admin@example.com"
    cursor.execute("SELECT * FROM employee WHERE E_mail=?", (admin_email,))
    if cursor.fetchone() is None:
        hashed_pw = hash_password("admin123")
        cursor.execute("INSERT INTO employee (Name, E_mail, Password, UType) VALUES (?, ?, ?, ?)",
                       ("Admin", admin_email, hashed_pw, "Admin"))
        conn.commit()
    conn.close()

# Show toast message
def show_popup(message):
    popup = Toplevel(root)
    popup.geometry("250x100+600+300")
    popup.overrideredirect(True)
    popup.configure(bg="#1e88e5")
    tk.Label(popup, text=message, font=("Arial", 12, "bold"), fg="white", bg="#1e88e5").pack(pady=20)
    popup.after(2000, popup.destroy)

# Open dashboard with user role and email
def open_dashboard(role, email):
    root.destroy()
    dashboard_root = tk.Tk()
    IMS(dashboard_root, user_role=role, user_email=email)
    dashboard_root.mainloop()

# Login process
def login():
    email = entry_email.get()
    password = entry_password.get()
    conn = sqlite3.connect("ims.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Password, UType FROM employee WHERE E_mail=?", (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password, role = result
        if check_password(stored_password, password):
            show_popup(f"Welcome {role}!")
            root.after(2000, open_dashboard, role, email)
        else:
            show_popup("Incorrect Password!")
    else:
        show_popup("User Not Found!")

# GUI
root = tk.Tk()
root.title("Login - Inventory Management System")
root.geometry("400x400")
root.resizable(False, False)
root.configure(bg="#e3f2fd")

login_frame = tk.Frame(root, bg="white", bd=5, relief="ridge")
login_frame.place(x=50, y=80, width=300, height=250)

tk.Label(login_frame, text="Login", font=("Arial", 20, "bold"), fg="#0d47a1", bg="white").pack(pady=10)

tk.Label(login_frame, text="Email:", font=("Arial", 12, "bold"), bg="white", fg="#1a237e").pack(pady=5)
entry_email = tk.Entry(login_frame, font=("Arial", 12), bd=2, relief="solid")
entry_email.pack(pady=5, padx=10, ipadx=5)

tk.Label(login_frame, text="Password:", font=("Arial", 12, "bold"), bg="white", fg="#1a237e").pack(pady=5)
entry_password = tk.Entry(login_frame, show="*", font=("Arial", 12), bd=2, relief="solid")
entry_password.pack(pady=5, padx=10, ipadx=5)

tk.Button(login_frame, text="Login", command=login, font=("Arial", 12, "bold"),
          bg="#1e88e5", fg="white", cursor="hand2", relief="raised").pack(pady=15, ipadx=15)

# Setup database
setup_database()

root.mainloop()
