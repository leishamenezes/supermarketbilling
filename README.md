This code is a supermarket billing system using Python and MySQL, managing both product inventory and customer bills. Here’s the breakdown:

Database Connection:
Connects to a MySQL database named essentialsmart using given credentials. If the connection fails, it returns an error message.

Fetching Products:
Queries the products table to find products matching user input and returns relevant product details (ID, name, price, stock quantity).

Updating Stock:
After a purchase, it reduces the stock quantity for a product in the database.

Creating a Bill:
Calculates the total amount for the cart and inserts it into the billing table. For each item in the cart, it also adds individual product details (quantity, price) to the billingdetails table and updates the stock.

Printing a Bill:
Displays a formatted bill with the customer name, products, quantities, prices, and a grand total.

Checkout Process:
Completes the billing by calling create_bill and print_bill. If something goes wrong, it shows an error.

Main Flow:
Starts with the user entering product names, checks available products, and allows adding them to the cart. After confirming the cart, it processes the checkout, then exits.
