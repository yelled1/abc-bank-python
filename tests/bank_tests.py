import os, sys
import datetime as D

from nose.tools import assert_equals

from abcbank.account  import Account, CHECKING, MAXI_SAVINGS, SAVINGS
from abcbank.bank     import Bank
from abcbank.customer import Customer


def test_customer_summary():
    bank = Bank()
    john = Customer("John").openAccount(Account(CHECKING))
    bank.addCustomer(john)
    assert_equals(bank.customerSummary(),
                  "Customer Summary\n - John (1 account)")


def test_checking_account():
    bank = Bank()
    checkingAccount = Account(CHECKING)
    bill = Customer("Bill").openAccount(checkingAccount)
    bank.addCustomer(bill)
    checkingAccount.deposit(100.0)
    assert_equals(bank.totalInterestPaid(), 0.1)


def test_savings_account():
    bank = Bank()
    savingsAccount = Account(SAVINGS)
    bank.addCustomer(Customer("Bill").openAccount(savingsAccount))
    savingsAccount.deposit(1500.0)
    assert_equals(bank.totalInterestPaid(), 2.0)


def test_maxi_savings_account():
    bank = Bank()
    maxiAccount = Account(MAXI_SAVINGS)
    bank.addCustomer(Customer("Bill").openAccount(maxiAccount))
    maxiAccount.deposit(3000.0)
    print(bank.totalInterestPaid())
    assert_equals(bank.totalInterestPaid(), 150.0)

def test_MaxiAcct_last10():
    bank = Bank()
    maxiAccount    = Account(MAXI_SAVINGS)
    savingsAccount = Account(SAVINGS)
    bank.addCustomer(Customer("Magnus").openAccount(maxiAccount).openAccount(savingsAccount))
    maxiAccount.deposit(100.0, D.date(2016,1,10))
    maxiAccount.deposit(100.0, D.date(2016,1,10))
    maxiAccount.withdraw(10.0, D.date(2016,8,20))
    print(bank.totalInterestPaid())
    assert_equals(bank.totalInterestPaid(), .19)

def test_N_interestDaily():
    bank = Bank()
    maxiAccount    = Account(MAXI_SAVINGS)
    savingsAccount = Account(SAVINGS)
    bank.addCustomer(Customer("Magnus").openAccount(maxiAccount).openAccount(savingsAccount))
    maxiAccount.deposit(100.0, D.date(2016,1,10))
    maxiAccount.deposit(100.0, D.date(2016,2,10))
    maxiAccount.withdraw(10.0, D.date(2016,8,20))
    print(bank.N_totalInterestPaid())

if 1: # __name__ == '__main__':
    test_customer_summary()
    test_checking_account()
    test_savings_account()
    test_maxi_savings_account()
    test_MaxiAcct_last10()
    test_N_interestDaily()
