from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def connect_db():
    connection = sqlite3.connect("food_orders.db")
    return connection

# Route for the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route for adding a new order
@app.route("/add", methods=["GET", "POST"])
def add_order():
    if request.method == "POST":
        name = request.form.get("name")  # Safely extract form data
        order_item = request.form.get("order_item")
        cost = request.form.get("cost")
        place = request.form.get("place")  # Get the place input

        if not name or not order_item or not cost or not place:
            return "Error: Missing required fields!", 400
        
         
        # Connect to database and insert order
        connection = sqlite3.connect("food_orders.db")
        cursor = connection.cursor()
        
        cursor.execute("""
        INSERT INTO orders (name, order_item, cost, date, place)
        VALUES (?, ?, ?, ?, ?)
        """, (name, order_item, float(cost), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), place))


        
        connection.commit()
        connection.close()

        return redirect("/view")  # Redirect to view all orders

    return render_template("add_order.html")  # Show the form

def update_db():
    connection = sqlite3.connect("food_orders.db")
    cursor = connection.cursor()
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN place TEXT")
        connection.commit()
        print("Column 'place' added successfully!")
    except sqlite3.OperationalError:
        print("Column 'place' might already exist!")
    connection.close()

# Run update_db() once at startup
update_db()

def get_total_price(name):
    connection = sqlite3.connect("food_orders.db")
    cursor = connection.cursor()

    # Calculate total cost for a specific customer
    cursor.execute("SELECT SUM(cost) FROM orders WHERE name = ?", (name,))
    total_price = cursor.fetchone()[0]  # Get the sum value

    connection.close()

    return total_price if total_price else 0

def search_customer():
    if request.method == "POST":
        name = request.form["name"]
        connection = sqlite3.connect("food_orders.db")
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM orders WHERE name LIKE ?", (f"%{name}%",))
        orders = cursor.fetchall()

        # Get total price
        total_price = get_total_price(name)

        connection.close()
        return render_template("search_results.html", orders=orders, name=name, total_price=total_price)
    
    return render_template("search.html")

#Search  for all orders
@app.route("/search", methods=["GET", "POST"])
def search_orders():
    if request.method == "POST":
        search_query = request.form["search"]  # Get search input
        connection = sqlite3.connect("food_orders.db")
        cursor = connection.cursor()
        
        # Search for matching orders (case-insensitive)
        cursor.execute("SELECT * FROM orders WHERE name LIKE ? OR order_item LIKE ?", (f"%{search_query}%", f"%{search_query}%"))
        orders = cursor.fetchall()

        connection.close()
        return render_template("search_results.html", orders=orders, search_query=search_query)
    
    return render_template("search.html")  # Display search form

@app.route("/search", methods=["GET", "POST"])
def search_customer():
    if request.method == "POST":
        name = request.form["name"]
        connection = sqlite3.connect("food_orders.db")
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM orders WHERE name LIKE ?", (f"%{name}%",))
        orders = cursor.fetchall()

        # Get total price
        total_price = get_total_price(name)

        connection.close()
        return render_template("search_results.html", orders=orders, name=name, total_price=total_price)
    
    return render_template("search.html")


# Route for viewing all orders
@app.route("/view")
def view_orders():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders")  # The 'date' column is included here
    orders = cursor.fetchall()
    connection.close()
    return render_template("view_orders.html", orders=orders)



if __name__ == "__main__":
    # Create database and table if it doesn't exist
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    order_item TEXT NOT NULL,
    cost REAL NOT NULL,
    date TEXT NOT NULL,
    place TEXT NOT NULL
)
""")
    
    

    connection.commit()
    connection.close()
    
    app.run(debug=True)