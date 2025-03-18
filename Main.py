import pandas as pd
import os
import pymysql
from getpass import getpass
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

FILE_NAME = 'bank_accounts.csv'
TRANSACTION_FILE_NAME = 'transactions.csv'

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=['Account Number', 'Name', 'Password', 'Balance'])
    df.to_csv(FILE_NAME, index=False)

if not os.path.exists(TRANSACTION_FILE_NAME):
    df = pd.DataFrame(columns=['Account Number', 'Transaction Type', 'Amount', 'Date'])
    df.to_csv(TRANSACTION_FILE_NAME, index=False)

def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",       
        password="oracle",   
        database="bank_system"
    )

def load_data_csv():     
    return pd.read_csv(FILE_NAME)

def save_data_csv(df):
    df.to_csv(FILE_NAME, index=False)

def load_data_mysql():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM accounts")
    data = cursor.fetchall()
    db.close()
    
    return pd.DataFrame(data, columns=['Account Number', 'Name', 'Password', 'Balance', 'Account Type'])

def save_data_mysql(account_number, name, password, balance, account_type):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO accounts (account_number, name, password, balance, account_type) VALUES (%s, %s, %s, %s, %s)",
        (account_number, name, password, balance, account_type)
    )
    db.commit()
    db.close()

def log_transaction_csv(account_number, transaction_type, amount):
    df = pd.read_csv(TRANSACTION_FILE_NAME)
    new_transaction = pd.DataFrame([[account_number, transaction_type, amount, datetime.now()]],
                                   columns=['Account Number', 'Transaction Type', 'Amount', 'Date'])
    df = pd.concat([df, new_transaction], ignore_index=True)
    df.to_csv(TRANSACTION_FILE_NAME, index=False)

def log_transaction_mysql(account_number, transaction_type, amount):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO transactions (account_number, transaction_type, amount, date) VALUES (%s, %s, %s, %s)",
        (account_number, transaction_type, amount, datetime.now())
    )
    db.commit()
    db.close()

def Interest():
    df_csv = load_data_csv()

    for index, account in df_csv.iterrows():
        if account['Account Type'] == 'savings':
            interest_rate = 0.04  # 4% interest for savings accounts
            interest = account['Balance'] * interest_rate
            new_balance = account['Balance'] + interest

            df_csv.at[index, 'Balance'] = new_balance
            save_data_csv(df_csv)

            log_transaction_csv(account['Account Number'], 'Interest', interest)
            log_transaction_mysql(account['Account Number'], 'Interest', interest)

            print(f"Interest of {interest} added to account {account['Account Number']}. New balance: {new_balance}")


def password_validation(password):
    i = 0

    upper = 0
    lower = 0
    digit = 0
    special = 0

    if len(password) >= 8:
        while i < len(password):
            if password[i].isupper():
                upper += 1
            elif password[i].islower():
                lower += 1
            elif password[i].isdigit():
                digit += 1
            elif not password[i].isidentifier():
                special += 1

            i += 1
        
        if upper >= 1 and lower >= 1 and digit >= 1 and special >= 1:
            return True
        else:
            return False
        
    else:
        return False

def signup():
    df_csv = load_data_csv()
    
    user_name = input("Enter your name: ")
    password = getpass('Enter your password: ')
    if not password_validation(password):
        print("Invalid password.")
        return

    account_type_choice = int(input("Select account type:\n1. Savings (4% interest)\n2. Checking (No interest)\nEnter your choice: "))
    account_type = 'savings' if account_type_choice == 1 else 'checking'
    
    initial_balance = 2000 if account_type == 'savings' else 1000
    print(f"An initial deposit of {initial_balance}/- is required to open a {account_type} account.")
    choice = input('Do you want to proceed with the initial deposit? (y/n): ').lower()
    
    if choice == 'y':
        balance = initial_balance
        acc_no = 1001 if df_csv.empty else df_csv['Account Number'].max() + 1
        
        new_account_csv = pd.DataFrame([[acc_no, user_name, password, balance, account_type]],
                                       columns=['Account Number', 'Name', 'Password', 'Balance', 'Account Type'])
        df_csv = pd.concat([df_csv, new_account_csv], ignore_index=True)
        save_data_csv(df_csv)
        
        save_data_mysql(acc_no, user_name, password, balance, account_type)
        
        log_transaction_csv(acc_no, 'Deposit', balance)
        log_transaction_mysql(acc_no, 'Deposit', balance)
        
        print(f"Account created successfully! Your account number is {acc_no}")
    else:
        print("Initial deposit is required to open an account. Thank you for your time.")


