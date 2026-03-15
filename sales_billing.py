# sales_billing.py - Customer Billing System

import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
import csv
from datetime import datetime
from fpdf import FPDF

class CustomerBilling:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Billing System")
        self.root.geometry("1000x600")

        # Database Connection
        self.conn = sqlite3.connect("ims.db")
        self.cursor = self.conn.cursor()

        self.cart = []
        self.total_bill = 0.0

        # Widgets
        Label(self.root, text="Customer Name:").place(x=20, y=20)
        self.customer_name = Entry(self.root)
        self.customer_name.place(x=150, y=20)

        Label(self.root, text="Search Product:").place(x=20, y=60)
        self.search_var = StringVar()
        self.search_entry = Entry(self.root, textvariable=self.search_var)
        self.search_entry.place(x=150, y=60)
        self.search_entry.bind("<KeyRelease>", self.filter_products)

        Label(self.root, text="Select Product:").place(x=20, y=100)
        self.product_combo = ttk.Combobox(self.root, state="readonly")
        self.product_combo.place(x=150, y=100)

        Label(self.root, text="Quantity:").place(x=20, y=140)
        self.quantity_entry = Entry(self.root)
        self.quantity_entry.place(x=150, y=140)

        Label(self.root, text="Discount (%):").place(x=20, y=180)
        self.discount_entry = Entry(self.root)
        self.discount_entry.place(x=150, y=180)

        Button(self.root, text="Add to Bill", command=self.add_to_bill).place(x=150, y=220)

        self.bill_area = Text(self.root, width=70, height=20)
        self.bill_area.place(x=350, y=20)

        Button(self.root, text="Save Bill", bg="green", fg="white", command=self.save_bill).place(x=150, y=500)
        Button(self.root, text="Export CSV", bg="orange", fg="black", command=self.export_csv).place(x=250, y=500)
        Button(self.root, text="Export PDF", bg="blue", fg="white", command=self.export_pdf).place(x=350, y=500)

        self.load_products()

    def load_products(self):
        self.cursor.execute("SELECT name FROM products")
        self.products = [row[0] for row in self.cursor.fetchall()]
        self.product_combo['values'] = self.products

    def filter_products(self, event):
        search_term = self.search_var.get().lower()
        filtered = [p for p in self.products if search_term in p.lower()]
        self.product_combo['values'] = filtered

    def add_to_bill(self):
        product = self.product_combo.get()
        qty = self.quantity_entry.get()
        discount = self.discount_entry.get()

        if not product or not qty.isdigit():
            messagebox.showerror("Error", "Please select a product and enter valid quantity")
            return

        qty = int(qty)
        discount = float(discount) if discount.replace('.', '', 1).isdigit() else 0.0

        self.cursor.execute("SELECT price FROM products WHERE name=?", (product,))
        result = self.cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Product not found")
            return

        price = result[0]
        total = price * qty
        discount_amount = total * (discount / 100)
        final_total = total - discount_amount

        self.cart.append((product, qty, price, discount, final_total))
        self.total_bill += final_total

        self.bill_area.insert(END, f"{product} - Qty: {qty} x Rs.{price} - {discount}% Off = Rs.{final_total:.2f}\n")
        self.bill_area.insert(END, f"Total: Rs.{self.total_bill:.2f}\n\n")

    def save_bill(self):
        if not self.customer_name.get():
            messagebox.showerror("Error", "Enter customer name")
            return

        if not self.cart:
            messagebox.showerror("Error", "Cart is empty")
            return

        invoice_no = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"
        date = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute("INSERT INTO invoices (invoice_no, customer_name, total_amount, date) VALUES (?, ?, ?, ?)",
                            (invoice_no, self.customer_name.get(), self.total_bill, date))

        for item in self.cart:
            self.cursor.execute("INSERT INTO bill_items (invoice_no, product, quantity, price, discount, tax, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (invoice_no, item[0], item[1], item[2], item[3], 0, item[4]))

        self.conn.commit()
        self.generated_invoice_no = invoice_no
        messagebox.showinfo("Success", f"Bill saved with Invoice No: {invoice_no}")

    def export_csv(self):
        if not hasattr(self, 'generated_invoice_no'):
            messagebox.showerror("Error", "Save bill first before exporting")
            return

        self.cursor.execute("SELECT * FROM bill_items WHERE invoice_no=?", (self.generated_invoice_no,))
        items = self.cursor.fetchall()

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
                                                 initialfile=f"Invoice_{self.generated_invoice_no}.csv")
        if not file_path:
            return

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Product", "Quantity", "Price", "Discount (%)", "Total"])
            for item in items:
                writer.writerow([item[2], item[3], item[4], item[5], item[7]])

        messagebox.showinfo("Success", f"Invoice exported as CSV: {file_path}")

    def export_pdf(self):
        if not hasattr(self, 'generated_invoice_no'):
            messagebox.showerror("Error", "Save bill first before exporting")
            return

        self.cursor.execute("SELECT * FROM bill_items WHERE invoice_no=?", (self.generated_invoice_no,))
        items = self.cursor.fetchall()

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
                                                 initialfile=f"Invoice_{self.generated_invoice_no}.pdf")
        if not file_path:
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Invoice", ln=True, align="C")

        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, f"Invoice No: {self.generated_invoice_no}", ln=True)
        pdf.cell(200, 10, f"Customer Name: {self.customer_name.get()}", ln=True)
        pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 10, "Product")
        pdf.cell(30, 10, "Qty")
        pdf.cell(30, 10, "Price")
        pdf.cell(30, 10, "Discount")
        pdf.cell(30, 10, "Total", ln=True)

        pdf.set_font("Arial", '', 12)
        for item in items:
            pdf.cell(40, 10, item[2])
            pdf.cell(30, 10, str(item[3]))
            pdf.cell(30, 10, str(item[4]))
            pdf.cell(30, 10, str(item[5]))
            pdf.cell(30, 10, str(item[7]), ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"Total Bill Amount: Rs.{self.total_bill:.2f}", ln=True)

        pdf.output(file_path)
        messagebox.showinfo("Success", f"Invoice exported as PDF: {file_path}")

if __name__ == "__main__":
    root = Tk()
    app = CustomerBilling(root)
    root.mainloop()
