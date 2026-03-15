import sqlite3
from tkinter import *
from tkinter import ttk, messagebox



class CategoryManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Category Management System")
        self.root.geometry("800x400")

        Label(self.root, text="Manage Product Category", font=("Arial", 16, "bold"), bg="darkgreen", fg="white").pack(
            side=TOP, fill=X)

        # Input Fields
        Label(self.root, text="Enter Category Name:").place(x=20, y=50)
        self.category_name = Entry(self.root)
        self.category_name.place(x=200, y=50, width=200)

        # Buttons
        Button(self.root, text="ADD", bg="green", fg="white", command=self.add_category).place(x=420, y=47, width=80,
                                                                                               height=25)
        Button(self.root, text="DELETE", bg="red", fg="white", command=self.delete_category).place(x=520, y=47,
                                                                                                   width=80, height=25)

        # Category Table
        self.category_table = ttk.Treeview(self.root, columns=("id", "name"), show="headings")
        self.category_table.place(x=20, y=100, width=600, height=250)

        self.category_table.heading("id", text="C ID")
        self.category_table.heading("name", text="Name")

        self.category_table.column("id", width=50)
        self.category_table.column("name", width=200)

        self.category_table.bind("<ButtonRelease-1>", self.get_selected_row)
        self.fetch_categories()

    # Add Category
    def add_category(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO category (Name) VALUES (?)", (self.category_name.get(),))
            con.commit()
            messagebox.showinfo("Success", "Category Added Successfully")
            self.fetch_categories()
            self.category_name.delete(0, END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Category Already Exists!")
        con.close()

    # Fetch Categories
    def fetch_categories(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM category")
        rows = cur.fetchall()
        con.close()

        self.category_table.delete(*self.category_table.get_children())
        for row in rows:
            self.category_table.insert("", END, values=row)

    # Get Selected Row
    def get_selected_row(self, event):
        selected = self.category_table.focus()
        data = self.category_table.item(selected)["values"]
        if data:
            self.category_name.delete(0, END)
            self.category_name.insert(0, data[1])

    # Delete Category
    def delete_category(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("DELETE FROM category WHERE Name=?", (self.category_name.get(),))
        con.commit()
        con.close()
        self.fetch_categories()
        self.category_name.delete(0, END)
        messagebox.showinfo("Deleted", "Category Deleted Successfully")


# Link to Dashboard
def open_category_page():
    root = Tk()
    CategoryManagement(root)
    root.mainloop()
