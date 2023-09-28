# import sqlite3

# login_details=sqlite3.connect('loginDetails.sqlite')

# #Create database
# cursor=login_details.cursor()
# sql_query=('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL)''')
# cursor.execute(sql_query)

# print("DB created")

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db='Bidding2/loginCred3.sqlite'

# Initialize biddingTime and startBid variables
biddingTime = 0  # Initialize with default value
startBid = False  # Initialize as False
bid_duration = 0
Secret_Number='1234'

#Retailer
# Initialize an empty list to store selected items
# Initialize selected_items with some sample items
selected_items = [
    {
        'username': 'Retailer1',
        'name': 'Carrots',
        'quantity': 2,
        'price': 1.5
    },
    {
        'username': 'Retailer2',
        'name': 'Tomatoes',
        'quantity': 3,
        'price': 2.0
    },
    {
        'username': 'Retailer3',
        'name': 'Broccoli',
        'quantity': 1,
        'price': 1.0
    }
]


#Farmer 
# Initialize the vegetables list with existing vegetables
vegetables = [
    {"name": "Carrots", "quantity": 2, "username": "Farmer1"},
    {"name": "Tomatoes", "quantity": 2, "username": "Farmer2"},
    {"name": "Broccoli", "quantity": 2, "username": "Farmer3"}
]

@app.route('/add_vegetable', methods=['POST'])
def add_vegetable():
    # Get the vegetable name and quantity from the form
    vegetable_name = request.form.get('vegetable_name')
    quantity = int(request.form.get('quantity'))
    
    # Get the username from the form
    username = request.form.get('username')

    # Add the new vegetable to the vegetables list with the provided username
    vegetables.append({"name": vegetable_name, "quantity": quantity, "username": username})

    # Redirect back to the farmer page with the username
    # return redirect(f'/farmer/{username}')
    print(vegetables)
    return render_template('farmer.html', username=username,vegetables=vegetables)



#Admin functions
@app.route('/admin')
def admin():
    return render_template('admin.html',biddingTime=biddingTime, startBid=startBid,vegetables=vegetables,bid_duration=bid_duration,selected_items=selected_items)

# Route to handle form submission for setting bidding time
@app.route('/set_bidding_time', methods=['POST'])
def set_bidding_time():
    global biddingTime
    global bid_duration

    bid_duration=(request.form.get('bid_duration'))
    biddingTime = (request.form.get('biddingTime'))
    return redirect('/admin')


#Toggle Bid
# Route to handle form submission for starting or stopping the bid
@app.route('/toggle_bid', methods=['POST'])
def toggle_bid():
    global startBid
    startBid = not startBid  # Toggle the value of startBid

    return redirect('/admin')


# Route to handle placing an order
# @app.route('/place_order', methods=['POST'])
@app.route('/place_order', methods=['POST'])
def place_order():
    username = request.form.get('username')
    selected_vegetable = request.form.get('selected_vegetable')
    price = float(request.form.get('price'))  # Convert price to float

    # Find the selected vegetable in the vegetables list
    selected_vegetable_data = next((veg for veg in vegetables if veg['name'] == selected_vegetable), None)

    if selected_vegetable_data:
        name = selected_vegetable_data['name']
        quantity = selected_vegetable_data['quantity']

        # Create a dictionary representing the order
        order = {
            'username': username,
            'name': name,
            'quantity': quantity,
            'price': price
        }

        # Check if the item already exists in selected_items
        existing_item = next((item for item in selected_items if item['name'] == name), None)

        if existing_item:
            # Compare the new price with the existing price
            if price > existing_item['price']:
                # Update the item with the new price and username
                existing_item['price'] = price
                existing_item['username'] = username
        else:
            # Add the order to the selected_items list if it doesn't exist
            selected_items.append(order)

    # Redirect to the retailer page or perform other actions as needed
    return render_template('retailer.html', username=username, vegetables=vegetables, startBid=startBid, selected_items=selected_items)



# Create DB function
def create_users_table():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    sql_query = '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, role TEXT NOT NULL)'''
    cursor.execute(sql_query)

    conn.commit()
    conn.close()

# Create the 'users' table
create_users_table()
print("DB created")


# Insert Function
def insert_user(username, password, email,role):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Check if the email already exists in the database
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        print("Email Already Exist")
        return "Already"
    else:
        # If the email doesn't exist, insert the user
        cursor.execute("INSERT INTO users (username, password, email,role) VALUES (?, ?, ?, ?)", (username, password, email,role))
        conn.commit()
        conn.close()
        # return "Account created successfully"
        return "Inserted"


# SEE bid 
@app.route('/see_bid')
def see_bid():
    return render_template('bid_Details.html',bid_duration=bid_duration,biddingTime=biddingTime,startBid=startBid,selected_items=selected_items)

# LOGIN 
def verify_login(username, password):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user is None:
        conn.close()
        return None  # Username doesn't exist in the database

    # Check if the provided password matches the stored password
    if user[2] == password:
        conn.close()
        return user  # Successful login
    else:
        conn.close()
        return False  # Incorrect password

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        login_result = verify_login(username, password)

        if login_result is None:
            error_message = "Username doesn't exist."
            return render_template('login.html', error_message=error_message)
        elif login_result is False:
            error_message = "Incorrect password."
            return render_template('login.html', error_message=error_message)
        else:
            role = login_result[4]
            return redirect(url_for('home_page', username=username, role=role))

    return render_template('login.html')



# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Home Page function for user
@app.route('/home_page/<username>/<role>')
def home_page(username,role):
    # Implement the logic for the home page here
    # return f'Welcome, {username}!'

    if(role=='farmer'):
        # return "Hello Farmer"
        return render_template('farmer.html', username=username,vegetables=vegetables)
    elif(role=='retailer'):
        return render_template('retailer.html', username=username,vegetables=vegetables,startBid=startBid,selected_items=selected_items)
    elif(role=='admin'):
        return render_template('admin.html',username=username,biddingTime=biddingTime, startBid=startBid,vegetables=vegetables,bid_duration=bid_duration,selected_items=selected_items)
        # return render_template(admin(username))

# Signup function
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # print("Opened the signup page")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role=request.form['role']

        if role=='admin':
            return render_template('admin_check.html',username=username,password=password,email=email,role=role)

        # Next Plan:
        
        # Hash the password (you should use a proper password hashing library)
        # hashed_password = password  # Replace this with actual password hashing

        insert_update=insert_user(username, password, email,role)
        # print(insert_update)

        if insert_update=='Inserted':
            return redirect(url_for('home_page', username=username,role=role))
        else:
            error_message = "Email Already Exist"
            return render_template('signup.html', error_message=error_message)
            # flash('Account created successfully!', 'success')
        
    return render_template('signup.html')


# Signup function
@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_check():
    username = request.form['username']
    password=request.form['password']
    email=request.form['email']
    role=request.form['role']

    security_number=request.form['security_number']

    # return security_number
    if security_number==Secret_Number:
        insert_update=insert_user(username, password, email,role)
            # print(insert_update)

        if insert_update=='Inserted':
            return redirect(url_for('home_page', username=username,role=role))
        else:
            error_message = "Email Already Exist"
            return render_template('signup.html', error_message=error_message)
    else:
        error_message="Password wrong"
        return render_template('admin_check.html',error_message=error_message)



## TEST

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
