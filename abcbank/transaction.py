import datetime as D

class Transaction:
    def __init__(self, amount, tDate=D.date.today(), tType=0):
        self.amount = amount
        self.transactionDate = tDate
        self.tType = tType
