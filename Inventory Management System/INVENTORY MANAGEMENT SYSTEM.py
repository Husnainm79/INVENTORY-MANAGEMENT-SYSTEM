import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from typing import List, Dict
import os

class Product:
    def __init__(self, product_id: int, name: str, category: str, price: float, quantity: int, reorder_level: int):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.reorder_level = reorder_level

    def update_quantity(self, amount: int):
        self.quantity += amount

    def check_reorder_level(self) -> bool:
        return self.quantity <= self.reorder_level

    def __str__(self):
        return f"{self.product_id},{self.name},{self.category},{self.price},{self.quantity},{self.reorder_level}"

class Supplier:
    def __init__(self, supplier_id: int, name: str, contact_info: str):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_info = contact_info
        self.products_supplied = []

    def add_product(self, product: Product):
        self.products_supplied.append(product)

    def update_contact_info(self, new_contact_info: str):
        self.contact_info = new_contact_info

    def get_supplied_products(self) -> List[Product]:
        return self.products_supplied

    def __str__(self):
        return f"{self.supplier_id},{self.name},{self.contact_info}"

class Order:
    def __init__(self, order_id: int, product: Product, quantity: int):
        self.order_id = order_id
        self.product = product
        self.quantity = quantity
        self.order_date = datetime.now()
        self.status = "Pending"
        self.total_price = self.calculate_total()

    def calculate_total(self) -> float:
        return self.product.price * self.quantity

    def update_status(self, new_status: str):
        self.status = new_status

    def get_order_details(self) -> Dict:
        return {
            "order_id": self.order_id,
            "product": self.product.name,
            "quantity": self.quantity,
            "order_date": self.order_date,
            "status": self.status,
            "total_price": self.total_price
        }

    def __str__(self):
        return f"{self.order_id},{self.product.product_id},{self.quantity},{self.order_date},{self.status},{self.total_price}"

class Inventory:
    def __init__(self):
        self.products = []
        self.suppliers = []
        self.orders = []
        self.load_data()

    def add_product(self, product: Product):
        self.products.append(product)
        self.save_data()

    def remove_product(self, product_id: int):
        self.products = [product for product in self.products if product.product_id != product_id]
        self.save_data()

    def update_product_quantity(self, product_id: int, amount: int):
        for product in self.products:
            if product.product_id == product_id:
                product.update_quantity(amount)
        self.save_data()

    def generate_stock_report(self):
        report = "Stock Report:\n"
        for product in self.products:
            report += str(product) + "\n"
        return report

    def add_supplier(self, supplier: Supplier):
        self.suppliers.append(supplier)
        self.save_data()

    def add_order(self, order: Order):
        self.orders.append(order)
        self.update_product_quantity(order.product.product_id, -order.quantity)
        self.save_data()

    def generate_report(self, report_type: str, date_range: tuple = None):
        if report_type == "stock":
            return self.generate_stock_report()
        # Additional report types can be implemented similarly

    def save_data(self):
        with open('IMSDB.txt', 'w') as f:
            f.write("Products\n")
            for product in self.products:
                f.write(str(product) + "\n")
            f.write("Suppliers\n")
            for supplier in self.suppliers:
                f.write(str(supplier) + "\n")
            f.write("Orders\n")
            for order in self.orders:
                f.write(str(order) + "\n")

    def load_data(self):
        if os.path.exists('IMSDB.txt'):
          
                with open('IMSDB.txt', 'r') as f:
                    lines = f.readlines()
                    section = None
                    for line in lines:
                        line = line.strip()
                        if line == "Products":
                            section = "Products"
                        elif line == "Suppliers":
                            section = "Suppliers"
                        elif line == "Orders":
                            section = "Orders"
                        elif line:
                            if section == "Products":
                                product_id, name, category, price, quantity, reorder_level = line.split(',')
                                product = Product(int(product_id), name, category, float(price), int(quantity), int(reorder_level))
                                self.products.append(product)
                            elif section == "Suppliers":
                                supplier_id, name, contact_info = line.split(',')
                                supplier = Supplier(int(supplier_id), name, contact_info)
                                self.suppliers.append(supplier)
                            elif section == "Orders":
                                order_id, product_id, quantity, order_date, status, total_price = line.split(',')
                                product = next((p for p in self.products if p.product_id == int(product_id)), None)
                                if product:
                                    order = Order(int(order_id), product, int(quantity))
                                    order.order_date = datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S.%f')
                                    order.status = status
                                    order.total_price = float(total_price)
                                    self.orders.append(order)

    def __str__(self):
        return f"Inventory with {len(self.products)} products, {len(self.suppliers)} suppliers, and {len(self.orders)} orders."

# GUI Implementation

