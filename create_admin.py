import sqlite3
import bcrypt

conn = sqlite3.connect("ims.db")
cursor = conn.cursor()

name = "Administrator"
email = "admin@ims.com"
password = "admin123"

hashed_password = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
).decode()

cursor.execute("""
INSERT INTO employee
(Name,E_mail,Gender,Contact,DOB,DOJ,Password,UType,Address,Salary)
VALUES (?,?,?,?,?,?,?,?,?,?)
""",
(
    name,
    email,
    "Male",
    "9999999999",
    "01/01/2000",
    "01/01/2025",
    hashed_password,
    "Admin",
    "System",
    "0"
))

conn.commit()
conn.close()

print("Admin Created Successfully!")