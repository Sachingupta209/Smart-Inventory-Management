import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


# Create Database Connection



class SupplierManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Supplier Management System")
        self.root.geometry("900x500")

        # Title
        Label(self.root, text="Manage Supplier Details", font=("Arial", 16, "bold")).pack(side=TOP, fill=X)

        # Input Fields
        Label(self.root, text="Invoice No:").place(x=20, y=50)
        self.invoice_no = Entry(self.root)
        self.invoice_no.place(x=150, y=50)

        Label(self.root, text="Supplier Name:").place(x=20, y=90)
        self.supplier_name = Entry(self.root)
        self.supplier_name.place(x=150, y=90)

        Label(self.root, text="Contact:").place(x=20, y=130)
        self.contact = Entry(self.root)
        self.contact.place(x=150, y=130)

        Label(self.root, text="Description:").place(x=20, y=170)
        self.description = Text(self.root, height=3, width=30)
        self.description.place(x=150, y=170)

        # Buttons
        Button(self.root, text="Save", bg="blue", fg="white", command=self.save_supplier).place(x=50, y=250)
        Button(self.root, text="Update", bg="green", fg="white", command=self.update_supplier).place(x=120, y=250)
        Button(self.root, text="Delete", bg="red", fg="white", command=self.delete_supplier).place(x=200, y=250)
        Button(self.root, text="Clear", bg="gray", fg="white", command=self.clear_fields).place(x=270, y=250)

        # Search Bar
        Label(self.root, text="Invoice No:").place(x=500, y=50)
        self.search_txt = Entry(self.root)
        self.search_txt.place(x=600, y=50)
        Button(self.root, text="Search", command=self.search_supplier).place(x=750, y=48)

        # Supplier Table with Scrollbar
        frame = Frame(self.root)
        frame.place(x=400, y=100, width=480, height=300)

        scroll_y = Scrollbar(frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.supplier_table = ttk.Treeview(frame, columns=("id", "invoice", "name", "contact", "desc"),
                                           show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.supplier_table.yview)

        self.supplier_table.pack(fill=BOTH, expand=1)

        self.supplier_table.heading("id", text="Sup ID")
        self.supplier_table.heading("invoice", text="Invoice No")
        self.supplier_table.heading("name", text="Name")
        self.supplier_table.heading("contact", text="Contact")
        self.supplier_table.heading("desc", text="Description")

        self.supplier_table.column("id", width=50)
        self.supplier_table.column("invoice", width=100)
        self.supplier_table.column("name", width=100)
        self.supplier_table.column("contact", width=100)
        self.supplier_table.column("desc", width=150)

        self.supplier_table.bind("<ButtonRelease-1>", self.get_selected_row)
        self.fetch_suppliers()

    # Validate Fields
    def generate_supplier_id(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT MAX(Sup_ID) FROM supplier")  # Get the highest Sup_ID
            last_id = cur.fetchone()[0]
            if last_id:  # If there's an existing ID, increment it
                new_id = last_id + 1
            else:  # If no ID exists, start from 1
                new_id = 1
            return new_id
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating Supplier ID: {str(ex)}", parent=self.root)
            return 1  # Default fallback
        finally:
            con.close()

    def validate_fields(self):
        if not self.invoice_no.get().strip() or not self.supplier_name.get().strip() or not self.contact.get().strip():
            messagebox.showerror("Error", "All fields are required")
            return False
        if not self.contact.get().isdigit():
            messagebox.showerror("Error", "Contact number should be numeric")
            return False
        return True

    # Save Supplier
    def save_supplier(self):
        if not self.validate_fields():
            return

        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            sup_id = self.generate_supplier_id()  # Get the new auto-generated Sup_ID
            cur.execute("INSERT INTO supplier (Sup_ID, Invoice_No, Name, Contact, Description) VALUES (?, ?, ?, ?, ?)",
                        (sup_id, self.invoice_no.get(), self.supplier_name.get(), self.contact.get(),
                         self.description.get("1.0", END)))
            con.commit()
            self.fetch_suppliers()
            self.clear_fields()
            messagebox.showinfo("Success", f"Supplier Added Successfully with ID {sup_id}")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Invoice number already exists")
        finally:
            con.close()

    # Fetch Data
    def fetch_suppliers(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM supplier")
        rows = cur.fetchall()
        con.close()

        self.supplier_table.delete(*self.supplier_table.get_children())
        for row in rows:
            self.supplier_table.insert("", END, values=row)

    # Get Selected Row
    def get_selected_row(self, event):
        selected = self.supplier_table.focus()
        data = self.supplier_table.item(selected)["values"]
        if data:
            self.invoice_no.delete(0, END)
            self.invoice_no.insert(0, data[1])
            self.supplier_name.delete(0, END)
            self.supplier_name.insert(0, data[2])
            self.contact.delete(0, END)
            self.contact.insert(0, data[3])
            self.description.delete("1.0", END)
            self.description.insert("1.0", data[4])

    # Update Supplier
    def update_supplier(self):
        if not self.validate_fields():
            return

        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("UPDATE supplier SET Name=?, Contact=?, Description=? WHERE Invoice_No=?",
                    (self.supplier_name.get(), self.contact.get(), self.description.get("1.0", END),
                     self.invoice_no.get()))
        con.commit()
        con.close()
        self.fetch_suppliers()
        self.clear_fields()
        messagebox.showinfo("Success", "Supplier Updated Successfully")

    # Delete Supplier with Confirmation
    def delete_supplier(self):
        if not self.invoice_no.get():
            messagebox.showerror("Error", "Please select a supplier to delete")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this supplier?")
        if confirm:
            con = sqlite3.connect("ims.db")
            cur = con.cursor()
            cur.execute("DELETE FROM supplier WHERE Invoice_No=?", (self.invoice_no.get(),))
            con.commit()
            con.close()
            self.fetch_suppliers()
            self.clear_fields()
            messagebox.showinfo("Deleted", "Supplier Deleted Successfully")

    # Search Supplier with Reset
    def search_supplier(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM supplier WHERE Invoice_No=?", (self.search_txt.get(),))
        row = cur.fetchone()
        con.close()

        self.supplier_table.delete(*self.supplier_table.get_children())
        if row:
            self.supplier_table.insert("", END, values=row)
        else:
            messagebox.showwarning("Not Found", "No Supplier Found!")
            self.fetch_suppliers()  # Reset table if no results

    # Clear Fields
    def clear_fields(self):
        self.invoice_no.delete(0, END)
        self.supplier_name.delete(0, END)
        self.contact.delete(0, END)
        self.description.delete("1.0", END)


# Link to Dashboard
def open_supplier_page():
    root = Tk()
    SupplierManagement(root)
    root.mainloop()

# To open the supplier page from the dashboard, call `open_supplier_page()`.
