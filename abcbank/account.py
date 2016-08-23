from abcbank.transaction import Transaction
import datetime as D

CHECKING = 0
SAVINGS = 1
MAXI_SAVINGS = 2

DEP_WITH = 0
TRANSFER = 1

"""
1) transfer between their accounts
2) Change Maxi-Savings accounts to have an interest rate of 5% assuming 
   no withdrawals in the past 10 days otherwise 0.1%
3) Interest rates should accrue daily (incl. wknds), rates above are per-annum"""


def compound_interest(principal, rate, times_per_year, years):
    body = 1 + (rate / times_per_year) # (1 + r/n)
    exponent = times_per_year * years  # P(1 + r/n)^nt
    intEarned = (principal * pow(body, exponent)) - principal
    return intEarned

class Account:
    def __init__(self, accountType):
        self.accountType = accountType
        self.transactions = []

    def deposit(self, amount, tDte=D.date.today()):
        if (amount <= 0): raise ValueError("amount must be greater than zero")
        else:             self.transactions.append(Transaction(amount, tDte, DEP_WITH))

    def withdraw(self, amount, tDte=D.date.today()):
        if (amount <= 0): raise ValueError("amount must be greater than zero")
        else:             self.transactions.append(Transaction(-amount, tDte, DEP_WITH))

    def transfer(self, toAcct, amount, tDte=D.date.today()):
        if (amount <= 0): raise ValueError("amount must be greater than zero")
        else:             
            self.transactions.append(Transaction(-amount, tDte, TRANSFER))
            toAcct.transactions.append(Transaction(+amount, tDte, TRANSFER))

    def interestEarned(self):
        amount = self.sumTransactions()
        if self.accountType == SAVINGS:
            if (amount <= 1000): return amount * 0.001
            else:   return 1 + (amount - 1000) * 0.002
        elif self.accountType == MAXI_SAVINGS:
            if (self.withdrawnInLast10()): return amount * 0.001
            else:                          return amount * 0.05

            if   (amount <= 1000): return               amount * 0.02
            elif (amount <= 2000): return 20 + (amount - 1000) * 0.05
            else:                  return 70 + (amount - 2000) * 0.1
        elif self.accountType == CHECKING: return amount * 0.001
        else: raise ValueError("Unknown Acct Type")

    def N_interestEarned(self):
        if len(self.transactions) == 0: return 0
        sum_intEarned = 0
        sum_amt       = self.transactions[0].amount
        last_transaction_date = self.transactions[0].transactionDate
        last_withdrawl_date   = D.date(1970,1,1)
        for t in self.transactions[1:]:
            nDays = (t.transactionDate-last_transaction_date).days
            sum_amt += t.amount
            lowr_maxi = (t.transactionDate - last_withdrawl_date).days <= 10
            annual_rate = self.calc_interestRate(sum_amt, lowr_maxi)
            sum_intEarned += compound_interest(sum_amt, annual_rate, 365, nDays/365)
            if t.amount < 0: last_withdrawl_date = t.transactionDate
        return sum_intEarned

    def calc_interestRate(self, amount, low_maxi):
        if self.accountType == SAVINGS:
            if (amount <= 1000): return 0.001
            else:   return (1 + (amount - 1000) * 0.002) / amount
        elif self.accountType == MAXI_SAVINGS:
            if (low_maxi): return 0.001
            else:                          return 0.05
        elif self.accountType == CHECKING: return 0.001
        else: raise ValueError("Unknown Acct Type")

    def sumTransactions(self, checkAllTransactions=True):
        return sum([t.amount for t in self.transactions])
        
    def withdrawnInLast10(self):
        today = D.date.today() 
        for t in self.transactions:
            if (((today-t.transactionDate).days <= 10) and (t.amount < 0) ): return 1 
        return 0
