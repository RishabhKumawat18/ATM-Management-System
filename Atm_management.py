import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class BankAccount:
    def __init__(self, account_number, pin, balance=0, transactions=None):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.transactions = transactions if transactions is not None else []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited: ${amount}")
            return f"Deposit successful! New balance: ${self.balance}"
        return "Invalid deposit amount."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrew: ${amount}")
            return f"Withdrawal successful! New balance: ${self.balance}"
        return "Invalid or insufficient funds."

    def check_balance(self):
        return f"Your current balance is: ${self.balance}"

    def view_transactions(self):
        return "\n".join(self.transactions) if self.transactions else "No transactions found."

class BankSystem:
    def __init__(self, data_file="atmaccount.json"):
        self.data_file = data_file
        self.accounts = self.load_accounts()

    def load_accounts(self):
        try:
            with open(self.data_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_accounts(self):
        with open(self.data_file, "w") as file:
            json.dump(self.accounts, file, indent=4)

    def create_account(self, account_number, pin):
        if account_number in self.accounts:
            return None, "Account number already exists."
        self.accounts[account_number] = {"pin": pin, "balance": 0, "transactions": []}
        self.save_accounts()
        return BankAccount(account_number, pin), "Account created successfully!"

    def authenticate(self, account_number, pin):
        account_data = self.accounts.get(account_number)
        if account_data and account_data["pin"] == pin:
            return BankAccount(account_number, pin, account_data["balance"], account_data["transactions"])
        return None

    def update_account(self, account):
        self.accounts[account.account_number] = {
            "pin": account.pin,
            "balance": account.balance,
            "transactions": account.transactions
        }
        self.save_accounts()

class ATMApp:
    def __init__(self, root):
        self.bank = BankSystem()
        self.account = None
        self.root = root
        self.root.title("ATM System")
        self.root.geometry("400x400")
        self.root.configure(bg="#2C3E50")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        ttk.Label(self.root, text="ATM System", font=("Arial", 16, "bold"), background="#2C3E50", foreground="white").pack(pady=10)
        ttk.Label(self.root, text="Account Number:", background="#2C3E50", foreground="white").pack()
        self.account_entry = ttk.Entry(self.root)
        self.account_entry.pack(pady=5)
        ttk.Label(self.root, text="PIN:", background="#2C3E50", foreground="white").pack()
        self.pin_entry = ttk.Entry(self.root, show="*")
        self.pin_entry.pack(pady=5)
        ttk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        ttk.Button(self.root, text="Create Account", command=self.create_account_screen).pack()

    def create_account_screen(self):
        self.clear_screen()
        ttk.Label(self.root, text="Create Account", font=("Arial", 16, "bold"), background="#2C3E50", foreground="white").pack(pady=10)
        ttk.Label(self.root, text="New Account Number:", background="#2C3E50", foreground="white").pack()
        self.new_account_entry = ttk.Entry(self.root)
        self.new_account_entry.pack(pady=5)
        ttk.Label(self.root, text="Set PIN:", background="#2C3E50", foreground="white").pack()
        self.new_pin_entry = ttk.Entry(self.root, show="*")
        self.new_pin_entry.pack(pady=5)
        ttk.Button(self.root, text="Create", command=self.create_account).pack(pady=5)
        ttk.Button(self.root, text="Back", command=self.create_login_screen).pack()

    def create_account(self):
        account_number = self.new_account_entry.get()
        pin = self.new_pin_entry.get()
        account, message = self.bank.create_account(account_number, pin)
        if account:
            messagebox.showinfo("Success", message)
            self.create_login_screen()
        else:
            messagebox.showerror("Error", message)

    def login(self):
        account_number = self.account_entry.get()
        pin = self.pin_entry.get()
        self.account = self.bank.authenticate(account_number, pin)
        if self.account:
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def create_main_screen(self):
        self.clear_screen()
        ttk.Label(self.root, text="Main Menu", font=("Arial", 16, "bold"), background="#2C3E50", foreground="white").pack(pady=10)
        ttk.Button(self.root, text="Check Balance", command=self.show_balance).pack(pady=5)
        ttk.Button(self.root, text="Deposit", command=self.deposit_screen).pack()
        ttk.Button(self.root, text="Withdraw", command=self.withdraw_screen).pack()
        ttk.Button(self.root, text="View Transactions", command=self.show_transactions).pack()
        ttk.Button(self.root, text="Logout", command=self.create_login_screen).pack(pady=5)

    def show_balance(self):
        messagebox.showinfo("Balance", self.account.check_balance())

    def deposit_screen(self):
        amount = simpledialog.askfloat("Deposit", "Enter deposit amount:")
        if amount:
            messagebox.showinfo("Deposit", self.account.deposit(amount))
            self.bank.update_account(self.account)

    def withdraw_screen(self):
        amount = simpledialog.askfloat("Withdraw", "Enter withdrawal amount:")
        if amount:
            messagebox.showinfo("Withdraw", self.account.withdraw(amount))
            self.bank.update_account(self.account)

    def show_transactions(self):
        messagebox.showinfo("Transactions", self.account.view_transactions())

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


root = tk.Tk()
app = ATMApp(root)
root.mainloop()
