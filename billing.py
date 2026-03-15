import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

from create_db import bill_table


def fetch_products():
    conn = sqlite3.connect("ims.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products")
    products = cursor.fetchall()
    conn.close()
    return {p[0]: p[1] for p in products}


def update_price(event):
    selected_product = combo_product.get()
    if selected_product in product_prices:
        entry_price.delete(0, tk.END)
        entry_price.insert(0, product_prices[selected_product])


def generate_bill():
    customer = entry_customer.get()
    product = combo_product.get()
    quantity = int(entry_quantity.get())
    price = float(entry_price.get())
    discount = float(entry_discount.get())
    tax = float(entry_tax.get())
    total = (quantity * price) * ((100 - discount) / 100) * ((100 + tax) / 100)

    conn = sqlite3.connect("ims.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bills (customer_name, product, quantity, price, discount, tax, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (customer, product, quantity, price, discount, tax, total))
    conn.commit()
    conn.close()

    text_bill.delete("1.0", tk.END)
    text_bill.insert(tk.END, f"Customer: {customer}\n")
    text_bill.insert(tk.END, f"Product: {product}\n")
    text_bill.insert(tk.END, f"Quantity: {quantity}\n")
    text_bill.insert(tk.END, f"Price: {price}\n")
    text_bill.insert(tk.END, f"Discount: {discount}%\n")
    text_bill.insert(tk.END, f"Tax: {tax}%\n")
    text_bill.insert(tk.END, f"Total: {total}\n")
    messagebox.showinfo("Success", "Bill generated successfully!")


root = tk.Tk()
root.title("Billing System")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

frame_bill = tk.Frame(root)
frame_bill.pack(pady=10)

tk.Label(frame_input, text="Customer Name:").grid(row=0, column=0)
tk.Label(frame_input, text="Product:").grid(row=1, column=0)
tk.Label(frame_input, text="Quantity:").grid(row=2, column=0)
tk.Label(frame_input, text="Price per Unit:").grid(row=3, column=0)
tk.Label(frame_input, text="Discount (%):").grid(row=4, column=0)
tk.Label(frame_input, text="Tax (%):").grid(row=5, column=0)

entry_customer = tk.Entry(frame_input)
entry_quantity = tk.Entry(frame_input)
entry_price = tk.Entry(frame_input)
entry_discount = tk.Entry(frame_input)
entry_tax = tk.Entry(frame_input)

entry_customer.grid(row=0, column=1)
entry_quantity.grid(row=2, column=1)
entry_price.grid(row=3, column=1)
entry_discount.grid(row=4, column=1)
entry_tax.grid(row=5, column=1)

product_prices = fetch_products()
combo_product = ttk.Combobox(frame_input, values=list(product_prices.keys()))
combo_product.grid(row=1, column=1)
combo_product.bind("<<ComboboxSelected>>", update_price)

tk.Button(frame_input, text="Generate Bill", command=generate_bill).grid(row=6, column=0, columnspan=2)

text_bill = tk.Text(frame_bill, height=10, width=40)
text_bill.pack()

bill_table()
root.mainloop()
