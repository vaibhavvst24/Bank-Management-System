import pandas as pd
import os

FILE_NAME = 'bank_accounts.csv'
TRANSACTION_FILE_NAME = 'transactions.csv'

def load_accounts():
    return pd.read_csv(FILE_NAME)

def save_accounts(df):
    df.to_csv(FILE_NAME, index=False)

def load_transactions():
    return pd.read_csv(TRANSACTION_FILE_NAME)

def save_transaction(account_number, transaction_type, amount):
    df = load_transactions()
    new_transaction = pd.DataFrame([[account_number, transaction_type, amount, pd.Timestamp.now()]],
                                   columns=['Account Number', 'Transaction Type', 'Amount', 'Date'])
    df = pd.concat([df, new_transaction], ignore_index=True)
    df.to_csv(TRANSACTION_FILE_NAME, index=False)

def signup_user(name, password, account_type):
    df = load_accounts()
    acc_no = 1001 if df.empty else df['Account Number'].max() + 1
    initial_balance = 2000 if account_type == 'savings' else 1000

    new_account = pd.DataFrame([[acc_no, name, password, initial_balance, account_type]],
                               columns=['Account Number', 'Name', 'Password', 'Balance', 'Account Type'])
    df = pd.concat([df, new_account], ignore_index=True)
    save_accounts(df)

    save_transaction(acc_no, 'Deposit', initial_balance)
    return True, f'Account created! Your account number is {acc_no}'

def login_user(account_number, password):
    df = load_accounts()
    account = df[(df['Account Number'] == account_number) & (df['Password'] == password)]
    return not account.empty

def get_balance(account_number):
    df = load_accounts()
    return df[df['Account Number'] == account_number]['Balance'].values[0]

def deposit_amount(account_number, amount):
    df = load_accounts()
    df.loc[df['Account Number'] == account_number, 'Balance'] += amount
    save_accounts(df)
    save_transaction(account_number, 'Deposit', amount)

def withdraw_amount(account_number, amount):
    df = load_accounts()
    current_balance = df[df['Account Number'] == account_number]['Balance'].values[0]
    if amount > current_balance:
        return False, 'Insufficient funds.'
    df.loc[df['Account Number'] == account_number, 'Balance'] -= amount
    save_accounts(df)
    save_transaction(account_number, 'Withdrawal', amount)
    return True, 'Withdrawal successful.'

def get_transactions(account_number):
    df = load_transactions()
    return df[df['Account Number'] == account_number].to_dict(orient='records')

def get_all_accounts():
    return load_accounts().to_dict(orient='records')

def get_all_transactions():
    return load_transactions().to_dict(orient='records')
