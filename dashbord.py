import os
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from employee import EmployeeClass
from supplier import SupplierManagement
from category import CategoryManagement
from product import ProductManagement
from sales_billing import CustomerBilling

import subprocess  # To restart login.py on logout

class IMS:
    def __init__(self, root, user_role=None, user_email=None):
        self.root = root
        self.user_role = user_role
        self.user_email = user_email

        self.root.geometry("1350x700+0+0")
        self.root.title(" Smart Inventory Management System")
        self.root.config(bg="#f4f4f4")

        # Title Label
        self.title = Label(
            self.root,
            text=" Smart Inventory Management System",
            font=("times new roman", 30, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20
        )
        self.title.place(x=0, y=0, relwidth=1, height=70)

        # Logout Button
        btn_logout = Button(
            self.root,
            text="Logout",
            font=("times new roman", 20, "bold"),
            bg="red",
            fg="white",
            cursor="hand2",
            relief=RAISED,
            command=self.logout
        )
        btn_logout.place(x=1100, y=15, height=40, width=150)

        # Logged-in User Info Label
        lbl_user_info = Label(
            self.root,
            text=f"Logged in as: {self.user_role} ({self.user_email})",
            font=("times new roman", 14, "bold"),
            fg="#333",
            bg="#f4f4f4"
        )
        lbl_user_info.place(x=900, y=70)

        # Left Menu Frame
        self.left_menu = Frame(self.root, bd=2, relief=RIDGE, bg="#ffffff")
        self.left_menu.place(x=0, y=102, width=220, height=565)

        lbl_menu = Label(
            self.left_menu,
            text="Menu",
            font=("times new roman", 20, "bold"),
            bg="#009688",
            fg="white",
            pady=10
        )
        lbl_menu.pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file="menu.png")  # Optional icon

        # Sidebar Buttons with Hover Effect
        def on_enter(e): e.widget.config(bg="#009688", fg="white")
        def on_leave(e): e.widget.config(bg="white", fg="black")

        menu_items = []

        if self.user_role == "Admin":
            menu_items.append(("User", self.employee))

        menu_items += [
            ("Supplier", self.supplier),
            ("Category", self.category),
            ("Product", self.product),
            ("Sales", self.sales),
            ("Exit", root.quit)
        ]

        for text, cmd in menu_items:
            btn = Button(
                self.left_menu,
                text=text,
                font=("times new roman", 18, "bold"),
                bg="white",
                fg="black",
                bd=3,
                cursor="hand2",
                relief=RIDGE,
                padx=5,
                anchor="w",
                command=cmd
            )
            btn.pack(side=TOP, fill=X, pady=2)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Dashboard Cards
        card_bg = "#42a5f5"
        card_text = "white"
        card_font = ("goudy old style", 20, "bold")

        # Employee Card - Show only for Admin
        self.lbl_emp = Label(self.root, text="Total Users\n[ 0 ]", bg=card_bg, fg=card_text,
                             font=card_font, bd=5, relief=RAISED)
        if self.user_role == "Admin":
            self.lbl_emp.place(x=280, y=120, height=150, width=280)

        # Other Cards
        self.lbl_sup = Label(self.root, text="Total Suppliers\n[ 0 ]", bg=card_bg, fg=card_text,
                             font=card_font, bd=5, relief=RAISED)
        self.lbl_sup.place(x=280 if self.user_role != "Admin" else 620, y=120, height=150, width=280)

        self.lbl_cate = Label(self.root, text="Total Categories\n[ 0 ]", bg=card_bg, fg=card_text,
                              font=card_font, bd=5, relief=RAISED)
        self.lbl_cate.place(x=620 if self.user_role != "Admin" else 960, y=120, height=150, width=280)

        self.lbl_prod = Label(self.root, text="Total Products\n[ 0 ]", bg=card_bg, fg=card_text,
                              font=card_font, bd=5, relief=RAISED)
        self.lbl_prod.place(x=280, y=300, height=150, width=280)

        self.lbl_sales = Label(self.root, text="Total Sales\n[ 0 ]", bg=card_bg, fg=card_text,
                               font=card_font, bd=5, relief=RAISED)
        self.lbl_sales.place(x=620, y=300, height=150, width=280)

        # Update dashboard counts
        self.update_dashboard_counts()

    def update_dashboard_counts(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM employee")
            emp_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM supplier")
            sup_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM category")
            cate_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM products")
            prod_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM invoices")
            sales_count = cur.fetchone()[0]

            if self.user_role == "Admin":
                self.lbl_emp.config(text=f"Total Users\n[ {emp_count} ]")
            self.lbl_sup.config(text=f"Total Suppliers\n[ {sup_count} ]")
            self.lbl_cate.config(text=f"Total Categories\n[ {cate_count} ]")
            self.lbl_prod.config(text=f"Total Products\n[ {prod_count} ]")
            self.lbl_sales.config(text=f"Total Sales\n[ {sales_count} ]")

        except Exception as ex:
            print(f"Error: {str(ex)}")
        finally:
            con.close()

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = EmployeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SupplierManagement(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CategoryManagement(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ProductManagement(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CustomerBilling(self.new_win)

    def logout(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?")
        if confirm:
            self.root.destroy()
            os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
