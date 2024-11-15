import mysql.connector

# Define the mart name
mart_name = "Essentials Mart"
my_bill_id = 0

# Database connection details
def get_db_connection():
    try:
        con = mysql.connector.connect(
            user='root',
            password='sags@123',
            host='localhost',
            database='essentialsmart')
        return con
    except mysql.connector.Error as err:
        print("Error: Could not connect to the database.", err)
        return None

def fetch_products(con, product_name):
    try:
        cursor = con.cursor()
        query = "SELECT product_id, product_name, price, stock_quantity FROM products WHERE product_name LIKE %s"
        cursor.execute(query, ('%' + product_name + '%',))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error fetching products:", err)
        return []

def update_product_quantity(con, product_id, quantity):
    try:
        cursor = con.cursor()
        update_query = "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s"
        cursor.execute(update_query, (quantity, product_id))
        con.commit()
    except mysql.connector.Error as err:
        print("Error updating product quantity:", err)
        con.rollback()

def create_bill(con, customer_name, cart):
    try:
        cursor = con.cursor()

        # Calculate total amount
        total_amount = sum(price * quantity for _, _, quantity, price in cart)

        # Insert details into the billing table
        billing_query = "INSERT INTO billing (total_amount) VALUES (%s)"
        cursor.execute(billing_query, (total_amount,))
        bill_id = cursor.lastrowid
        global my_bill_id
        my_bill_id = bill_id

        for product_id, product_name, quantity, price in cart:
            total_price = price * quantity  # Calculate total price for each product
            detail_query = "INSERT INTO billingdetails (bill_id, customer_name, product_id, quantity, price_per_item, total_price) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(detail_query, (bill_id, customer_name, product_id, quantity, price, total_price))

            # Update the product quantity in the products table
            update_product_quantity(con, product_id, quantity)

        con.commit()
        return total_amount
    except mysql.connector.Error as err:
        print("Error creating bill:", err)
        con.rollback()
        return 0

def print_bill(customer_name, cart, total_amount):
    print('\n' * 30, '\t' * 4, mart_name, '\n')
    print('\t' * 4, "===== BILL =====\n")
    print("Bill No:", my_bill_id)
    print("Customer Name:", customer_name)
    print("{:<30} {:<10} {:<15} {:<10}".format("Product", "Quantity", "Price Per Item", "Total Price"))
    print("-" * 70)

    for product_id, product_name, quantity, price in cart:
        total_price = price * quantity
        print("{:<30} {:<10} Rs. {:<15.2f} Rs. {:<10.2f}".format(product_name, quantity, price, total_price))

    print("-" * 70)
    print("{:<50} Rs. {:.2f}".format("Grand Total", total_amount))
    print("======================")
    print("\n\nThank you for shopping with us at", mart_name + "!", '\n' * 11)

def checkout_process(con, cart, customer_name):
    while True:
        print("\nGenerating the bill...")

        total_amount = create_bill(con, customer_name, cart)
        if total_amount > 0:
            print_bill(customer_name, cart, total_amount)
            return False
        else:
            print("Error generating the bill.")
        break

def main():
    con = get_db_connection()
    if not con:
        return

    print("Welcome to", mart_name, "billing portal!")
    cart = []  # Initialize cart here

    while True:
        product_name = input("Please enter the product name: (type 'e' or 'exit' to finish) ").lower()
        if product_name == 'exit' or product_name == 'e':
            if not cart:
                print("Your cart is empty. Exiting without billing.")
                break
            else:
                customer_name = input("Please enter your name: ")
                if checkout_process(con, cart, customer_name):
                    break
                else:
                    cart.clear()
                    break

        products = fetch_products(con, product_name)
        if not products:
            print("No products found.")
            continue

        print("Here are the products with names containing", product_name, ":")
        for idx, (product_id, product_name, price, qty) in enumerate(products):
            print(idx + 1, "|", product_name, "| Rs.", "{:.2f}".format(price), "| Qty:", qty)

        while True:
            try:
                product_choice = int(input("Please enter the product number you want to buy: ")) - 1
                if 0 <= product_choice < len(products):
                    selected_product = products[product_choice]
                    product_id = selected_product[0]
                    break  # Valid choice, exit the loop
                else:
                    print("Invalid product selection. Please enter a valid product number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        while True:
            try:
                quantity = int(input("Please enter the quantity you would like to buy: "))
                if quantity <= 0:  # Check for negative or zero quantities
                    print("Invalid quantity. Quantity must be a positive number.")
                else:
                    available_qty = selected_product[3]
                    if quantity > available_qty:
                        print("Sorry, only", available_qty, "available.")
                    else:
                        print("Thank you! You have added", quantity, "of", selected_product[1], "to your cart.")
                        cart.append((product_id, selected_product[1], quantity, selected_product[2]))  # Add product_id, product_name, quantity, price
                        break  # Valid quantity, exit the loop
            except ValueError:
                print("Invalid quantity. Please enter a valid number.")

    con.close()
main()
