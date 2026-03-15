import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

class ProductManagement:
    def __init__(self, root):
        self.root = root
        self.root.geometry("950x500+300+100")
        self.root.title("Product Management")
        self.root.config(bg="white")

        # ======= Database Connection =======
        self.conn = sqlite3.connect("ims.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # ======= Title =======
        title = Label(self.root, text="Manage Product Details", font=("goudy old style", 20, "bold"), bg="blue", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)

        # ======= Form Fields =======
        Label(self.root, text="Category", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=70)
        self.cmb_category = ttk.Combobox(self.root, font=("times new roman", 13), state="readonly", justify=CENTER)
        self.cmb_category.place(x=200, y=70, width=200)

        Label(self.root, text="Supplier", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=110)
        self.cmb_supplier = ttk.Combobox(self.root, font=("times new roman", 13), state="readonly", justify=CENTER)
        self.cmb_supplier.place(x=200, y=110, width=200)

        Label(self.root, text="Name", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=150)
        self.txt_name = Entry(self.root, font=("times new roman", 13), bg="lightyellow")
        self.txt_name.place(x=200, y=150, width=200)

        Label(self.root, text="Price", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=190)
        self.txt_price = Entry(self.root, font=("times new roman", 13), bg="lightyellow")
        self.txt_price.place(x=200, y=190, width=200)

        Label(self.root, text="QTY", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=230)
        self.txt_qty = Entry(self.root, font=("times new roman", 13), bg="lightyellow")
        self.txt_qty.place(x=200, y=230, width=200)

        Label(self.root, text="Status", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=270)
        self.cmb_status = ttk.Combobox(self.root, values=("Active", "Inactive"), font=("times new roman", 13), state="readonly", justify=CENTER)
        self.cmb_status.place(x=200, y=270, width=200)
        self.cmb_status.current(0)

        # ======= Buttons =======
        btn_save = Button(self.root, text="Save", font=("times new roman", 15, "bold"), bg="green", fg="white", command=self.save_product)
        btn_save.place(x=50, y=320, width=80, height=30)

        btn_update = Button(self.root, text="Update", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.update_product)
        btn_update.place(x=150, y=320, width=80, height=30)

        btn_delete = Button(self.root, text="Delete", font=("times new roman", 15, "bold"), bg="red", fg="white", command=self.delete_product)
        btn_delete.place(x=250, y=320, width=80, height=30)

        btn_clear = Button(self.root, text="Clear", font=("times new roman", 15, "bold"), bg="gray", fg="white", command=self.clear_fields)
        btn_clear.place(x=350, y=320, width=80, height=30)

        # ======= Table Frame with Scrollbars =======
        table_frame = Frame(self.root, bd=2, relief=RIDGE)
        table_frame.place(x=450, y=70, width=480, height=400)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.product_table = ttk.Treeview(
            table_frame,
            columns=("pid", "category", "name", "supplier", "price", "qty", "status"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.config(command=self.product_table.xview)
        scroll_y.config(command=self.product_table.yview)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("category", text="Category")
        self.product_table.heading("name", text="Product Name")
        self.product_table.heading("supplier", text="Supplier")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="QTY")
        self.product_table.heading("status", text="Status")
        self.product_table["show"] = "headings"

        self.product_table.pack(fill=BOTH, expand=1)

        self.fetch_products()
        self.load_categories_suppliers()

    # ======= Database Table Creation =======
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                pid INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                supplier TEXT,
                name TEXT,
                price REAL,
                qty INTEGER,
                status TEXT
            )
        """)
        self.conn.commit()

    # ======= Load Category & Supplier from DB =======
    def load_categories_suppliers(self):
        self.cursor.execute("SELECT name FROM category")
        categories = [row[0] for row in self.cursor.fetchall()]
        self.cmb_category["values"] = categories

        self.cursor.execute("SELECT name FROM supplier")
        suppliers = [row[0] for row in self.cursor.fetchall()]
        self.cmb_supplier["values"] = suppliers

    # ======= Save Product =======
    def save_product(self):
        if self.txt_name.get() == "" or self.txt_price.get() == "" or self.txt_qty.get() == "":
            messagebox.showerror("Error", "All fields are required")
            return

        self.cursor.execute(
            "INSERT INTO products (category, supplier, name, price, qty, status) VALUES (?, ?, ?, ?, ?, ?)",
            (
                self.cmb_category.get(),
                self.cmb_supplier.get(),
                self.txt_name.get(),
                self.txt_price.get(),
                self.txt_qty.get(),
                self.cmb_status.get(),
            ),
        )
        self.conn.commit()
        messagebox.showinfo("Success", "Product Added Successfully!")
        self.fetch_products()

    # ======= Fetch Products =======
    def fetch_products(self):
        self.cursor.execute("SELECT pid, category, name, supplier, price, qty, status FROM products")
        rows = self.cursor.fetchall()
        self.product_table.delete(*self.product_table.get_children())
        for row in rows:
            self.product_table.insert("", END, values=row)

    # ======= Update Product =======
    def update_product(self):
        selected = self.product_table.focus()
        if not selected:
            messagebox.showerror("Error", "Select a product to update")
            return

        values = self.product_table.item(selected, "values")
        pid = values[0]

        self.cursor.execute(
            "UPDATE products SET category=?, supplier=?, name=?, price=?, qty=?, status=? WHERE pid=?",
            (
                self.cmb_category.get(),
                self.cmb_supplier.get(),
                self.txt_name.get(),
                self.txt_price.get(),
                self.txt_qty.get(),
                self.cmb_status.get(),
                pid,
            ),
        )
        self.conn.commit()
        messagebox.showinfo("Success", "Product Updated!")
        self.fetch_products()

    # ======= Delete Product =======
    def delete_product(self):
        selected = self.product_table.focus()
        if not selected:
            messagebox.showerror("Error", "Select a product to delete")
            return

        pid = self.product_table.item(selected, "values")[0]
        self.cursor.execute("DELETE FROM products WHERE pid=?", (pid,))
        self.conn.commit()
        messagebox.showinfo("Success", "Product Deleted!")
        self.fetch_products()

    # ======= Clear Fields =======
    def clear_fields(self):
        self.cmb_category.set("")
        self.cmb_supplier.set("")
        self.txt_name.delete(0, END)
        self.txt_price.delete(0, END)
        self.txt_qty.delete(0, END)
        self.cmb_status.current(0)

if __name__ == "__main__":
    root = Tk()
    obj = ProductManagement(root)
    root.mainloop()