def login():
    df_csv = load_data_csv()
    
    account_number = int(input("Enter your account number: "))
    password = getpass("Enter your password: ")
    
    account = df_csv[df_csv['Account Number'] == account_number]
    if account.empty or account.iloc[0]['Password'] != password:
        print("Invalid account number or password.")
        return None
    else:
        print("Login successful!")
        return account.iloc[0]

def balance(account):
    print(f"Your current balance is: {account['Balance']}")

def deposit(account):
    df_csv = load_data_csv()
    db = connect_db()
    cursor = db.cursor()
    
    amount = float(input("Enter the amount to deposit: "))
    
    df_csv.loc[df_csv['Account Number'] == account['Account Number'], 'Balance'] += amount
    save_data_csv(df_csv)
    
    new_balance = account['Balance'] + amount
    cursor.execute(
        "UPDATE accounts SET balance = %s WHERE account_number = %s",
        (new_balance, account['Account Number'])
    )
    db.commit()
    db.close()
    
    log_transaction_csv(account['Account Number'], 'Deposit', amount)
    log_transaction_mysql(account['Account Number'], 'Deposit', amount)
    
    print(f"${amount} deposited successfully!")
    account['Balance'] = new_balance

def withdraw(account):
    df_csv = load_data_csv()
    db = connect_db()
    cursor = db.cursor()
    
    amount = float(input("Enter the amount to withdraw: "))
    
    if amount > account['Balance']:
        print("Insufficient funds!")
    else:
        df_csv.loc[df_csv['Account Number'] == account['Account Number'], 'Balance'] -= amount
        save_data_csv(df_csv)
        
        new_balance = account['Balance'] - amount
        cursor.execute(
            "UPDATE accounts SET balance = %s WHERE account_number = %s",
            (new_balance, account['Account Number'])
        )
        db.commit()
        db.close()
        
        log_transaction_csv(account['Account Number'], 'Withdrawal', amount)
        log_transaction_mysql(account['Account Number'], 'Withdrawal', amount)
        
        print(f"${amount} withdrawn successfully!")
        account['Balance'] = new_balance

def Admin():
    df_csv = load_data_csv()
    df_transactions = pd.read_csv(TRANSACTION_FILE_NAME)
    
    print("Admin Interface")
    print("1. View all accounts")
    print("2. View transaction history")
    
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        print(df_csv)
    elif choice == 2:
        print(df_transactions)
    else:
        print("Invalid choice.")

