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
        name = request.form["name"]
        order_item = request.form["order_item"]
        cost = request.form["cost"]
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time in YYYY-MM-DD HH:MM:SS format

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO orders (name, order_item, cost, date)
        VALUES (?, ?, ?, ?)
        """, (name, order_item, float(cost), date))
        connection.commit()
        connection.close()
        return redirect("/")
    return render_template("add_order.html")

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
    date TEXT NOT NULL
)
""")

    connection.commit()
    connection.close()
    
    app.run(debug=True)
