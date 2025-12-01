from PyQt6.QtWidgets import *
from gui_p2 import *
import csv

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






