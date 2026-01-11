import json
import os
import uuid

USERS_FILE = "users.json"
PRODUCTS_FILE = "products.json"
ORDERS_FILE = "orders.json"


# ---------------- FILE HANDLING ----------------
def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []


def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- USER CLASS ----------------
class User:
    def __init__(self, name, email, password, address):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password
        self.address = address

    def to_dict(self):
        return self.__dict__


# ---------------- PRODUCT CLASS ----------------
class Product:
    def __init__(self, pid, name, category, price):
        self.product_id = pid
        self.name = name
        self.category = category
        self.price = price

    def to_dict(self):
        return self.__dict__


# ---------------- CART CLASS ----------------
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        self.items.append({"product": product, "quantity": quantity})

    def view_cart(self):
        total = 0
        print("\n--- Shopping Cart ---")
        for item in self.items:
            cost = item["product"]["price"] * item["quantity"]
            total += cost
            print(f'{item["product"]["name"]} | Qty: {item["quantity"]} | Rs.{cost}')
        print(f"Total: Rs.{total}")
        return total

    def remove_item(self, pid):
        self.items = [i for i in self.items if i["product"]["product_id"] != pid]

    def clear_cart(self):
        self.items = []


# ---------------- ORDER CLASS ----------------
class Order:
    def __init__(self, email, items, total):
        self.order_id = str(uuid.uuid4())
        self.email = email
        self.items = items
        self.total = total
        self.status = "Placed"

    def to_dict(self):
        return self.__dict__


# ---------------- INITIAL PRODUCTS ----------------
def init_products():
    if not os.path.exists(PRODUCTS_FILE):
        products = [
            Product("P1", "Rice", "Grocery", 60).to_dict(),
            Product("P2", "Milk", "Dairy", 30).to_dict(),
            Product("P3", "Soap", "Household", 25).to_dict(),
            Product("P4", "Sugar", "Grocery", 45).to_dict()
        ]
        save_data(PRODUCTS_FILE, products)


# ---------------- USER FUNCTIONS ----------------
def register_user():
    users = load_data(USERS_FILE)
    print("\n--- Register ---")
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    address = input("Address: ")

    users.append(User(name, email, password, address).to_dict())
    save_data(USERS_FILE, users)
    print("Registration successful!")


def login_user():
    users = load_data(USERS_FILE)
    email = input("Email: ")
    password = input("Password: ")

    for u in users:
        if u["email"] == email and u["password"] == password:
            print(f"Welcome {u['name']}!")
            return u
    print("Invalid login")
    return None


# ---------------- PRODUCT SEARCH ----------------
def search_products():
    products = load_data(PRODUCTS_FILE)
    key = input("Search by name/category: ").lower()

    results = [p for p in products if key in p["name"].lower() or key in p["category"].lower()]
    if not results:
        print("No products found.")
    else:
        for p in results:
            print(f'{p["product_id"]} | {p["name"]} | {p["category"]} | Rs.{p["price"]}')
    return results


# ---------------- CHECKOUT ----------------
def checkout(user, cart):
    total = cart.view_cart()
    if total == 0:
        return

    confirm = input("Proceed to checkout? (y/n): ")
    if confirm.lower() == "y":
        orders = load_data(ORDERS_FILE)
        orders.append(Order(user["email"], cart.items, total).to_dict())
        save_data(ORDERS_FILE, orders)
        cart.clear_cart()
        print("Order placed successfully!")


# ---------------- ORDER HISTORY ----------------
def view_orders(user):
    orders = load_data(ORDERS_FILE)
    print("\n--- Order History ---")
    for o in orders:
        if o["email"] == user["email"]:
            print(f'Order ID: {o["order_id"]} | Total: Rs.{o["total"]} | Status: {o["status"]}')


# ---------------- MAIN MENU ----------------
def main():
    init_products()
    cart = Cart()
    current_user = None

    while True:
        print("\n===== HOME MENU =====")
        print("1. Register")
        print("2. Login")
        print("3. Search Products")
        print("4. View Cart")
        print("5. Checkout")
        print("6. Order History")
        print("7. Exit")

        choice = input("Choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            current_user = login_user()
        elif choice == "3":
            results = search_products()
            if results:
                pid = input("Enter Product ID to add to cart: ")
                for p in results:
                    if p["product_id"] == pid:
                        qty = int(input("Quantity: "))
                        cart.add_item(p, qty)
                        print("Item added to cart")
        elif choice == "4":
            cart.view_cart()
        elif choice == "5":
            if current_user:
                checkout(current_user, cart)
            else:
                print("Login required")
        elif choice == "6":
            if current_user:
                view_orders(current_user)
            else:
                print("Login required")
        elif choice == "7":
            print("Thank you for shopping!")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
