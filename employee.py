from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import bcrypt

class EmployeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title(" Smart Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_email = StringVar()
        self.var_name = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        searchFrame = LabelFrame(self.root, text="Search User", bg="white",
                                 font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE)
        searchFrame.place(x=250, y=20, width=600, height=70)

        cmg_search = ttk.Combobox(searchFrame, textvariable=self.var_searchby,
                                  values=("Select", "E_mail", "Contact", "Name"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmg_search.place(x=10, y=10, width=180)
        cmg_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=200, y=10)
        btn_search = Button(searchFrame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50",
                            fg="white")
        btn_search.place(x=410, y=9, width=150, height=30)

        title = Label(self.root, text="User Details", font=("goudy old style", 15),
                      bg="#0f4d7d", fg="white")
        title.place(x=50, y=100, width=1000)

        Label(self.root, text="Emp ID", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15), bg="lightgray").place(x=150, y=150,
                                                                                                           width=180)

        Label(self.root, text="Gender", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender,
                                  values=("Select", "Male", "Female", "Other"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)

        Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=750, y=150)
        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=850, y=150, width=180)

        Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=190, width=180)

        Label(self.root, text="D.O.B", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow").place(x=500, y=190, width=180)

        Label(self.root, text="D.O.J", font=("goudy old style", 15), bg="white").place(x=750, y=190)
        Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow").place(x=850, y=190, width=180)

        Label(self.root, text="E-mail", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=230, width=180)

        Label(self.root, text="Password", font=("goudy old style", 15), bg="white").place(x=350, y=230)
        Entry(self.root, textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow").place(x=500, y=230, width=180)

        Label(self.root, text="User Type", font=("goudy old style", 15), bg="white").place(x=750, y=230)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Staff"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)

        Label(self.root, text="Address", font=("goudy old style", 15), bg="white").place(x=50, y=270)
        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)

        Label(self.root, text="Salary", font=("goudy old style", 15), bg="white").place(x=500, y=270)
        Entry(self.root, textvariable=self.var_salary, font=("goudy old style", 15), bg="lightyellow").place(x=600, y=270, width=180)

        Button(self.root, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196F3",
               fg="white", cursor="hand2").place(x=500, y=305, width=110, height=28)
        Button(self.root, text="Update", command=self.update, font=("goudy old style", 15), bg="#FFC107",
               fg="white", cursor="hand2").place(x=620, y=305, width=110, height=28)
        Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#F44336",
               fg="white", cursor="hand2").place(x=740, y=305, width=110, height=28)
        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#9C27B0",
               fg="white", cursor="hand2").place(x=860, y=305, width=110, height=28)

        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=(
            "E_id", "Name", "E_mail", "Gender", "Contact", "DOB", "DOJ", "Password", "UType", "Address", "Salary"),
            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.config(command=self.EmployeeTable.yview)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        for col in ("E_id", "Name", "E_mail", "Gender", "Contact", "DOB", "DOJ", "Password", "UType", "Address", "Salary"):
            self.EmployeeTable.heading(col, text=col)
            self.EmployeeTable.column(col, width=100)
        self.EmployeeTable["show"] = "headings"
        self.show()

    def generate_emp_id(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT MAX(E_id) FROM employee")  # Get the highest Employee ID
            last_id = cur.fetchone()[0]
            if last_id:
                new_id = int(last_id) + 1  # Increment the last ID
            else:
                new_id = 1001  # Default start ID
            return str(new_id)
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating Employee ID: {str(ex)}", parent=self.root)
            return "1001"  # Fallback value
        finally:
            con.close()

    def add(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "" or self.var_email.get() == "":
                messagebox.showerror("Error", "Name and Email are required", parent=self.root)
            else:
                self.var_emp_id.set(self.generate_emp_id())  # Auto-generate Employee ID
                cur.execute("SELECT * FROM employee WHERE E_mail=?", (self.var_email.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Email already exists", parent=self.root)
                else:
                    hashed_password = bcrypt.hashpw(self.var_pass.get().encode(), bcrypt.gensalt()).decode()
                    cur.execute(
                        "INSERT INTO employee (E_id, Name, E_mail, Gender, Contact, DOB, DOJ, Password, UType, Address, Salary) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            self.var_emp_id.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            hashed_password,
                            self.var_utype.get(),
                            self.txt_address.get("1.0", END),
                            self.var_salary.get()
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", f"Employee added successfully with ID {self.var_emp_id.get()}",
                                        parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "User ID is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE E_id=?", (self.var_emp_id.get(),))
                if cur.fetchone() is None:
                    messagebox.showerror("Error", "Invalid User ID", parent=self.root)
                else:
                    hashed_password = bcrypt.hashpw(self.var_pass.get().encode(), bcrypt.gensalt()).decode()
                    cur.execute(
                        "UPDATE employee SET Name=?, E_mail=?, Gender=?, Contact=?, DOB=?, DOJ=?, Password=?, UType=?, Address=?, Salary=? WHERE E_id=?",
                        (
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            hashed_password,
                            self.var_utype.get(),
                            self.txt_address.get("1.0", END),
                            self.var_salary.get(),
                            self.var_emp_id.get()
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "User updated", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "User ID is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE E_id=?", (self.var_emp_id.get(),))
                if cur.fetchone() is None:
                    messagebox.showerror("Error", "Invalid User ID", parent=self.root)
                else:
                    confirm = messagebox.askyesno("Confirm", "Delete this User?", parent=self.root)
                    if confirm:
                        cur.execute("DELETE FROM employee WHERE E_id=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "User deleted", parent=self.root)
                        self.clear()
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete("1.0", END)
        self.var_salary.set("")


    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set("")  # Hide hashed password
        self.var_utype.set(row[8])
        self.txt_address.delete("1.0", END)
        self.txt_address.insert(END, row[9])
        self.var_salary.set(row[10])

    def search(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select a search category", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Enter search text", parent=self.root)
            else:
                query = f"SELECT * FROM employee WHERE {self.var_searchby.get()} LIKE ?"
                cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                if rows:
                    for row in rows:
                        self.EmployeeTable.insert("", END, values=row)
                else:
                    messagebox.showinfo("No Result", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)
        finally:
            con.close()
    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()
