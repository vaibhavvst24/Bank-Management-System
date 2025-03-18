from flask import Flask, render_template, request, redirect, url_for, session, flash
from bank_functions import signup_user, login_user, get_balance, deposit_amount, withdraw_amount, get_transactions, get_all_accounts, get_all_transactions
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session handling

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        account_type = request.form['account_type']
        success, message = signup_user(name, password, account_type)
        flash(message)
        if success:
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_number = int(request.form['account_number'])
        password = request.form['password']
        account = login_user(account_number, password)
        if account:
            session['account_number'] = account_number
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Try again.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'account_number' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    
    account_number = session['account_number']
    balance = get_balance(account_number)
    transactions = get_transactions(account_number)
    return render_template('dashboard.html', balance=balance, transactions=transactions)

@app.route('/deposit', methods=['POST'])
def deposit():
    amount = float(request.form['amount'])
    deposit_amount(session['account_number'], amount)
    flash(f'Deposited ₹{amount} successfully!')
    return redirect(url_for('dashboard'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    amount = float(request.form['amount'])
    success, message = withdraw_amount(session['account_number'], amount)
    flash(message)
    return redirect(url_for('dashboard'))

@app.route('/admin')
def admin():
    accounts = get_all_accounts()
    transactions = get_all_transactions()
    return render_template('admin.html', accounts=accounts, transactions=transactions)

@app.route('/logout')
def logout():
    session.pop('account_number', None)
    flash('Logged out successfully.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
