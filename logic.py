from PyQt6.QtWidgets import *
from bankdetailsgui import *
from launchscreengui import *
from accountcreationgui import *
import csv

user_info = {'cschappert' : '1234'}

class Launch(QMainWindow, Ui_LaunchWindow):
    def __init__(self):
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
            if user_info[username] == password:
                self.error_label.setText("You are logged in!")
                self.details.show()
            elif user_info[username] != password:
                raise ValueError

        except KeyError:
            self.error_label.setText("No such user!")

        except ValueError:
            self.error_label.setText("Incorrect Password!")

    def create_account_window(self):
        self.create_account.show()


class CreateAccount(QMainWindow, Ui_AccountCreationWindow):
    def __init__(self):
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

            user_info[username] = password
            self.error_label.setText("Account created!")

        except TypeError:
            self.password_input.clear()
            self.password_confirm_input.clear()
            self.error_label.setText("Passwords do not match!")

        except ValueError:
            pass

class Details(QMainWindow, Ui_BankDetailsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.checking_option_confirm.clicked.connect(lambda: self.checking_action())
        self.savings_option_confirm.clicked.connect(lambda: self.savings_action())

    def checking_action(self):
        self.checking_balance = float(self.checking_balance_label.text())
        self.checking_input = float(self.checking_amount_input.text())

        self.checking_option = self.checking_option_select.currentText()

        if self.checking_option == 'Deposit':
            self.checking_error_label.setText("")
            self.checking_balance += self.checking_input
            self.checking_balance_label.setText(self.checking_balance)

        elif self.checking_option == 'Withdraw':
            try:
                self.checking_balance = self.checking_balance_label.text()
                self.checking_balance -= self.checking_input

                if self.checking_balance < 0:
                    raise ValueError
                else:
                    self.checking_balance_label.setText(f"{self.checking_balance:.2f}")

            except ValueError:
                self.checking_error_label.setText("Insufficient funds. Please deposit money or withdraw a smaller amount.")

    def savings_action(self):
        self.savings_balance = float(self.savings_balance_label.text())
        self.savings_input = float(self.savings_amount_input.text())

        self.savings_option = self.savings_option_select.currentText()




class Account:
    def __init__(self, name, balance=0):
        self.__name = name
        self.set_balance(balance)

    def deposit(self, amount):
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

class SavingAccount(Account):
    MINIMUM = 100
    RATE = 0.02

    def __init__(self, name):
        super().__init__(name, self.MINIMUM)
        self.__deposit_count = 0

    def apply_interest(self):
        if self.__deposit_count % 5 == 0 and self.__deposit_count != 0:
            updated_balance = self.get_balance() + (self.get_balance() * self.RATE)
            self.set_balance(updated_balance)

    def deposit(self, amount):
        if amount <= 0:
            return False
        if super().deposit(amount):
            self.__deposit_count += 1
            self.apply_interest()
        return True

    def withdraw(self, amount):
        x = self.get_balance() - amount
        if amount <= 0 or x < self.MINIMUM:
            return False
        return super().withdraw(amount)

    def set_balance(self, value):
        if value < self.MINIMUM:
            super().set_balance(self.MINIMUM)
        else:
            super().set_balance(value)

    def __str__(self):
        return f'SAVING ACCOUNT: {super().__str__()}'






