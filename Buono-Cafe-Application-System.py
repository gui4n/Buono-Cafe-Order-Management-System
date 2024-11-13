import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import deque
from datetime import datetime

# Coffee menu and prices
menu = {
    "Cold Brew Americano": 90.00,
    "Cold Brew Latte": 95.00,
    "Cold Brew Mocha": 110.00,
    "Cold Brew Caramel Machiato": 110.00,
    "Cold Brew BrownSugar Cinnamon": 110.00,
    "Cold Brew French Vanilla": 110.00
}

class CoffeeShop:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("Buono Cafe")  # Set the title of the window

        self.order = {}  # Initialize an empty dictionary to store the order
        self.delivery_queue = deque()  # Initialize an empty queue for delivery orders
        
        # Create the GUI elements
        self.create_widgets()

    def create_widgets(self):
        
        row = 0
        # Create labels for Coffee, Price, and Quantity at the top row
        tk.Label(self.root, text="Coffee", font=('Courier', 14)).grid(row=row, column=0, padx=10, pady=5)
        tk.Label(self.root, text="Price", font=('Courier', 14)).grid(row=row, column=1, padx=10, pady=5)
        tk.Label(self.root, text="Quantity", font=('Courier', 14)).grid(row=row, column=2, padx=10, pady=5)

        self.entries = {}  # Dictionary to store Entry widgets for each coffee
        row += 1

        # Create labels and entry fields for each coffee type in the menu
        for coffee, price in menu.items():
            tk.Label(self.root, text=coffee, font=('Courier', 12)).grid(row=row, column=0, padx=10, pady=5)
            tk.Label(self.root, text=f"PHP{price:.2f}", font=('Courier', 12)).grid(row=row, column=1, padx=10, pady=5)
            quantity = tk.Entry(self.root, width=5)  # Entry field for quantity
            quantity.grid(row=row, column=2, padx=10, pady=5)
            self.entries[coffee] = quantity  # Store the Entry widget in the dictionary
            row += 1

        # Create the buttons in a single row
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)

        tk.Button(button_frame, text="Generate Receipt", command=self.generate_receipt).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="New Order", command=self.new_order).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Order", command=self.delete_order).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Add to Delivery Queue", command=self.add_to_queue).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Process Next Delivery", command=self.process_next_delivery).grid(row=0, column=4, padx=5)
        tk.Button(button_frame, text="Show Delivery Queue", command=self.show_queue).grid(row=0, column=5, padx=5)

    def generate_receipt(self):
        # Reset the order dictionary
        self.order = {}
        
        # Iterate through the entries dictionary to collect user input
        for coffee, entry in self.entries.items():
            try:
                quantity = int(entry.get())  # Get the quantity entered by the user
                if quantity > 0:
                    self.order[coffee] = quantity  # Add valid entries to the order dictionary
            except ValueError:
                pass  # Ignore entries that are not valid integers

        # If no valid entries were made, show a warning message
        if not self.order:
            messagebox.showwarning("Invalid Order", "Please enter valid quantities for at least one coffee.")
            return
        
        # Call the method to display the receipt
        self.show_receipt()

    def show_receipt(self):
        # Create a new window (Toplevel) for displaying the receipt
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Receipt")  # Set the title of the receipt window

        # Create a ScrolledText widget to display the receipt content
        receipt_text = scrolledtext.ScrolledText(receipt_window, width=70, height=20, font=('Courier', 10))
        receipt_text.grid(row=0, column=0, padx=10, pady=10)

        total = 0.0  # Initialize the total cost accumulator
        receipt_content = "Coffee Shop Receipt\n\n"
        receipt_content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"  # Add date and time
        receipt_content += f"{'Item':<30}{'Qty':<5}{'Price':<10}{'Total':<10}\n"  # Header of the receipt
        receipt_content += "-"*55 + "\n"  # Separator line
        
        # Iterate through the items in the order dictionary to create receipt lines
        for coffee, quantity in self.order.items():
            price = menu[coffee]  # Get the price of the coffee from the menu dictionary
            line_total = price * quantity  # Calculate the total cost for this item
            total += line_total  # Add to the overall total
            # Format the receipt line and add it to the receipt content
            receipt_content += f"{coffee:<30}{quantity:<5}PHP{price:<9.2f}PHP{line_total:<9.2f}\n"
        
        receipt_content += "-"*55 + "\n"  # Separator line
        receipt_content += f"{'Total':<45}PHP{total:<.2f}\n"  # Total line
        
        # Insert the receipt content into the ScrolledText widget and disable editing
        receipt_text.insert(tk.END, receipt_content)
        receipt_text.config(state=tk.DISABLED)

    def new_order(self):
        # Clear all entry fields to start a new order
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def delete_order(self):
        # Clear the order dictionary and all entry fields
        self.order = {}
        self.new_order()
        messagebox.showinfo("Order Deleted", "The previous order has been deleted.")

    def add_to_queue(self):
        # Add the current order to the delivery queue with the current date and time
        if self.order:
            order_with_time = {
                "order": self.order.copy(),
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.delivery_queue.append(order_with_time)
            messagebox.showinfo("Order Added", "The order has been added to the delivery queue.")
            self.new_order()
        else:
            messagebox.showwarning("No Order", "There is no order to add to the queue.")

    def process_next_delivery(self):
        # Process the next order in the delivery queue
        if self.delivery_queue:
            next_order = self.delivery_queue.popleft()
            messagebox.showinfo("Next Delivery", f"Processing next delivery: {next_order['order']} (Time: {next_order['timestamp']})")
        else:
            messagebox.showinfo("Queue Empty", "There are no orders in the delivery queue.")

    def show_queue(self):
        # Display the current delivery queue
        if self.delivery_queue:
            queue_window = tk.Toplevel(self.root)
            queue_window.title("Delivery Queue")
            
            queue_text = scrolledtext.ScrolledText(queue_window, width=70, height=20, font=('Courier', 10))
            queue_text.grid(row=0, column=0, padx=10, pady=10)

            queue_content = "Current Delivery Queue\n\n"
            for idx, order in enumerate(self.delivery_queue, 1):
                queue_content += f"Order {idx} (Time: {order['timestamp']}):\n"
                for coffee, quantity in order['order'].items():
                    price = menu[coffee]
                    line_total = price * quantity
                    queue_content += f"  {coffee:<30}{quantity:<5}PHP{price:<9.2f}PHP{line_total:<9.2f}\n"
                queue_content += "-"*55 + "\n"

            queue_text.insert(tk.END, queue_content)
            queue_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Queue Empty", "There are no orders in the delivery queue.")

# Main program execution starts here
if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = CoffeeShop(root)  # Instantiate the CoffeeShop class with the main window
    root.mainloop()  # Start the main event loop to run the application
