import random
import qrcode 
# Admin Functions

def add_user(user_type, username, password):
    with open("users.txt", "a") as file:
        file.write(f"{user_type},{username},{password}\n")
    print("User added successfully.")

def view_users():
    with open("users.txt", "r") as file:
        for line in file:
            print(line.strip())

def generate_report():
    with open("users.txt", "r") as file:
        users = file.readlines()
    print(f"Total users: {len(users)}")

def view_pending_orders():
    print("Pending Orders:")
    with open("orders.txt", "r") as file:
        for line in file:
            order_id, status = line.strip().split(',')
            if status == "pending":
                print(f"Order ID: {order_id}")



# Farmer Functions

def browse_seeds():
    with open("seeds.txt", "r") as file:
        for line in file:
            print(line.strip())

def view_purchase_history(farmer_name):
    print(f"Purchase history for {farmer_name}:")
    with open("purchases.txt", "r",encoding="utf-8") as file:
        for line in file:
            f_name, item_type, item, quantity,price = line.strip().split(',')
            if f_name == farmer_name:
                print(f"Item: {item}, Quantity: {quantity} Price: {price}")


def weather_update():
    weather_conditions = ["Sunny", "Cloudy", "Rainy", "Windy"]
    temperature = random.randint(20, 40)  # Simulated temperature
    condition = random.choice(weather_conditions)
    print(f"Today's weather: {condition}, {temperature}°C")

def submit_feedback(farmer_name, item_name, feedback):
    with open("feedback.txt", "a") as file:
        file.write(f"{farmer_name},{item_name},{feedback}\n")
    print("Thank you for your feedback!")


def browse_fertilizers():
    with open("fertilizers.txt", "r") as file:
        for line in file:
            print(line.strip())

def browse_vehicles():
    with open("vehicles.txt", "r") as file:
        for line in file:
            print(line.strip())

def purchase_item(item_type, item_name, quantity, farmer_name,total_price):
    with open("purchases.txt", "a",encoding="utf-8") as file:
        file.write(f"{farmer_name},{item_type},{item_name},{quantity},₹{total_price}\n")
    print("Purchase recorded successfully.")

# Example location within a purchase processing function

def generate_payment_qr(upi_id, amount, transaction_note="Payment for goods"):
    """
    Generates a QR code for UPI payment.
    :param upi_id: The UPI ID of the recipient.
    :param amount: Amount to be paid.
    :param transaction_note: Optional note for the transaction.
    """
    # UPI payment URL format
    payment_url = f"upi://pay?pa={upi_id}&pn=Farm Supply&am={amount}&cu=INR&tn={transaction_note}"

    # Generate the QR code
    qr = qrcode.make(payment_url)
    qr.show()  # Display QR code for scanning
    qr.save("payment_qr.png")  # Save QR code image

    print("QR code generated and saved as payment_qr.png.")

# Usage example within the purchase process
def process_purchase(item_type, item_name, quantity):
    # Retrieve the total price (using previously defined calculate_price)
    file_map = {
        'seed': 'seeds.txt',
        'fertilizer': 'fertilizers.txt',
        'vehicle': 'vehicles.txt'
    }
    file_path = file_map.get(item_type.lower())
    if file_path:
        total_price = calculate_price(file_path, item_name, quantity)
        if total_price is not None:
            print(f"Total cost for {quantity} {item_name}(s): ₹{total_price}")
            # Generate QR for payment
            upi_id = "1236hetpatel@okaxis"  # Replace with actual UPI ID of the vendor
            generate_payment_qr(upi_id, total_price, f"Purchase of {item_name}")
        else:
            print("Item not found.")
    else:
        print("Invalid item type.")


def calculate_price(file_path, item_name, quantity):
    # Open the file with product details
    with open(file_path, 'r') as file:
        for line in file:
            data = line.strip().split(',')  # Split by commas to read parameters
            if data[0] == item_name:
                base_price = float(data[2])  # Assuming price is in the third position
                return base_price * quantity
    return None  # If item not found



# Vendor Functions

def add_product(product_type, name, price, description,base_quantity):
    filename = ""
    if product_type == "seed":
        filename = "seeds.txt"
    elif product_type == "fertilizer":
        filename = "fertilizers.txt"
    elif product_type == "vehicle":
        filename = "vehicles.txt"

    with open(filename, "a") as file:
        file.write(f"{name},{base_quantity},{price},({description})\n")
    print(f"{product_type.capitalize()} added successfully.")


# Support Functions

def submit_query(farmer_name, query):
    with open("queries.txt", "a") as file:
        file.write(f"{farmer_name},{query}\n")
    print("Query submitted successfully.")

def view_queries():
    with open("queries.txt", "r") as file:
        for line in file:
            print(line.strip())

# Registration and Login Functions

def register_user(user_type, username, password):
    with open("users.txt", "a") as file:
        file.write(f"{user_type},{username},{password}\n")
    print("Registration successful!")