class InventoryGUI:
    def __init__(self, root, inventory):
        self.root = root
        self.inventory = inventory
        self.root.title("Inventory Management System")

        self.main_menu = tk.Frame(self.root)
        self.main_menu.pack()

        self.create_main_menu()

    def create_main_menu(self):
        title = tk.Label(self.main_menu, text="Inventory Management System", font=("Helvetica", 16))
        title.pack(pady=10)

        add_product_btn = tk.Button(self.main_menu, text="Add Product", command=self.add_product_menu)
        add_product_btn.pack(pady=5)

        add_supplier_btn = tk.Button(self.main_menu, text="Add Supplier", command=self.add_supplier_menu)
        add_supplier_btn.pack(pady=5)

        add_order_btn = tk.Button(self.main_menu, text="Add Order", command=self.add_order_menu)
        add_order_btn.pack(pady=5)

        generate_report_btn = tk.Button(self.main_menu, text="Generate Stock Report", command=self.generate_report)
        generate_report_btn.pack(pady=5)

    def add_product_menu(self):
        self.clear_menu()

        self.product_form = tk.Frame(self.root)
        self.product_form.pack()

        tk.Label(self.product_form, text="Product ID").grid(row=0, column=0)
        self.product_id_entry = tk.Entry(self.product_form)
        self.product_id_entry.grid(row=0, column=1)

        tk.Label(self.product_form, text="Name").grid(row=1, column=0)
        self.product_name_entry = tk.Entry(self.product_form)
        self.product_name_entry.grid(row=1, column=1)

        tk.Label(self.product_form, text="Category").grid(row=2, column=0)
        self.product_category_entry = tk.Entry(self.product_form)
        self.product_category_entry.grid(row=2, column=1)

        tk.Label(self.product_form, text="Price").grid(row=3, column=0)
        self.product_price_entry = tk.Entry(self.product_form)
        self.product_price_entry.grid(row=3, column=1)

        tk.Label(self.product_form, text="Quantity").grid(row=4, column=0)
        self.product_quantity_entry = tk.Entry(self.product_form)
        self.product_quantity_entry.grid(row=4, column=1)

        tk.Label(self.product_form, text="Reorder Level").grid(row=5, column=0)
        self.product_reorder_level_entry = tk.Entry(self.product_form)
        self.product_reorder_level_entry.grid(row=5, column=1)

        submit_btn = tk.Button(self.product_form, text="Add Product", command=self.add_product)
        submit_btn.grid(row=6, columnspan=2, pady=10)

        back_btn = tk.Button(self.product_form, text="Back", command=self.back_to_main_menu)
        back_btn.grid(row=7, columnspan=2)

    def add_product(self):
        product_id = int(self.product_id_entry.get())
        name = self.product_name_entry.get()
        category = self.product_category_entry.get()
        price = float(self.product_price_entry.get())
        quantity = int(self.product_quantity_entry.get())
        reorder_level = int(self.product_reorder_level_entry.get())

        product = Product(product_id, name, category, price, quantity, reorder_level)
        self.inventory.add_product(product)

        messagebox.showinfo("Success", "Product added successfully")
        self.back_to_main_menu()

    def add_supplier_menu(self):
        self.clear_menu()

        self.supplier_form = tk.Frame(self.root)
        self.supplier_form.pack()

        tk.Label(self.supplier_form, text="Supplier ID").grid(row=0, column=0)
        self.supplier_id_entry = tk.Entry(self.supplier_form)
        self.supplier_id_entry.grid(row=0, column=1)

        tk.Label(self.supplier_form, text="Name").grid(row=1, column=0)
        self.supplier_name_entry = tk.Entry(self.supplier_form)
        self.supplier_name_entry.grid(row=1, column=1)

        tk.Label(self.supplier_form, text="Contact Info").grid(row=2, column=0)
        self.supplier_contact_entry = tk.Entry(self.supplier_form)
        self.supplier_contact_entry.grid(row=2, column=1)

        submit_btn = tk.Button(self.supplier_form, text="Add Supplier", command=self.add_supplier)
        submit_btn.grid(row=3, columnspan=2, pady=10)

        back_btn = tk.Button(self.supplier_form, text="Back", command=self.back_to_main_menu)
        back_btn.grid(row=4, columnspan=2)

    def add_supplier(self):
        supplier_id = int(self.supplier_id_entry.get())
        name = self.supplier_name_entry.get()
        contact_info = self.supplier_contact_entry.get()

        supplier = Supplier(supplier_id, name, contact_info)
        self.inventory.add_supplier(supplier)

        messagebox.showinfo("Success", "Supplier added successfully")
        self.back_to_main_menu()

    def add_order_menu(self):
        self.clear_menu()

        self.order_form = tk.Frame(self.root)
        self.order_form.pack()

        tk.Label(self.order_form, text="Order ID").grid(row=0, column=0)
        self.order_id_entry = tk.Entry(self.order_form)
        self.order_id_entry.grid(row=0, column=1)

        tk.Label(self.order_form, text="Product ID").grid(row=1, column=0)
        self.order_product_id_entry = tk.Entry(self.order_form)
        self.order_product_id_entry.grid(row=1, column=1)

        tk.Label(self.order_form, text="Quantity").grid(row=2, column=0)
        self.order_quantity_entry = tk.Entry(self.order_form)
        self.order_quantity_entry.grid(row=2, column=1)

        submit_btn = tk.Button(self.order_form, text="Add Order", command=self.add_order)
        submit_btn.grid(row=3, columnspan=2, pady=10)

        back_btn = tk.Button(self.order_form, text="Back", command=self.back_to_main_menu)
        back_btn.grid(row=4, columnspan=2)

    def add_order(self):
        order_id = int(self.order_id_entry.get())
        product_id = int(self.order_product_id_entry.get())
        quantity = int(self.order_quantity_entry.get())

        product = next((p for p in self.inventory.products if p.product_id == product_id), None)

        if product is None:
            messagebox.showerror("Error", "Product not found")
            return

        order = Order(order_id, product, quantity)
        self.inventory.add_order(order)

        messagebox.showinfo("Success", "Order added successfully")
        self.back_to_main_menu()

    def generate_report(self):
        report = self.inventory.generate_report("stock")
        messagebox.showinfo("Stock Report", report)

    def back_to_main_menu(self):
        self.clear_menu()
        self.main_menu.pack()

    def clear_menu(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    inventory = Inventory()
    root = tk.Tk()
    gui = InventoryGUI(root, inventory)
    root.mainloop()
