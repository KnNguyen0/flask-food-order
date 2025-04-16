import sqlite3
from datetime import datetime  # Import to handle the current date and time

# Connect to a database (or create one if it doesn't exist)
connection = sqlite3.connect("food_orders.db")
cursor = connection.cursor()

connection.commit()

print("The 'date' column has been successfully added!")

# Add the column or recreate the table
try:
    cursor.execute("ALTER TABLE orders ADD COLUMN date TEXT")
    connection.commit()
    print("The 'date' column has been successfully added!")
except sqlite3.OperationalError:
    print("The 'date' column already exists!")
    cursor.execute("ALTER TABLE orders ADD COLUMN place TEXT")

# Function to add a new order
def add_order(name, order_item, cost, place):
    # Capture the current date and time in the desired format
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update the INSERT query to include the 'date' column
    cursor.execute("""
    INSERT INTO orders (name, order_item, cost, date, place)
    VALUES (?, ?, ?, ?,?)
    """, (name, order_item, cost, date, place))
    connection.commit()
    print(f"Order for {name} added successfully on {date}!")

# Function to view all orders
def view_orders():
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    for row in rows:
        # Display the 'date' field along with other details
        print(f"ID: {row[0]}, Name: {row[1]}, Order Item: {row[2]}, Cost: ${row[3]}, Date: {row[4]}, Place: {row[5]}")

# Menu for user input
while True:
    print("\nOptions:")
    print("1. Add a new order")
    print("2. View all orders")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter customer name: ")
        order_item = input("Enter order item: ")
        cost = float(input("Enter cost of the item: "))
        place = input("Enter place name")
        add_order(name, order_item, cost, place)
    elif choice == "2":
        print("\nAll Orders:")
        view_orders()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, please try again.")

# Close the database connection when done
connection.close()