def login_user(user_type, username, password):
    with open("users.txt", "r") as file:
        for line in file:
            u_type, u_name, u_pass = line.strip().split(',')
            if u_type == user_type and u_name == username and u_pass == password:
                print(f"Login successful as {user_type}!")
                return True
    print("Invalid credentials. Please try again.")
    return False

# Main Menu Function

def main_menu():
    print("Welcome to FarmEase!")
    print("Select your role:")
    print("1. Admin")
    print("2. Farmer")
    print("3. Vendor")
    role_choice = input("Enter choice (1-3): ")

    if role_choice == "1":
        user_type = "admin"
    elif role_choice == "2":
        user_type = "farmer"
    elif role_choice == "3":
        user_type = "vendor"
    else:
        print("Invalid choice. Exiting.")
        return

    print("1. Register")
    print("2. Login")
    action = input("Choose action (1-2): ")

    username = input("Enter username: ")
    password = input("Enter password: ")

    if action == "1":
        register_user(user_type, username, password)
        main_menu()

    elif action == "2":
        if login_user(user_type, username, password):
            if user_type == "admin":
                admin_menu()
            elif user_type == "farmer":
                farmer_menu()
            elif user_type == "vendor":
                vendor_menu()
    else:
        print("Invalid action selected.")


# Admin Menu

def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. View Users")
        print("2. Generate Report")
        print("3. View Queries")
        print("4. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            view_users()
        elif choice == "2":
            generate_report()
        elif choice == "3":
            view_queries()
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

# Farmer Menu

def farmer_menu():
    while True:
        print("\nFarmer Menu")
        print("1. Browse Seeds")
        print("2. Browse Fertilizers")
        print("3. Browse Vehicles")
        print("4. Weather Update")
        print("5. Purchase Item")
        print("6. Submit Feedback")
        print("7. Submit Query")
        print("8. View Purchase History")
        print("9. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            browse_seeds()
        elif choice == "2":
            browse_fertilizers()
        elif choice == "3":
            browse_vehicles()   
        elif choice == "4":
            weather_update()
        elif choice == "5":
            print("1. Purchase Seeds")
            print("2. Purchase Fertilizers")
            print("3. Purchase Vehicles")
            choice = input("Enter your choice: ")

            if choice == '1':
                item_type = "seed"
                item_name = input("Enter seed name: ")
                quantity = int(input("Enter quantity: "))
                process_purchase('seed', item_name, quantity)
            elif choice == '2':
                item_type = "fertilizer"
                item_name = input("Enter fertilizer name: ")
                quantity = int(input("Enter quantity: "))
                process_purchase('fertilizer', item_name, quantity)
            elif choice == '3':
                item_type = "vehicle"
                item_name = input("Enter vehicle name: ")
                quantity = int(input("Enter quantity: "))
                process_purchase('vehicle', item_name, quantity)
            else:
                print("Invalid choice.")
            # item_type = input("Enter item type (seed/fertilizer/vehicle): ")
            # item_name = input("Enter item name: ")
            # quantity = input("Enter quantity: ")
            farmer_name = input("Enter your name: ")
            file_map = {
            'seed': 'seeds.txt',
            'fertilizer': 'fertilizers.txt',
            'vehicle': 'vehicles.txt'
                }
            file_path = file_map.get(item_type.lower())
            total_price = calculate_price(file_path, item_name, quantity)
            purchase_item(item_type, item_name, quantity, farmer_name,total_price)
        elif choice == "6":
            farmer_name = input("Enter your name: ")
            item_name = input("Enter the item name for feedback: ")
            feedback = input("Enter your feedback: ")
            submit_feedback(farmer_name, item_name, feedback)
        elif choice == "7":
            query = input("Enter your query: ")
            submit_query(farmer_name, query)
        elif choice == "8":
            farmer_name = input("Enter your name: ")
            view_purchase_history(farmer_name)
        elif choice == "9":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

# Vendor Menu

def vendor_menu():
    while True:
        print("\nVendor Menu")
        print("1. Add Seed")
        print("2. Add Fertilizer")
        print("3. Add Vehicle")
        print("4. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter seed name: ")
            price = input("Enter price: ")
            description = input("Enter description: ")
            base_quantity=input("Enter base quantity: ")
            add_product("seed", name, price, description,base_quantity)
        elif choice == "2":
            name = input("Enter fertilizer name: ")
            price = input("Enter price: ")
            description = input("Enter description: ")
            base_quantity=input("Enter base quantity: ")
            add_product("fertilizer", name, price, description,base_quantity)
        elif choice == "3":
            name = input("Enter vehicle name: ")
            price = input("Enter price: ")
            description = input("Enter description: ")
            base_quantity=input("Enter base quantity: ")
            add_product("vehicle", name, price, description,base_quantity)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")



main_menu()