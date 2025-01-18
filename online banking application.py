
from tkinter import *
from tkinter import Tk, Frame, Entry, Button, Label, StringVar, messagebox, Toplevel, ttk
import sqlite3
import random
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

ARIAL = ("arial",10,"bold")

class Bank:
        def __init__(self,root):
            self.conn = sqlite3.connect("atm_databse.db", timeout=100)
            self.login = False
            self.root = root
            self.header = Label(self.root,text="Online Banking Application",bg="#50A8B0",fg="white",font=("arial",35,"bold"))
            self.header.pack(fill=X)
            self.frame = Frame(self.root,bg="#728B8E",width=600,height=400)


            #Login Page Form Components
            self.userlabel =Label(self.frame,text="Account Number",bg="#728B8E",fg="white",font=ARIAL)
            self.uentry = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
               highlightthickness=2,
                highlightbackground="white")

            self.plabel = Label(self.frame, text="Password",bg="#728B8E",fg="white",font=ARIAL)
            self.pentry = Entry(self.frame,bg="honeydew",show="*",highlightcolor="#50A8B0",
               highlightthickness=2,
                highlightbackground="white")

            self.button = Button(self.frame,text="LOGIN",bg="#50A8B0",fg="white",font=ARIAL,command=self.verify)
            self.q = Button(self.frame,text="Quit",bg="#50A8B0",fg="white",font=ARIAL,command = self.root.destroy)
            self.open_new_account_button = Button(self.frame, text="Open New Account", bg="#50A8B0", fg="white",font=ARIAL, command=self.open_new_account)

            self.userlabel.place(x=145,y=100,width=120,height=20)
            self.uentry.place(x=153,y=130,width=200,height=20)

            self.plabel.place(x=125,y=160,width=120,height=20)
            self.pentry.place(x=153,y=190,width=200,height=20)

            self.button.place(x=155,y=230,width=120,height=20)
            self.q.place(x=340,y=360,width=120,height=20)

            self.open_new_account_button.place(x=150, y=360, width=180, height=20)

            self.frame.pack()


        def database_fetch(self):#Fetching Account data from database
            self.acc_list = []
            self.temp = self.conn.execute("select name,pass,acc_no,acc_type,bal from atm where acc_no = ? ",(self.ac,))
            for i in self.temp:
                self.acc_list.append("Name = {}".format(i[0]))
                self.acc_list.append("Account no = {}".format(i[2]))
                self.acc_list.append("Account type = {}".format(i[3]))
                self.ac = i[2]
                self.acc_list.append("Balance = {}".format(i[4]))


        # New Account Form Components
        def open_new_account(self):
            self.frame.destroy()
            self.frame = Frame(self.root, bg="#728B8E", width=600, height=400)

            #name
            self.name_label = Label(self.frame, text="Name", bg="#728B8E", fg="white", font=ARIAL)
            self.name_entry = Entry(self.frame, bg="honeydew", highlightcolor="#50A8B0", highlightthickness=2,
                                    highlightbackground="white")


            # Account Type selection using Listbox
            self.acc_type_label = Label(self.frame, text="Account Type", bg="#728B8E", fg="white", font=ARIAL)
            self.acc_type_list = ["Savings", "Current", "Fixed Deposit"]
            self.acc_type_var = StringVar(self.frame)
            self.acc_type_var.set(self.acc_type_list[0])  # Default selection
            self.acc_type_entry = OptionMenu(self.frame, self.acc_type_var, *self.acc_type_list)



            #Password
            self.password_label = Label(self.frame, text="Password", bg="#728B8E", fg="white", font=ARIAL)
            self.password_entry = Entry(self.frame, bg="honeydew", show="*", highlightcolor="#50A8B0",
                                         highlightthickness=2,
                                         highlightbackground="white")

            # Opening Balance
            self.balance_label = Label(self.frame, text="Balance", bg="#728B8E", fg="white", font=ARIAL)
            self.balance_entry = Entry(self.frame, bg="honeydew", highlightcolor="#50A8B0", highlightthickness=2,
                                       highlightbackground="white")


            # action buttons
            self.open_account_button = Button(self.frame, text="Open Account", bg="#50A8B0", fg="white", font=ARIAL,command=self.create_account)
            self.back_button = Button(self.frame, text="Back to Login", bg="#50A8B0", fg="white", font=ARIAL,
                                      command=self.show_login)


           # Place New Account Form Components
            self.name_label.place(x=110, y=50, width=120, height=20)
            self.name_entry.place(x=153, y=80, width=200, height=20)

            self.acc_type_label.place(x=135, y=110, width=120, height=20)
            self.acc_type_entry.place(x=153, y=140, width=200, height=20)


            self.password_label.place(x=125, y=180, width=120, height=20)
            self.password_entry.place(x=153, y=210, width=200, height=20)

            self.balance_label.place(x=120, y=255, width=120, height=20)
            self.balance_entry.place(x=153, y=280, width=200, height=20)

            self.open_account_button.place(x=155, y=360, width=120, height=20)
            self.back_button.place(x=290, y=360, width=120, height=20)

            self.frame.pack()


        def create_account(self):
            name = self.name_entry.get()
            acc_type = self.acc_type_var.get()
            password = self.password_entry.get()
            balance = self.balance_entry.get()

            # Check if the opening balance is not negative
            if float(balance) < 0:
                messagebox.showerror("Error", "Opening balance cannot be negative.")
                return

            # Generate a random 6-digit number
            random_digits = str(random.randint(100000, 999999))

            # Generate the account number based on the specified format
            if acc_type == "Savings":
                acc_type_code = "1001"
            elif acc_type == "Current":
                acc_type_code = "2002"
            elif acc_type == "Fixed Deposit":
                acc_type_code = "3003"
            else:
                messagebox.showerror("Error", "Invalid account type")
                return

            # Combine the account type code and random digits to create the account number
            acc_no = acc_type_code + random_digits

            # Check if the generated account number already exists in the database
            while self.acc_no_exists(acc_no):
                random_digits = str(random.randint(100000, 999999))
                acc_no = acc_type_code + random_digits

            # Insert the new account details into the database
            self.conn.execute("INSERT INTO atm (name, acc_no, acc_type, bal, pass) VALUES (?, ?, ?, ?, ?)",
                               (name, acc_no, acc_type, balance, password))
            self.conn.commit()

            # Show message box with account creation information
            message = f"Your account has been created.\nAccount No. is {acc_no}\nEnjoy Banking with us."
            messagebox.showinfo("Account Created", message)

            # record for passbook
            # Record the transaction
            self.conn.execute("INSERT INTO transactions (acc_no, txn_type, amount, Bal_) VALUES (?, ?, ?, ?)",
                          (acc_no, 'Inital Deposit', balance, balance))
            self.conn.commit()

            # Redirect to the login page
            self.show_login()

        def acc_no_exists(self, acc_no):
            # Check if the account number already exists in the database
            cursor = self.conn.execute("SELECT COUNT(*) FROM atm WHERE acc_no=?", (acc_no,))
            count = cursor.fetchone()[0]
            return count > 0

        def show_login(self):
            self.frame.destroy()
            self.__init__(self.root)

        def verify(self):#verifying of authorised user
            ac = False
            self.temp = self.conn.execute("select name,pass,acc_no,acc_type,bal from atm where acc_no = ? ", (int(self.uentry.get()),))
            for i in self.temp:
                self.ac = i[2]
                if i[2] == self.uentry.get():
                    ac = True
                elif i[1] == self.pentry.get():
                    ac = True
                    m = "{} Login SucessFull".format(i[0])
                    self.database_fetch()
                    messagebox._show("Login Info", m)
                    self.frame.destroy()
                    self.MainMenu()
                else:
                    ac = True
                    m = " Login UnSucessFull ! Wrong Password"
                    messagebox._show("Login Info!", m)

            if not ac:
                m = " Wrong Acoount Number !"
                messagebox._show("Login Info!", m)


        def MainMenu(self):#Main App Appears after logined !
            self.frame = Frame(self.root,bg="#728B8E",width=800,height=400)
            root.geometry("800x400")
            self.detail = Button(self.frame,text="Account Details",bg="#50A8B0",fg="white",font=ARIAL,command=self.account_detail)
            self.enquiry = Button(self.frame, text="Balance Enquiry",bg="#50A8B0",fg="white",font=ARIAL,command= self.Balance)
            self.deposit = Button(self.frame, text="Deposit Money",bg="#50A8B0",fg="white",font=ARIAL,command=self.deposit_money)
            self.withdrawl = Button(self.frame, text="Withdrawl Money",bg="#50A8B0",fg="white",font=ARIAL,command=self.withdrawl_money)
            self.q = Button(self.frame, text="Quit", bg="#50A8B0", fg="white", font=ARIAL, command=self.root.destroy)
            self.passbook_button = Button(self.frame, text="View Passbook", bg="#50A8B0", fg="white", font=ARIAL, command=self.passbook_statement)


            self.detail.place(x=0,y=0,width=200,height=50)
            self.enquiry.place(x=0, y=315, width=200, height=50)
            self.deposit.place(x=600, y=0, width=200, height=50)
            self.withdrawl.place(x=600, y=315, width=200, height=50)
            self.q.place(x=340, y=340, width=120, height=20)
            self.passbook_button.place(x=341, y=300, width=120, height=20)
            self.frame.pack()

        def account_detail(self):
            self.database_fetch()
            text = self.acc_list[0]+"\n"+self.acc_list[1]+"\n"+self.acc_list[2]
            self.label = Label(self.frame,text=text,font=ARIAL)
            self.label.place(x=200,y=100,width=300,height=100)

        def Balance(self):
            self.database_fetch()
            self.label = Label(self.frame, text=self.acc_list[3],font=ARIAL)
            self.label.place(x=200, y=100, width=300, height=100)

        def deposit_money(self):
            self.money_box = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
               highlightthickness=2,
                highlightbackground="white")
            self.submitButton = Button(self.frame,text="Submit",bg="#50A8B0",fg="white",font=ARIAL, command=self.deposit_trans)

            self.money_box.place(x=200,y=100,width=200,height=20)
            self.submitButton.place(x=445,y=100,width=55,height=20)


        def deposit_trans(self):
            # Check if the deposit amount is not negative
            deposit = float(self.money_box.get())
            if deposit < 0:
                messagebox.showerror("Error", "Deposit cannot be negative.")
                return

            self.label = Label(self.frame, text="Transaction Completed !", font=ARIAL)
            self.label.place(x=200, y=100, width=300, height=100)

            # Update balance in the database
            self.conn.execute("update atm set bal = bal + ? where acc_no = ?",(self.money_box.get(),self.ac))
            self.conn.commit()

             # Record the transaction
            self.conn.execute("INSERT INTO transactions (acc_no, txn_type, amount, Bal_) VALUES (?, ?, ?, ?)",
                          (self.ac, 'Deposit', deposit, self.get_current_balance()))
            self.conn.commit()

        def withdrawl_money(self):
            self.money_box = Entry(self.frame,bg="honeydew",highlightcolor="#50A8B0",
               highlightthickness=2,
                highlightbackground="white")
            self.submitButton = Button(self.frame,text="Submit",bg="#50A8B0",fg="white",font=ARIAL, command=self.withdrawl_trans)

            self.money_box.place(x=200,y=100,width=200,height=20)
            self.submitButton.place(x=445,y=100,width=55,height=20)

        def withdrawl_trans(self):

            withdraw = float(self.money_box.get())
            if withdraw < 0:
                messagebox.showerror("Error", "withdrwal cannot be negative.")
                return


            withdrawal_amount = float(self.money_box.get())
            if withdrawal_amount > self.get_current_balance():
                messagebox.showerror("Error", "Insufficient funds")
            else:
                self.label = Label(self.frame, text="Money Withdrawal Successful!", font=ARIAL)
                self.label.place(x=200, y=100, width=300, height=100)
                self.conn.execute("UPDATE atm SET bal = bal - ? WHERE acc_no = ?", (withdrawal_amount, self.ac))
                self.conn.commit()

                # Record the transaction
                self.conn.execute("INSERT INTO transactions (acc_no, txn_type, amount, Bal_) VALUES (?, ?, ?, ?)",
                          (self.ac, 'Withdrawal', withdraw, self.get_current_balance()))
                self.conn.commit()

        def get_current_balance(self):
            # Retrieve current balance from the database
            cursor = self.conn.execute("SELECT bal FROM atm WHERE acc_no = ?", (self.ac,))
            current_balance = cursor.fetchone()[0]
            return current_balance

        def passbook_statement(self):
            # Fetch transactions for the current user using the logged-in account number
            cursor = self.conn.execute("SELECT name, acc_no, acc_type FROM atm WHERE acc_no = ?", (self.ac,))
            account_info = cursor.fetchone()

            # Fetch transactions
            cursor = self.conn.execute("SELECT timestamp, txn_type, amount, Bal_ FROM transactions WHERE acc_no = ? ORDER BY timestamp ASC", (self.ac,))
            transactions = cursor.fetchall()

            # Create a Toplevel window to display the passbook
            passbook_window = Toplevel(self.root)
            passbook_window.title("Passbook Statement")

            # Create a Treeview widget for the passbook
            passbook_tree = ttk.Treeview(passbook_window, columns=["Date and Time", "Txn Type", "Amount", "Balance"], show="headings")

            # Set column headings
            for col in ["Date and Time", "Txn Type", "Amount", "Balance"]:
                passbook_tree.heading(col, text=col)

            # Insert transaction data into the Treeview
            for txn in transactions:
                passbook_tree.insert("", "end", values=txn)

            # Add a scrollbar to the Treeview
            scrollbar = ttk.Scrollbar(passbook_window, orient="vertical", command=passbook_tree.yview)
            passbook_tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # Pack the Treeview to make it visible
            passbook_tree.pack(fill="both", expand=True)

            # Function to generate PDF
            def generate_pdf():
                styles = getSampleStyleSheet()
                pdf_filename = "{}.pdf".format(account_info[1])
                doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
                elements = []

                # Add account info to PDF
                elements.append(Paragraph("Account Holder Name: " + account_info[0], styles['Normal']))
                elements.append(Paragraph("Account Number: " + str(account_info[1]), styles['Normal']))
                elements.append(Paragraph("Account Type: " + account_info[2], styles['Normal']))

                # Add a spacer for space after Account Type
                elements.append(Spacer(1, 12))  # Adjust the height as needed


                # Add transactions to PDF as a table
                data = [["Date and Time", "Txn Type", "Amount", "Balance"]]
                for txn in transactions:
                    data.append(list(txn))
                t = Table(data)
                t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
                elements.append(t)

                # Generate PDF
                doc.build(elements)
                messagebox.showinfo("Download Complete", "Passbook PDF downloaded successfully!")

            # Add a button to close the passbook window and return to the main menu
            close_button = Button(passbook_window, text="Close Passbook", bg="#50A8B0", fg="white", font=ARIAL, command=passbook_window.destroy)
            close_button.pack(pady=10)

            # Add a button to download passbook as PDF
            download_button = Button(passbook_window, text="Download Passbook", bg="#50A8B0", fg="white", font=ARIAL, command=generate_pdf)
            download_button.pack(pady=5)

root = Tk()
root.title("Sign In")
root.geometry("600x420")
obj = Bank(root)
root.mainloop()