
# Australian Open Ticket Management System (AOTMS)
# MN404 T4 2025 Group Assignment 2 – FINAL VERSION

# --- User login data ---
users = {
    "root": "root"
}

# --- Ticket pricing: [standard, concession/kids] ---
ticket_prices = {
    "Ground Pass (Week 1)": [49, 25],
    "Ground Pass (Middle Weekend)": [69, 30],
    "Ground Pass (Week 2)": [139, 70],
    "Youth Ground Pass (Week 1)": [10, 10],
    "Youth Ground Pass (Week 2)": [5, 5],
    "Rod Laver Arena (Reserved)": [75, 37.5],
    "Margaret Court Arena (Reserved)": [65, 32.5],
    "John Cain Arena (Reserved)": [65, 32.5],
    "AO Live": [20, 10]
}

# --- General ticket inventory ---
ticket_inventory = {
    "Rod Laver Arena (Reserved)": 50,
    "Margaret Court Arena (Reserved)": 50,
    "John Cain Arena (Reserved)": 50,
    "AO Live": 10
}

# --- Special Rod Laver session inventory ---
rod_laver_special_inventory = {
    "Men’s Final": 6,
    "Women’s Final": 6,
    "Men’s Semi-Final": 6
}

# --- Valid concession types ---
valid_concession_types = [
    "Student Card",
    "Pensioner Concession Card",
    "Veteran Affairs/TPI",
    "Health Care Card",
    "Personal Treatment Entitlement Card"
]

# --- Login function ---
def login():
    print("\n--- AOTMS Login ---")
    user_id = input("User ID: ")
    password = input("Password: ")
    if user_id in users and users[user_id] == password:
        print("✅ Login successful!\n")
        return True
    else:
        print("❌ Invalid credentials.")
        sign_up = input("Have you signed up? (Y/N): ").upper()
        if sign_up == "Y":
            print("Please check credentials and try again.")
        else:
            print("Please sign up first.")
        return False

# --- Menu ---
def display_menu():
    print("\n--- AOTMS Menu ---")
    print("1. Calculate AO 2026 Ticket Price")
    print("2. Logout")

# --- Ticket price based on rules ---
def get_price(ticket_type, age, is_concession):
    if age < 3:
        return 0
    elif 3 <= age <= 11:
        return ticket_prices[ticket_type][1]
    elif 12 <= age <= 17:
        if "Youth" in ticket_type:
            return ticket_prices[ticket_type][0]
        else:
            return ticket_prices[ticket_type][1] if is_concession else ticket_prices[ticket_type][0]
    elif age >= 18 and is_concession:
        return ticket_prices[ticket_type][1]
    else:
        return ticket_prices[ticket_type][0]

# --- Ticket processing ---
def calculate_ticket():
    print("\n--- Available Ticket Types ---")
    for idx, t in enumerate(ticket_prices.keys(), start=1):
        print(f"{idx}. {t}")
    choice = int(input("Enter ticket type number: "))
    ticket_type = list(ticket_prices.keys())[choice - 1]

    # --- Session handling & limits ---
    session_name = None
    if ticket_type == "Rod Laver Arena (Reserved)":
        session = input("Is this for a Final or Semi-Final session? (Y/N): ").upper()
        if session == "Y":
            print("1. Men’s Final\n2. Women’s Final\n3. Men’s Semi-Final")
            session_map = {1: "Men’s Final", 2: "Women’s Final", 3: "Men’s Semi-Final"}
            sess_choice = int(input("Enter session type number: "))
            session_name = session_map.get(sess_choice)
            if session_name and rod_laver_special_inventory[session_name] > 0:
                max_limit = rod_laver_special_inventory[session_name]
                print(f"⚠️ Max {max_limit} tickets allowed for {session_name}")
            else:
                print("❌ Invalid session or no tickets left.")
                return
        else:
            max_limit = ticket_inventory[ticket_type]
    elif ticket_type == "John Cain Arena (Reserved)":
        date = int(input("Enter January date (12–20): "))
        if 12 <= date <= 20:
            max_limit = ticket_inventory[ticket_type]
        else:
            print("❌ Invalid date for John Cain Arena.")
            return
    elif ticket_type == "AO Live":
        date = int(input("Enter January date (23–25): "))
        if 23 <= date <= 25:
            max_limit = ticket_inventory[ticket_type]
        else:
            print("❌ Invalid date for AO Live.")
            return
    else:
        max_limit = ticket_inventory.get(ticket_type, 100)

    num_tickets = int(input(f"Enter number of tickets (max {max_limit}): "))
    if num_tickets > max_limit:
        print(f"❌ You cannot buy more than {max_limit} tickets.")
        return

    # --- Individual age input and validation ---
    total_price = 0
    individual_prices = []

    for i in range(num_tickets):
        print(f"\n--- Ticket {i+1} Details ---")
        age = int(input(f"Enter age of person {i+1}: "))

        is_concession = False
        concession_type = None

        if ticket_type in ["Youth Ground Pass (Week 1)", "Youth Ground Pass (Week 2)"]:
            if not (12 <= age <= 17):
                print(f"❌ Age {age} is NOT eligible for Youth Ground Pass (12–17 only).")
                return
            is_concession = False
            concession_type = "Not Applicable (Youth)"
        elif age >= 18 or (12 <= age <= 17 and ticket_type not in ["Youth Ground Pass (Week 1)", "Youth Ground Pass (Week 2)"]):
            has_card = input("Do you have a concession card? (Y/N): ").upper()
            if has_card == "Y":
                for idx, c in enumerate(valid_concession_types, 1):
                    print(f"{idx}. {c}")
                c_index = int(input("Enter card type number: "))
                if 1 <= c_index <= len(valid_concession_types):
                    is_concession = True
                    concession_type = valid_concession_types[c_index - 1]

        price = get_price(ticket_type, age, is_concession)
        individual_prices.append((age, is_concession, concession_type, price))
        total_price += price

    # --- Inventory update ---
    if ticket_type == "Rod Laver Arena (Reserved)" and session_name:
        rod_laver_special_inventory[session_name] -= num_tickets
    elif ticket_type in ticket_inventory:
        ticket_inventory[ticket_type] -= num_tickets

    # --- Ticket Summary ---
    print("\n--- Ticket Summary ---")
    print("\n  Ticketer Age \t | Concession \t  | Price ")
    for idx, (age, conc, ctype, price) in enumerate(individual_prices, 1):
        label = f"Concession: {ctype}" if conc else ("Not Applicable" if ctype else "Standard")
        print(f"Ticket {idx}: Age {age} | {label} | ${price:.2f}")
    print(f"\nTotal Price: ${total_price:.2f}")

    # Remaining ticket count
    if ticket_type == "Rod Laver Arena (Reserved)" and session_name:
        print(f"Tickets left for {session_name}: {rod_laver_special_inventory[session_name]}")
    elif ticket_type in ticket_inventory:
        print(f"Tickets left for {ticket_type}: {ticket_inventory[ticket_type]}")

# --- Main loop ---
def main():
    if login():
        while True:
            display_menu()
            option = input("Enter choice: ")
            if option == "1":
                calculate_ticket()
            elif option == "2":
                print("✅ You have been logged out. Goodbye!")
                break
            else:
                print("❌ Invalid option. Try again.")

# --- Run program ---
main()
