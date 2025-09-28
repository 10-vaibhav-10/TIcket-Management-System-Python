import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

class AOTMS_GUI:
    def __init__(self, root):
        self.root = root
        self.session_var = tk.StringVar(value="Men's Final")
        self.root.title("Australian Open Ticket Management System")
        self.root.geometry("650x600")
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', padding=5, font=('Arial', 10))
        
        # User accounts
        self.users = {"admin": "root"}  # Default account
        self.current_user = None
        self.ticket_details = []
        
        # Ticket prices [Standard, Concession]
        self.ticket_prices = {
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
        
        # ACTUAL RUNTIME INVENTORY (changes during program)
        self.current_inventory = {
            "Rod Laver Arena (Reserved)": 50,
            "Ground Pass (Week 1)": 100,
            "Ground Pass (Middle Weekend)": 100,
            "Ground Pass (Week 2)": 100,
            "Youth Ground Pass (Week 1)": 100,
            "Youth Ground Pass (Week 2)": 100,
            "Men's Final": 6,
            "Women's Final": 6,
            "Men's Semi-Final": 6,
            "Margaret Court Arena (Reserved)": 50,
            "John Cain Arena (Reserved)": 50,
            "AO Live": 10,
            # Ground Passes have unlimited inventory (not tracked)
        }
        
        self.valid_concession_types = [
            "Student Card (under 30 only)",
            "Pensioner Concession Card (60+ only)",
            "Veteran Affairs/TPI",
            "Health Care Card",
            "Personal Treatment Entitlement Card"
        ]
        
        self.create_login_screen()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_login_screen(self):
        self.clear_frame()
        self.current_user = None
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(pady=(0, 20))
        tk.Label(header_frame, text="Australian Open Ticket Management System", 
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Login form
        login_frame = ttk.LabelFrame(main_frame, text="User Login", padding=20)
        login_frame.pack(fill=tk.X, padx=50, pady=20)
        
        ttk.Label(login_frame, text="User ID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.user_id_entry = ttk.Entry(login_frame)
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Login", command=self.attempt_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Footer
        tk.Label(main_frame, text="© 2025 MIT - MN404 Group Assignment", 
                font=("Arial", 8), bg="#f0f0f0").pack(side=tk.BOTTOM, pady=10)
    
    def attempt_login(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        
        if user_id in self.users and self.users[user_id] == password:
            self.current_user = user_id
            self.create_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
    
    def create_main_menu(self):
        self.clear_frame()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(header_frame, text="Australian Open Ticket Management System", 
                font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Menu buttons
        menu_frame = ttk.Frame(main_frame)
        menu_frame.pack(pady=20)
        ttk.Button(menu_frame, text="Get AO 2026 Ticket", 
                  command=self.create_ticket_calculator, width=30).pack(pady=10)
        ttk.Button(menu_frame, text="Logout", command=self.create_login_screen).pack(pady=20)
        
        # Footer
        tk.Label(main_frame, text="© 2025 MIT - MN404 Group Assignment", 
                font=("Arial", 8), bg="#f0f0f0").pack(side=tk.BOTTOM, pady=10)
    
    def create_ticket_calculator(self):
        self.clear_frame()
        self.ticket_details = []
        self.show_summary = False
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Customer name
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        ttk.Label(name_frame, text="Customer Name:").pack(side=tk.LEFT, padx=5)
        self.customer_name = ttk.Entry(name_frame)
        self.customer_name.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Button(header_frame, text="← Back to Menu", command=self.create_main_menu).pack(side=tk.LEFT)
        tk.Label(header_frame, text="Ticket Price Calculator", 
                font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Main content
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Ticket selection
        self.left_frame = ttk.LabelFrame(content_frame, text="Ticket Information", padding=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(self.left_frame, text="Select Ticket Type:").pack(anchor="w", pady=(0, 5))
        self.ticket_type_var = tk.StringVar()
        self.ticket_type_cb = ttk.Combobox(self.left_frame, textvariable=self.ticket_type_var, 
                                         values=list(self.ticket_prices.keys()), state="readonly")
        self.ticket_type_cb.pack(fill=tk.X, pady=(0, 10))
        self.ticket_type_cb.current(0)
        self.ticket_type_cb.bind("<<ComboboxSelected>>", self.update_ticket_limits)
        
        # Special session frame (Rod Laver)
        self.special_session_frame = ttk.Frame(self.left_frame)
        self.special_session_var = tk.StringVar(value="N")
        
        # Date frame
        self.date_frame = ttk.Frame(self.left_frame)
        
        # Quantity
        ttk.Label(self.left_frame, text="Number of Tickets:").pack(anchor="w", pady=(0, 5))
        self.quantity_var = tk.IntVar(value=1)
        self.quantity_spin = ttk.Spinbox(self.left_frame, from_=1, to=100, textvariable=self.quantity_var)
        self.quantity_spin.pack(fill=tk.X, pady=(0, 10))
        
        # Remaining tickets display
        self.limit_label = ttk.Label(self.left_frame, text="Remaining: ", foreground="blue")
        self.limit_label.pack(anchor="w", pady=(0, 10))
        
        # Add tickets button
        ttk.Button(self.left_frame, text="Add Ticket Details", command=self.add_ticket_details).pack(pady=10)
        
        # Middle panel - Ticket details
        self.middle_frame = ttk.LabelFrame(content_frame, text="Ticket Details", padding=10)
        self.middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        
        
        # Scrollable details area
        details_container = ttk.Frame(self.middle_frame)
        details_container.pack(fill=tk.BOTH, expand=True)
        self.details_canvas = tk.Canvas(details_container)
        self.details_scrollbar = ttk.Scrollbar(details_container, orient="vertical", command=self.details_canvas.yview)
        self.details_canvas.configure(yscrollcommand=self.details_scrollbar.set)
        self.details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.details_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.details_frame = ttk.Frame(self.details_canvas)
        self.details_canvas.create_window((0, 0), window=self.details_frame, anchor="nw")
        self.details_frame.bind("<Configure>", lambda e: self.details_canvas.configure(scrollregion=self.details_canvas.bbox("all")))
        
        # Action buttons
        self.total_price_button = ttk.Button(self.middle_frame, text="Calculate Total Price", command=self.toggle_calculation_view)
        self.total_price_button.pack(pady=15)
        self.clear_details_button = ttk.Button(self.middle_frame, text="Clear All Tickets", command=self.clear_ticket_details)
        self.clear_details_button.pack(padx=5)

        
        def go_back_and_clear():
            self.clear_ticket_details()
            self.create_main_menu()  

        # Right panel - Order summary (hidden initially)
            self.right_frame = ttk.LabelFrame(content_frame, text="Order Summary", padding=10)
        self.right_frame.pack_forget()
        self.summary_text = ScrolledText(self.right_frame, height=10, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        self.summary_text.config(state=tk.DISABLED)
        ttk.Button(self.right_frame, text="Go Back to Ticket Purchase",command=go_back_and_clear).pack(pady=10)
        
        self.update_ticket_limits()
    
    def update_ticket_limits(self, event=None):
        """Update REAL-TIME remaining ticket display"""
        ticket_type = self.ticket_type_var.get()
        
        # Get remaining tickets (default 100 for unlimited types)
        remaining = self._get_remaining_tickets(ticket_type)
        
        # Special handling for Rod Laver
        if ticket_type == "Rod Laver Arena (Reserved)" and hasattr(self, 'session_var'):
            session = self.session_var.get()
            session_remaining = self.current_inventory.get(session, 6)
            remaining = min(remaining, session_remaining)
        
        # Update UI
        color = "green" if remaining > 5 else ("orange" if remaining > 0 else "red")
        self.limit_label.config(text=f"Remaining: {remaining}", foreground=color)
        self.quantity_spin.config(to=max(1, remaining))  # Ensure at least 1
        
        # Disable if sold out
        if remaining <= 0:
            self.ticket_type_cb.config(state="disabled")
            self.quantity_spin.config(state="disabled")
            
            # Specific message for Rod Laver special sessions
            if ticket_type == "Rod Laver Arena (Reserved)":
                session = self.session_var.get()
                messagebox.showinfo("Sold Out", f"No more tickets available for {session}")
            else:
                messagebox.showinfo("Sold Out", f"No more {ticket_type} tickets available")

        else:
            self.ticket_type_cb.config(state="readonly")
            self.quantity_spin.config(state="normal")
        
        # Handle date fields
        for widget in self.special_session_frame.winfo_children():
            widget.destroy()
        self.special_session_frame.pack_forget()
        
        for widget in self.date_frame.winfo_children():
            widget.destroy()
        self.date_frame.pack_forget()
        
        if ticket_type == "Rod Laver Arena (Reserved)":
            self.special_session_frame.pack(fill=tk.X, pady=(0, 10))
            ttk.Label(self.special_session_frame, text="Select Special Session:").pack(anchor="w", pady=(5, 0))
            
            # session_var already initialized
            self.special_session_menu = ttk.Combobox(
                self.special_session_frame,
                textvariable=self.session_var,
                values=["Men's Final", "Women's Final", "Men's Semi-Final"],
                state="readonly"
            )
            self.special_session_menu.pack(fill=tk.X)

            if self.session_var.get() not in self.special_session_menu['values']:
                self.session_var.set("Men's Final")
        
        elif ticket_type == "John Cain Arena (Reserved)":
            self.date_frame.pack(fill=tk.X, pady=(0, 10))
            ttk.Label(self.date_frame, text="Enter January date (12-20):").pack(anchor="w")
            self.john_cain_date = ttk.Spinbox(self.date_frame, from_=12, to=20)
            self.john_cain_date.pack(fill=tk.X)
        
        elif ticket_type == "AO Live":
            self.date_frame.pack(fill=tk.X, pady=(0, 10))
            ttk.Label(self.date_frame, text="Enter January date (23-25):").pack(anchor="w")
            self.ao_live_date = ttk.Spinbox(self.date_frame, from_=23, to=25)
            self.ao_live_date.pack(fill=tk.X)
    
    def _get_remaining_tickets(self, ticket_type, session=None):
        """Get actual remaining tickets from inventory"""
        remaining = self.current_inventory.get(ticket_type, 100)  # Default 100 for unlimited
        
        if ticket_type == "Rod Laver Arena (Reserved)" and session:
            remaining = min(remaining, self.current_inventory.get(session, 6))
        
        return remaining
    
    def _update_inventory(self, ticket_type, quantity, session=None):
        """Reduce inventory when tickets are booked"""
        if ticket_type in self.current_inventory:
            self.current_inventory[ticket_type] = max(0, self.current_inventory[ticket_type] - quantity)
        
        if session and session in self.current_inventory:
            self.current_inventory[session] = max(0, self.current_inventory[session] - quantity)
    
    def add_ticket_details(self):
        """Add tickets after validating inventory"""
        ticket_type = self.ticket_type_var.get()
        if not ticket_type:
            messagebox.showerror("Error", "Please select a ticket type")
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError
            
            # Check Rod Laver special session
            session = None
            if ticket_type == "Rod Laver Arena (Reserved)":
                session = self.session_var.get()
            
            # Check remaining tickets
            remaining = self._get_remaining_tickets(ticket_type, session)
            if quantity > remaining:
                messagebox.showerror("Error", 
                    f"Only {remaining} tickets remaining for {ticket_type}")
                return
            
            # Validate dates
            if ticket_type == "John Cain Arena (Reserved)":
                try:
                    date = int(self.john_cain_date.get())
                    if not 12 <= date <= 20:
                        raise ValueError
                except:
                    messagebox.showerror("Error", "Invalid date (12-20 Jan) for John Cain Arena")
                    return
            
            if ticket_type == "AO Live":
                try:
                    date = int(self.ao_live_date.get())
                    if not 23 <= date <= 25:
                        raise ValueError
                except:
                    messagebox.showerror("Error", "Invalid date (23-25 Jan) for AO Live")
                    return
            
            # DEDUCT FROM INVENTORY
            # Inventory update moved to validate_and_calculate
            
            # Clear previous and add new tickets
            for widget in self.details_frame.winfo_children():
                widget.destroy()
            self.ticket_details = []
            
            for i in range(quantity):
                self.create_ticket_detail_entry(ticket_type, i+1)
            
            # Refresh UI
            self.update_ticket_limits()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid ticket quantity")
    
    def create_ticket_detail_entry(self, ticket_type, ticket_num):
        """Create UI for individual ticket details"""
        detail_frame = ttk.LabelFrame(self.details_frame, text=f"Ticket {ticket_num}: {ticket_type}", padding=10)
        detail_frame.pack(fill=tk.X, pady=5)
        
        # Age input
        ttk.Label(detail_frame, text="Age:").grid(row=0, column=0, sticky="e", padx=5)
        age_var = tk.StringVar()
        age_spin = ttk.Spinbox(detail_frame, from_=1, to=120, textvariable=age_var)
        age_spin.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Concession section
        concession_frame = ttk.Frame(detail_frame)
        concession_var = tk.BooleanVar()
        concession_type_var = tk.StringVar()
        
        def update_concession_display():
            try:
                age = int(age_var.get()) if age_var.get() else 0
                if age >= 18 or (12 <= age <= 17 and "Youth" not in ticket_type):
                    concession_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
                else:
                    concession_frame.grid_forget()
                    concession_var.set(False)
            except: pass
        
        age_var.trace_add("write", lambda *args: update_concession_display())
        
        ttk.Checkbutton(concession_frame, text="Has concession card:", 
                       variable=concession_var).pack(side=tk.LEFT, padx=5)
        
        concession_cb = ttk.Combobox(concession_frame, textvariable=concession_type_var, 
                                    values=self.valid_concession_types, state="readonly")
        concession_cb.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        def validate_concession(*args):
            if not concession_var.get(): return
            concession_type = concession_type_var.get()
            try:
                age = int(age_var.get()) if age_var.get() else 0
                if "Student Card" in concession_type and age >= 30:
                    concession_type_var.set("")
                if "Pensioner Concession Card" in concession_type and age < 60:
                    concession_type_var.set("")
            except: pass
        
        concession_type_var.trace_add("write", validate_concession)
        
        # Store ticket data
        self.ticket_details.append({
            "frame": detail_frame,
            "ticket_type": ticket_type,
            "age_var": age_var,
            "concession_var": concession_var,
            "concession_type_var": concession_type_var,
            "ticket_num": ticket_num
        })
        
        update_concession_display()
    
    def validate_and_calculate(self):
        """Calculate total price with validation"""
        if not self.ticket_details:
            messagebox.showerror("Error", "No ticket details added")
            return False
        
        customer_name = self.customer_name.get().strip()
        if not customer_name:
            messagebox.showerror("Error", "Please enter your name")
            return False
        
        total_price = 0
        summary_lines = [f"Customer: {customer_name}\n=== Ticket Details ==="]
        
        for ticket in self.ticket_details:
            try:
                age_str = ticket["age_var"].get()
                if not age_str:
                    messagebox.showerror("Error", f"Enter age for Ticket {ticket['ticket_num']}")
                    return False
                
                age = int(age_str)
                ticket_type = ticket["ticket_type"]
                is_concession = ticket["concession_var"].get()
                concession_type = ticket["concession_type_var"].get()
                
                # Validate Youth tickets
                if "Youth Ground Pass" in ticket_type and not 12 <= age <= 17:
                    messagebox.showerror("Error", f"Youth tickets require age 12-17")
                    return False
                
                # Validate concessions
                if is_concession and not concession_type:
                    messagebox.showerror("Error", "Select concession type")
                    return False
                
                if is_concession:
                    if "Student Card" in concession_type and age >= 30:
                        messagebox.showerror("Error", "Student cards only for under 30")
                        return False
                    if "Pensioner Concession Card" in concession_type and age < 60:
                        messagebox.showerror("Error", "Pensioner cards only for 60+")
                        return False
                
                # Calculate price
                if age < 3:
                    price = 0
                    price_category = "Free (under 3)"
                elif 3 <= age <= 11:
                    price = self.ticket_prices[ticket_type][1]
                    price_category = "Child"
                elif 12 <= age <= 17:
                    if "Youth" in ticket_type:
                        price = self.ticket_prices[ticket_type][0]
                        price_category = "Youth"
                    else:
                        price = self.ticket_prices[ticket_type][1] if is_concession else self.ticket_prices[ticket_type][0]
                        price_category = f"Youth {'Concession' if is_concession else 'Standard'}"
                else:
                    price = self.ticket_prices[ticket_type][1] if is_concession else self.ticket_prices[ticket_type][0]
                    price_category = f"{'Concession' if is_concession else 'Standard'}"
                
                summary_lines.append(
                    f"Ticket {ticket['ticket_num']}: {ticket_type}\n"
                    f"  Age: {age} | Category: {price_category} | Price: ${price:.2f}\n"
                )
                
                total_price += price
                
            except ValueError:
                messagebox.showerror("Error", f"Invalid age for Ticket {ticket['ticket_num']}")
                return False
        
        # Update summary
        self.summary_text.config(state=tk.NORMAL)

        summary_lines = [f"Customer: {customer_name}\n=== Ticket Details ==="]
        for ticket in self.ticket_details:
            summary_lines.append(
                f"Ticket {ticket['ticket_num']}: {ticket_type}\n"
                f"  Age: {age} | Category: {price_category} | Price: ${price:.2f}"
            )
        summary_lines.append(f"\nTotal Price: ${total_price:.2f}")
        self.summary_text.insert(tk.END, "\n".join(summary_lines))  # Display in GUI

        # Update inventory after successful validation
        for ticket in self.ticket_details:
            session = self.session_var.get() if ticket["ticket_type"] == "Rod Laver Arena (Reserved)" else None
            self._update_inventory(ticket["ticket_type"], 1, session)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, "\n".join(summary_lines))
        self.summary_text.insert(tk.END, f"\n\nTotal Price: ${total_price:.2f}")
        self.summary_text.config(state=tk.DISABLED)
        
        return True
    
    
    def toggle_calculation_view(self):
        """Switch between ticket entry and summary views"""
        if self.show_summary:
            self.show_summary = False
            self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
            self.middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.right_frame.pack_forget()
        else:
            if self.validate_and_calculate():
                self.show_summary = True
                self.left_frame.pack_forget()
                self.middle_frame.pack_forget()
                self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def clear_ticket_details(self):
        """Reset all ticket entries"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        self.ticket_details = []
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AOTMS_GUI(root)
    root.mainloop()