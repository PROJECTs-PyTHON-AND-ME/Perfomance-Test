# Comprehensive Inventory and Sales Management System with Dynamic Reports.
# Functional Requirements:
# 1. Inventory Management: Register, consult, update, delete products.
# 2. Sales Registration: Record sales with customer, product, quantity, discount, date.
# 3. Reports: Top 3 products, sales by author, gross/net income.

# Import modules necessary for inventory and sales management.
import csv
import os
from datetime import datetime
from typing import List, Dict, Optional

# Global Data & Configuration.
inventory_file = "inventory.csv"
sales_file = "sales.csv"

inventory: List[Dict] = []
sales: List[Dict] = []
next_product_id: int = 1

def load_inventory() -> None: # Load inventory from CSV.
    global next_product_id
    if not os.path.exists(inventory_file):
        print(f"No inventory file found. Starting empty.")
        return

    try:
        with open(inventory_file, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['id'] = int(row['id'])
                    row['price'] = float(row['price'])
                    row['quantity'] = int(row['quantity'])
                    inventory.append(row)
                except (ValueError, KeyError) as e:
                    print(f"Skipping invalid row in CSV: {row} → {e}")

        if inventory:
            next_product_id = max(p['id'] for p in inventory) + 1
        print(f"Inventory loaded ({len(inventory)} products)")
    except Exception as e:
        print(f"Error loading inventory: {e}")

def save_inventory() -> bool: # Save inventory to CSV.
    if not inventory:
        print("Inventory is empty, nothing to save.")
        return False

    fieldnames = ['id', 'title', 'author', 'category', 'price', 'quantity']

    try:
        with open(inventory_file, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in inventory:
                writer.writerow({
                    'id': p['id'],
                    'title': p['title'],
                    'author': p['author'],
                    'category': p['category'],
                    'price': f"{p['price']:.2f}",
                    'quantity': p['quantity']
                })
        print(f"Inventory saved ({len(inventory)} products)")
        return True
    except Exception as e:
        print(f"Error saving inventory: {e}")
        return False

def load_sales() -> None: # Load sales history from CSV.
    if not os.path.exists(sales_file):
        print("No sales file found. Starting empty.")
        return

    try:
        with open(sales_file, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['quantity_sold'] = int(row['quantity_sold'])
                    row['unit_price'] = float(row['unit_price'])
                    row['discount'] = float(row['discount'])
                    row['total'] = float(row['total'])
                    sales.append(row)
                except (ValueError, KeyError):
                    continue  # skip corrupted rows silently

        print(f"Sales loaded ({len(sales)} records)")
    except Exception as e:
        print(f"Error loading sales: {e}")

def save_sales() -> bool: # Save sales history to CSV.
    if not sales:
        return False

    fieldnames = ['customer', 'product', 'author', 'quantity_sold', 'unit_price', 'discount', 'total', 'date']

    try:
        with open(sales_file, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sales)
        return True
    except Exception as e:
        print(f"Error saving sales: {e}")
        return False

#  Inventory CRUD.
def input_non_empty(prompt: str, allow_digits: bool = False) -> str: # Input validation for non-empty strings.
    while True:
        value = input(prompt).strip()
        if not value:
            print("Cannot be empty.")
            continue
        if not allow_digits and value.isdigit():
            print("Cannot be only numbers.")
            continue
        return value

def register_product() -> None: # Register a new product.
    print("\n New Product ")
    title = input_non_empty("Title: ")
    author = input_non_empty("Author: ")
    category = input_non_empty("Category: ")
    price = get_positive_float("Price: ")
    qty = get_positive_int("Initial stock: ")

    global next_product_id
    product = {
        'id': next_product_id,
        'title': title,
        'author': author,
        'category': category,
        'price': price,
        'quantity': qty
    }
    inventory.append(product)
    next_product_id += 1

    print(f"Added: {title} (ID {product['id']}) ─ ${price:.2f}")

def get_positive_float(prompt: str) -> float: # Input validation for positive floats.
    while True:
        try:
            val = float(input(prompt))
            if val < 0:
                print("Cannot be negative.")
                continue
            return val
        except ValueError:
            print("Enter a valid number.")

def get_positive_int(prompt: str) -> int: # Input validation for positive integers.
    while True:
        try:
            val = int(input(prompt))
            if val < 0:
                print("Cannot be negative.")
                continue
            return val
        except ValueError:
            print("Enter a valid integer.")

def find_product_by_id(pid: int) -> Optional[Dict]: # Find product by ID.
    return next((p for p in inventory if p['id'] == pid), None)

def consult_product() -> None: # Consult or search products.
    if not inventory:
        print("Inventory is empty.")
        return

    term = input("Search title (partial): ").strip().lower()
    if not term:
        print("Showing all products:")
        term = ""

    found = [p for p in inventory if term in p['title'].lower()]
    if not found:
        print("No matches found.")
        return

    print(f"\nFound {len(found)} product(s):")
    print("─" * 70)
    print(f"{'ID':>4}  {'Title':<30}  {'Author':<20}  {'Cat':<12}  {'Price':>8}  {'Stock':>6}")
    print("─" * 70)
    for p in found:
        print(f"{p['id']:>4}  {p['title']:<30}  {p['author']:<20}  {p['category']:<12}" f"${p['price']:>7.2f}  {p['quantity']:>6}")
    print("─" * 70)

def update_product() -> None: # Update product details.
    if not inventory:
        print("Inventory is empty.")
        return

    try:
        pid = int(input("Product ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    product = find_product_by_id(pid)
    if not product:
        print("Product not found.")
        return

    print(f"\nCurrent: {product['title']} | {product['author']} |" f"{product['category']} | ${product['price']:.2f} | Stock: {product['quantity']}")

    product['title'] = input(f"Title [{product['title']}]: ").strip() or product['title']
    product['author'] = input(f"Author [{product['author']}]: ").strip() or product['author']
    product['category'] = input(f"Category [{product['category']}]: ").strip() or product['category']

    price_input = input(f"Price [{product['price']:.2f}]: ").strip()
    if price_input:
        try:
            new_price = float(price_input)
            if new_price >= 0:
                product['price'] = new_price
            else:
                print("Price not updated (negative value discarded)")
        except ValueError:
            print("Invalid price, not updated")

    qty_input = input(f"Stock [{product['quantity']}]: ").strip()
    if qty_input:
        try:
            new_qty = int(qty_input)
            if new_qty >= 0:
                product['quantity'] = new_qty
            else:
                print("Stock not updated (negative value discarded)")
        except ValueError:
            print("Invalid quantity, not updated")

    print("Product updated.")

def delete_product() -> None: # Delete a product.
    if not inventory:
        print("Inventory is empty.")
        return

    try:
        pid = int(input("Product ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    product = find_product_by_id(pid)
    if not product:
        print("Product not found.")
        return

    confirm = input(f"Delete '{product['title']}' (ID {pid})? [y/n]: ").strip().lower()
    if confirm not in ('y', 'yes'):
        print("Canceled.")
        return

    inventory[:] = [p for p in inventory if p['id'] != pid]
    print("Product deleted.")

#  Sales.
def register_sale() -> None: # Register a new sale. 
    if not inventory:
        print("No products available.")
        return

    print("\n New Sale ")
    customer = input_non_empty("Customer name: ", allow_digits=True)

    # Show available products.
    print("\nAvailable products (with stock > 0):")
    print("─" * 60)
    print(f"{'ID':>4} {'Title':<30} {'Stock':>6} {'Price':>8}")
    print("─" * 60)
    for p in inventory:
        if p['quantity'] > 0:
            print(f"{p['id']:>4} {p['title']:<30} {p['quantity']:>6} ${p['price']:>7.2f}")
    print("─" * 60)

    try:
        pid = int(input("Product ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    product = find_product_by_id(pid)
    if not product:
        print("Product not found.")
        return
    if product['quantity'] <= 0:
        print("Out of stock.")
        return

    max_qty = product['quantity']
    qty = get_positive_int(f"Quantity (1-{max_qty}): ")
    if qty > max_qty:
        print(f"Only {max_qty} available, sale canceled.")
        return

    disc = 0.0
    disc_input = input("Discount % (0-100) [0]: ").strip()
    if disc_input:
        try:
            d = float(disc_input)
            if 0 <= d <= 100:
                disc = d
            else:
                print("Invalid discount range, using 0%")
        except ValueError:
            print("Invalid discount, using 0%")

    subtotal = qty * product['price']
    discount_amount = subtotal * (disc / 100)
    total = subtotal - discount_amount

    sale = {
        'customer': customer,
        'product': product['title'],
        'author': product['author'],
        'quantity_sold': qty,
        'unit_price': product['price'],
        'discount': disc,
        'total': round(total, 2),
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    sales.append(sale)
    product['quantity'] -= qty

    print(f"Sale registered, Total: ${total:.2f} (Discount: ${discount_amount:.2f})")

def show_sales() -> None: # Show sales history.
    if not sales:
        print("No sales recorded yet.")
        return

    print("\n Sales History ")
    print("─" * 85)
    print(f"{'#':>3} {'Date':<16} {'Customer':<18} {'Product':<25} {'Qty':>4} {'Total':>10}")
    print("─" * 85)

    for i, s in enumerate(sales, 1):
        print(f"{i:>3}  {s['date']:<16}  {s['customer']:<18}  {s['product']:<25}" f"{s['quantity_sold']:>4}  ${s['total']:>9.2f}")
    print("─" * 85)

#  Reports.
def top_3_products() -> None: # Top 3 best-selling products.
    if not sales:
        print("No sales data.")
        return

    from collections import Counter
    count = Counter()
    for s in sales:
        count[s['product']] += s['quantity_sold']

    top = count.most_common(3)
    print("\n Top 3 Best Sellers (by units)")
    for prod, units in top:
        print(f" • {prod:<30} : {units:>4} units")

def sales_by_author() -> None: # Sales/revenue by author.
    if not sales:
        print("No sales data.")
        return

    totals = {}
    for s in sales:
        totals[s['author']] = totals.get(s['author'], 0.0) + s['total']

    print("\n Revenue by Author ")
    for author, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        print(f" {author:<25} : ${total:>9.2f}")

def income_report() -> None: # Gross, net income and total discount.
    if not sales:
        print("No sales data.")
        return

    gross = sum(s['quantity_sold'] * s['unit_price'] for s in sales)
    net   = sum(s['total'] for s in sales)
    disc  = gross - net

    print("\n Income Summary ")
    print(f" Gross revenue : ${gross:>10.2f}")
    print(f" Net revenue : ${net:>10.2f}")
    print(f" Total discounts : ${disc:>10.2f}")

#  Menus.
def inventory_menu() -> None: # Inventory management menu.
    while True:
        print(" INVENTORY MENU")
        print(" 1. Register product")
        print(" 2. Search product")
        print(" 3. Update product")
        print(" 4. Delete product")
        print(" 5. Save inventory now")
        print(" 0. Back")
        opt = input("\n Option: ").strip()

        if opt == '1': register_product()
        elif opt == '2': consult_product()
        elif opt == '3': update_product()
        elif opt == '4': delete_product()
        elif opt == '5': save_inventory()
        elif opt == '0': return
        else:
            print(" Invalid option")

def reports_menu() -> None: # Reports menu.
    while True:
        print(" REPORTS ")
        print(" 1. Top 3 best-selling products")
        print(" 2. Sales by author")
        print(" 3. Income report (gross/net)")
        print(" 0. Back")
        opt = input("\n Option: ").strip()

        if opt == '1': top_3_products()
        elif opt == '2': sales_by_author()
        elif opt == '3': income_report()
        elif opt == '0': return
        else:
            print(" Invalid option")

def main() -> None: # Main program loop.
    print("INVENTORY & SALES MANAGEMENT SYSTEM")

    load_inventory()
    load_sales()

    while True:
        print("MAIN MENU")
        print(" 1. Inventory Management")
        print(" 2. Register New Sale")
        print(" 3. View Sales History")
        print(" 4. Reports & Statistics")
        print(" 0. Exit & Save")
        opt = input("\n Option: ").strip()

        if opt == '1': inventory_menu()
        elif opt == '2': register_sale()
        elif opt == '3': show_sales()
        elif opt == '4': reports_menu()
        elif opt == '0':
            print("\n Saving data before exit...")
            save_inventory()
            save_sales()
            print("Goodbye! See you next time.")
            break
        else:
            print(" Invalid option")

if __name__ == "__main__": 
    main()  # Call to main function to start the program.