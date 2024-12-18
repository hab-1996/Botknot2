from flask import Flask, render_template, request, redirect, url_for, flash
from openpyxl import Workbook, load_workbook
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

EXCEL_FILE = 'user_data.xlsx'

# Initialize Excel file and ensure headers exist
def initialize_excel():
    if not os.path.exists(EXCEL_FILE):
        # Create a new Excel file with headers
        wb = Workbook()
        ws = wb.active
        ws.title = 'Users'
        ws.append(['Customer_ID', 'First_Name', 'Last_Name', 'Email', 'Country', 'City', 'Address', 'Password'])
        wb.save(EXCEL_FILE)
        print("Initialized 'user_data.xlsx' with headers.")


@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Collect form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        country = request.form['country']
        city = request.form['city']
        address = request.form['address']
        password = request.form['password']

        # Load Excel file
        wb = load_workbook(EXCEL_FILE)
        ws = wb.active

        # Ensure headers are intact before appending data
        if ws.cell(1, 1).value != 'Customer_ID':
            ws.insert_rows(1)
            ws.append(['Customer_ID', 'First_Name', 'Last_Name', 'Email', 'Country', 'City', 'Address', 'Password'])

        # Check for duplicate email
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row and row[3] == email:  # Email is in the 4th column
                flash('Email already exists! Please log in.', 'error')
                return redirect(url_for('signup'))

        # Determine the next Customer_ID
        last_customer_id = 1000
        for row in ws.iter_rows(min_row=2, max_col=1, values_only=True):
            if row[0] and isinstance(row[0], int):  # Ensure valid Customer_IDs
                last_customer_id = max(last_customer_id, int(row[0]))

        new_customer_id = last_customer_id + 1

        # Append new user data to Excel
        ws.append([new_customer_id, first_name, last_name, email, country, city, address, password])
        wb.save(EXCEL_FILE)

        flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('login_page'))

    return render_template('signup.html')

if __name__ == '__main__':
    initialize_excel()
    app.run(debug=True)
