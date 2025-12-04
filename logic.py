from PyQt6.QtWidgets import *
from bankdetailsgui import *
from launchscreengui import *
from accountcreationgui import *
import csv

user_info = {}

class Launch(QMainWindow, Ui_LaunchWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.create_account = CreateAccount()
        self.details = Details()

        self.signin_button.clicked.connect(lambda: self.signin())
        self.createaccount_button.clicked.connect(lambda: self.create_account_window())

    def signin(self) -> None:
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            if user_info[username]['password'] == password:
                self.error_label.setText("You are logged in!")
                self.details.set_user(username) # Communicates to details window which user is logged in
                self.details.show()

            elif user_info[username] != password:
                raise ValueError

        except KeyError:
            self.error_label.setText("No such user!")

        except ValueError:
            self.error_label.setText("Incorrect Password!")

    def create_account_window(self) -> None:
        self.create_account.show()


class CreateAccount(QMainWindow, Ui_AccountCreationWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.create_account_button.clicked.connect(lambda: self.create_account())

    def create_account(self):

        username = self.username_input.text()
        password = self.password_input.text()
        password_confirm = self.password_confirm_input.text()

        try:
            if password != password_confirm:
                raise TypeError

            user_info[username] = { # Sets user account details properly
                'password': password,
                'checking': Account('Checking', 0),
                'savings': Account('Savings', 0)
            }

            self.error_label.setText("Account created!")
            print(user_info)
        except TypeError:
            self.password_input.clear()
            self.password_confirm_input.clear()
            self.error_label.setText("Passwords do not match!")


class Details(QMainWindow, Ui_BankDetailsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.user = None  # stores username
        self.accounts = None  # stores account data in user's dict

        self.checking_option_confirm.clicked.connect(lambda: self.confirm('checking'))
        self.savings_option_confirm.clicked.connect(lambda: self.confirm('savings'))

    def set_user(self, username):
        """Load's correct details for the logged-in user"""
        self.user = username
        self.accounts = user_info[username]
        self.checking_balance_label.setText(f"{self.accounts['checking'].get_balance():.2f}") # Sets checking balance on log in
        self.savings_balance_label.setText(f"{self.accounts['savings'].get_balance():.2f}") # Sets savings balance on login

    def confirm(self, account_type):
        """Deposits/Withdraws to/from account_type"""
        account = self.accounts[account_type] # initializes the object (account) from the dict info

        if account_type == 'checking':
            balance_label = self.checking_balance_label
            amount_input = self.checking_amount_input
            option_select = self.checking_option_select
            error_label = self.checking_error_label

        elif account_type == 'savings':
            balance_label = self.savings_balance_label
            amount_input = self.savings_amount_input
            option_select = self.savings_option_select
            error_label = self.savings_error_label

        try:
            amount = float(amount_input.text())
            if amount <= 0:
                raise ValueError

        except ValueError:
            error_label.setText("Please enter a positive number.")
            amount_input.clear()

        option = option_select.currentText()

        if option == 'Deposit':
            account.deposit(amount)
            balance_label.setText(f"{account.get_balance():.2f}")
            error_label.setText("")


        elif option == 'Withdraw':
            if account.withdraw(amount):
                balance_label.setText(f"{account.get_balance():.2f}")
            else:
                error_label.setText("Insufficient funds. Please deposit money or withdraw a smaller amount.")


class Account:
    def __init__(self, name: object, balance: object = 0) -> None:
        self.__name = name
        self.set_balance(balance)

    def deposit(self, amount) -> bool:
        """Deposits amount"""
        if amount <= 0:
            return False
        else:
            self.__balance += amount
            return True

    def withdraw(self, amount):
        if amount <= 0 or amount > self.__balance:
           return False
        else:
           self.__balance -= amount
           return True

    def get_balance(self):
        return self.__balance

    def get_name(self):
        return self.__name

    def set_balance(self, value):
        if value < 0:
            self.__balance = 0
        else:
            self.__balance = value

    def set_name(self, value):
        self.__name = value

    def __str__(self):
        return f'Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}'

