#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 23:17:07 2022

@author: zhongmeiru
"""
import csv
import os
from prettytable import PrettyTable

def read_file(filename,has_header=True):
    transactions = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        if has_header:
            next(reader,None)
        for row in reader:
            transactions.append((row[0].strip(),
                                row[1].strip(),
                                row[2].strip(),
                                row[3].strip()))
    return transactions


def get_text_between_two_delimiters(text,delimiter_1,delimiter_2):
    index_start = text.index(delimiter_1)
    index_end = text.index(delimiter_2)
    return text[index_start+1:index_end]

class account:
    def __init__(self,name,account_type):
        self._name = name
        self._account_type = account_type
        self._fees_charged = 0
        self._balance = 0
        
    def get_name(self):
        return self._name
    
    def get_account_type(self):
        return self._account_type
    
    def get_fees_charged(self):
        return self._fees_charged
    
    def get_balance(self):
        return self._balance
    
class retailaccount(account):
    def __init__(self,name,account_type):
        account.__init__(self,name,account_type)
    
    def process_transaction(self,deposit,amount):
        if deposit:
            self._balance += amount
        elif self._balance - amount <0:
            fee = 30
            self._balance -= fee
            self._fees_charged += fee
        else:
            self._balance -= amount
            
class businessaccount(account):
    def __init__(self,name,account_type):
        account.__init__(self,name,account_type)
        
    def process_transaction(self,deposit,amount):
        if deposit:
            self._balance += float(amount)
        elif self._balance - float(amount) <0:
            fee = 0.01*(float(amount) - self._balance)
            self._balance -= fee
            self._fees_charged += fee
        else:
            self._balance -= float(amount)
            
class bank:
    def __init__(self):
        self.transaction_files = {}
        self.accounts = {}
        self.fees_charged = {}
        
    def get_transaction_files(self,directory):
        for file in os.listdir(directory):
            if file.startswith('transactions') and file.endswith('.csv'):
                num = get_text_between_two_delimiters(file,'_','.')
                self.transaction_files[int(num)] = file
    
    def process_transaction_files(self):
        num = 1
        while True:
            if num not in self.transaction_files.keys():
                break
            self.process_transaction(self.transaction_files[num])
            num += 1
            
    def process_transaction(self,file):
        transactions = read_file(file,False)
        for transaction in transactions:
            account = None
            if transaction[1] == 'R':
                if transaction[0] not in self.accounts.keys():
                    account = retailaccount(transaction[0],transaction[1])
                    self.accounts[account.get_name()] = account
                else:
                    account = self.accounts[transaction[0]]
            elif transaction[1] == 'B':
                if transaction[0] not in self.accounts.keys():
                    account = businessaccount(transaction[0],transaction[1])
                    self.accounts[account.get_name()] = account
                else:
                    account = self.accounts[transaction[0]]
            account.process_transaction(transaction[2]=='D',float(transaction[3]))
            
    def report(self):
        overall_retail_account_balance,overall_business_account_balance = 0,0
        overall_retail_fees, overall_business_fees = 0, 0
        retail_accounts, business_accounts = [], []
        
        for name, account in self.accounts.items():
            if account.get_account_type() == 'R':
                overall_retail_account_balance += account.get_balance()
                overall_retail_fees += account.get_fees_charged()
                retail_accounts.append(account)
            elif account.get_account_type() == 'B':
                overall_business_account_balance += account.get_balance()
                overall_business_fees += account.get_fees_charged()
                business_accounts.append(account)
        sorted_retail_balance = sorted(retail_accounts,key=lambda x: x.get_balance(), reverse = True)
        sorted_business_balance = sorted(business_accounts,key=lambda x: x.get_balance(), reverse = True)
        
        print()
        x= PrettyTable()
        x.field_names = ['Name','Balance','Fees Charged']
        for field_name in x.field_names:
            x.align[field_name] = 'r'
        for account in sorted_retail_balance:
            x.add_row([account.get_name(),round(account.get_balance(),2),round(account.get_fees_charged(),2)])
        x.add_row([' ',' ',' '])
        x.add_row(['Total',round(overall_retail_account_balance,2),round(overall_retail_fees,2)])
        print(x.get_string(title='Retail Accounts'))
        
        print()
        x= PrettyTable()
        x.field_names = ['Name','Balance','Fees Charged']
        for field_name in x.field_names:
            x.align[field_name] = 'r'
        for account in sorted_business_balance:
            x.add_row([account.get_name(),round(account.get_balance(),2),round(account.get_fees_charged(),2)])
        x.add_row([' ',' ',' '])
        x.add_row(['Total',round(overall_business_account_balance,2),round(overall_business_fees,2)])
        print(x.get_string(title='Business Accounts'))
             
def main():
    bank_account = bank()
    #bank_account.get_transaction_files('C:/Users/mac/Desktop/brandeis/python2')
    bank_account.process_transaction('transactions_2.csv')
    bank_account.process_transaction_files()
    bank_account.report()
    
if __name__ == '__main__':
    main()
