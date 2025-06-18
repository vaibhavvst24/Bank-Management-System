🏦 Bank Account Management System
This is a command-line-based bank account management system built using Python. It allows users to create and manage their bank accounts, perform transactions, and generate detailed reports. The system also integrates MySQL for database operations, uses CSV files for backup, and provides visual analytics using Matplotlib and Seaborn.

It is also a web-based application developed using Flask (a Python web framework) that provides users with a seamless platform to manage their bank accounts. 
This system is designed to simulate essential banking operations like account creation, login authentication, 
and fund management while offering a user-friendly interface with a modern UI using HTML, CSS, and Boxicons.

📌 Features
🔐 User Account Features
Sign Up: Create a new account (Savings or Checking).

Password Validation: Ensures strong password (at least 1 uppercase, 1 lowercase, 1 digit, 1 special character, and minimum 8 characters).

Login: Secure access using account number and password.

Deposit & Withdraw: Perform basic banking operations.

Balance Check: View the current account balance.

🏦 Admin Features
View All Accounts: Displays complete account details.

Transaction History: View full transaction records.

Interest Application: Automatically apply 4% interest to all savings accounts.

Delete Account: Remove a user’s account and its transactions from both CSV and MySQL.

📊 Reporting & Analytics
Generate Reports:

Account balances

Transaction summaries

Aggregated account type summaries

Data Analytics & Visualizations:

Monthly transaction trends

Deposits vs Withdrawals vs Interest

Account type distribution

Average balance by account type

High-value transaction alerts (above ₹50,000)

User-specific Dashboard: Personalized visual reports for individual users

🗃️ Data Storage
This system uses a hybrid approach:

CSV Files:

bank_accounts.csv: Stores user details.

transactions.csv: Stores transaction records.

MySQL Database (bank_system):

accounts table

transactions table

🧰 Technologies Used
Python Libraries:

pandas – data management

pymysql – MySQL connection

matplotlib, seaborn – visualizations

getpass – password input

datetime – timestamping transactions

MySQL – backend relational database

📋 Functional Flow
Start the App: Run Main.py to start the menu-driven system.

Choose Action:

Sign up, Log in, Admin panel, etc.

Perform Transactions: Deposit, Withdraw, Balance inquiry.

Data Logging:

Every action updates both CSV and MySQL.

Analytics & Reports:

View detailed summaries and plots.

🌐 Web Interface (Flask + HTML/CSS)
The project includes a user-friendly web interface:

Flask Backend: Handles routing, logic, and database interaction

HTML Forms: For login, signup, deposits, withdrawals, and report access

CSS Styling: Clean, responsive UI with styled buttons, inputs, and tables

Chart Rendering: Plots are generated using Matplotlib and rendered as images

📈 Analytics Visualizations
Monthly Transaction Trend: Line chart showing frequency.

Transaction Type Summary: Bar chart for deposit, withdrawal, interest.

Account Type Pie Chart: Visual distribution of savings vs checking.

Average Balance Bar Chart: Average funds by account type.

High-Value Alerts: List of transactions above ₹50,000.

✅ Conclusion
This Bank Account Management System provides a complete and practical demonstration of how core banking operations can be implemented using Python, Flask, MySQL, and Data Visualization tools. It offers both command-line and web-based interfaces, making it a versatile learning and showcase project.

Whether you're a student learning backend development, a data analyst interested in financial datasets, or a developer exploring full-stack applications, this project integrates:

Database operations

Secure user authentication

Data storage and backups

Visual reports and dashboards

Clean and responsive UI with Flask + HTML/CSS