def delete_account():
    df_csv = load_data_csv()
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='oracle',
        database='bank_system'
    )
    
    account_number = int(input("Enter the account number to delete: "))
    
    try:
        if account_number in df_csv['Account Number'].values:
            df_csv = df_csv[df_csv['Account Number'] != account_number]
            save_data_csv(df_csv)
            
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM accounts WHERE account_number = %s", (account_number,))
                cursor.execute("DELETE FROM transactions WHERE account_number = %s", (account_number,))
                connection.commit()
                
            print(f"Account number {account_number} has been deleted successfully.")
        else:
            print("Account number does not exist.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def generate_reports():
    # Load data from CSV for reporting
    df_csv = load_data_csv()
    df_transactions = pd.read_csv('transactions.csv')  
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='oracle',
        database='bank_system'
    )
    
    print("\nReport Options:")
    print("1. Account Balances")
    print("2. Transaction History")
    print("3. Account Summary")
    
    choice = int(input("Enter your choice: "))
    
    try:
        if choice == 1:
            print("\nAccount Balances:")
            print(df_csv[['Account Number', 'Name', 'Balance']])
            
        elif choice == 2:
            print("\nTransaction History:")
            print(df_transactions)
            
        elif choice == 3:
            print("\nAccount Summary:")
            account_summary = df_csv.groupby('Account Type').agg(
                total_balance=('Balance', 'sum'),
                num_accounts=('Account Number', 'count')
            )
            print(account_summary)
            
        else:
            print("Invalid choice.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def generate_analytics():
    df_transactions = pd.read_csv('transactions.csv')
    df_accounts = pd.read_csv('bank_accounts.csv')

    df_transactions['Date'] = pd.to_datetime(df_transactions['Date'])
    df_transactions['Month'] = df_transactions['Date'].dt.to_period('M')

    # -----------------------------
    # 1. Monthly Transaction Trend
    # -----------------------------
    monthly_trend = df_transactions.groupby('Month').size()

    plt.figure(figsize=(8, 6))
    sns.lineplot(x=monthly_trend.index.astype(str), y=monthly_trend.values, marker='o')
    plt.xticks(rotation=45)
    plt.title('Monthly Transaction Volume')
    plt.xlabel('Month')
    plt.ylabel('Number of Transactions')
    plt.grid(True)
    plt.show()

    # -----------------------------
    # 2. Deposits vs Withdrawals vs Interest
    # -----------------------------
    transaction_summary = df_transactions.groupby('Transaction Type')['Amount'].sum()

    plt.figure(figsize=(8, 5))
    transaction_summary.plot(kind='bar', color=['green', 'red', 'orange'])
    plt.title('Total Deposits vs Withdrawals vs Interest')
    plt.ylabel('Amount (₹)')
    plt.show()

    # -----------------------------
    # 3. Account Type Distribution
    # -----------------------------
    account_type_distribution = df_accounts['Account Type'].value_counts()

    plt.figure(figsize=(6, 6))
    account_type_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgreen'])
    plt.title('Account Type Distribution')
    plt.ylabel('')
    plt.show()

    # -----------------------------
    # 4. Average Balance Per Account Type
    # -----------------------------
    average_balance = df_accounts.groupby('Account Type')['Balance'].mean()

    plt.figure(figsize=(8, 5))
    average_balance.plot(kind='bar', color='purple')
    plt.title('Average Balance Per Account Type')
    plt.ylabel('Average Balance (₹)')
    plt.xticks(rotation=0)
    plt.show()

    # -----------------------------
    # 5. High-Value Transaction Alerts
    # -----------------------------
    HIGH_VALUE_THRESHOLD = 50000
    high_value_transactions = df_transactions[df_transactions['Amount'] > HIGH_VALUE_THRESHOLD]

    if not high_value_transactions.empty:
        print("\n⚠️ High-Value Transactions (over ₹50,000):")
        print(high_value_transactions)
    else:
        print("\n✅ No high-value transactions found.")

def user_dashboard(account_number):
    df_transactions = pd.read_csv('transactions.csv')
    user_transactions = df_transactions[df_transactions['Account Number'] == account_number]

    if user_transactions.empty:
        print("\nNo transactions found for your account.")
        return

    user_transactions['Date'] = pd.to_datetime(user_transactions['Date'])
    user_transactions['Month'] = user_transactions['Date'].dt.to_period('M')

    # Monthly Transaction Trend (for this user)
    monthly_trend = user_transactions.groupby('Month').size()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=monthly_trend.index.astype(str), y=monthly_trend.values, marker='o')
    plt.title(f'Monthly Transaction Volume - Account {account_number}')
    plt.xlabel('Month')
    plt.ylabel('Number of Transactions')
    plt.grid(True)
    plt.show()

    # Deposits vs Withdrawals (for this user)
    transaction_summary = user_transactions.groupby('Transaction Type')['Amount'].sum()
    plt.figure(figsize=(8, 5))
    transaction_summary.plot(kind='bar', color=['green', 'red', 'orange'])
    plt.title(f'Deposits vs Withdrawals - Account {account_number}')
    plt.ylabel('Amount (₹)')
    plt.show()

def main():
    while True:
        print("\nWelcome to the Bank System")
        print("1. Sign up (Create Account)")
        print("2. Log in")
        print("3. Admin")
        print("4. Interest (Admin Only)")
        print("5. Delete Account")
        print("6. Generate Reports")
        print("7. Generate Analytics Reports")
        print("8. User Reports")
        print("9. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            signup()
        elif choice == 2:
            account = login()
            if account is not None:
                while True:
                    print("\n1. View Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Logout")
                    
                    choice = int(input("Enter your choice: "))
                    
                    if choice == 1:
                        balance(account)
                    elif choice == 2:
                        deposit(account)
                    elif choice == 3:
                        withdraw(account)
                    elif choice == 4:
                        break
                    else:
                        print("Invalid choice.")
        elif choice == 3:
            Admin()
        elif choice == 4:
            Interest()
        elif choice == 5:
            delete_account()
        elif choice == 6:
            generate_reports()
        elif choice == 7:
            generate_analytics()
        elif choice == 8:
            account_number = int(input("Enter your account number to view your reports: "))
            user_dashboard(account_number)
        elif choice == 9:
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()