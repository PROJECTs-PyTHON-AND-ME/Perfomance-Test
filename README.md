# Inventory & Sales Management System.

A comprehensive Python-based application for managing inventory and sales operations with dynamic reporting capabilities.

## Overview.

This project is a **Performance Test** for the Python Data Science course. It implements a fully functional inventory and sales management system with persistent data storage using CSV files.
The system provides a menu-driven interface for managing products, recording sales, and generating various business reports.


## Features.

### Inventory Management.

| Feature | Description |
|---------|-------------|
| **Register Product** | Add new products with title, author, category, price, and initial stock |
| **Search Product** | Find products by title (partial match search) |
| **Update Product** | Modify any product details (title, author, category, price, stock) |
| **Delete Product** | Remove products from inventory with confirmation |
| **Save Inventory** | Manually save inventory changes to CSV file |

### Sales Management

| Feature | Description |
|---------|-------------|
| **Register Sale** | Record new sales with customer name, product, quantity, and optional discount |
| **View Sales History** | Display complete sales log with all transaction details |
| **Automatic Stock Update** | Inventory quantities decrease automatically with each sale |
| **Discount Support** | Apply percentage-based discounts (0-100%) to sales |

### Reports & Statistics.

| Report | Description |
|--------|-------------|
| **Top 3 Best Sellers** | Shows the 3 most sold products by units |
| **Sales by Author** | Displays revenue breakdown by product author |
| **Income Summary** | Shows gross revenue, net revenue, and total discounts given |

---

## Installation.

1. **Ensure you have Python 3.x installed**
   ```bash
   python --version
   ```

2. **No additional dependencies required**
   - Uses only Python standard library modules:
     - `csv` - CSV file handling
     - `os` - Operating system interface
     - `datetime` - Date/time operations
     - `typing` - Type hints

3. **Run the application**
   ```bash
   python inventory.py
   ```

---

## Usage.

### Main Menu Options.

```
MAIN MENU
 1. Inventory Management
 2. Register New Sale
 3. View Sales History
 4. Reports & Statistics
 0. Exit & Save
```

### Navigation.

1. **Select an option** by entering the corresponding number.
2. **Follow the prompts** displayed on the screen.
3. **Data is automatically saved** when exiting (option 0).
4. **Manual save** is available in the inventory menu (option 5).

---

## Data Files.

### inventory.csv.

Stores product information with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Unique product identifier |
| `title` | String | Product name/title |
| `author` | String | Product author/creator |
| `category` | String | Product category/type |
| `price` | Float | Unit price |
| `quantity` | Integer | Current stock level |

### sales.csv.

Stores sales transaction records with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `customer` | String | Customer name |
| `product` | String | Product purchased |
| `author` | String | Product author |
| `quantity_sold` | Integer | Units sold |
| `unit_price` | Float | Price per unit at time of sale |
| `discount` | Float | Discount percentage applied |
| `total` | Float | Final sale total |
| `date` | DateTime | Timestamp of the sale |

---

## Sample Data.

### Products (inventory.csv).

| ID | Title | Author | Category | Price | Quantity |
|----|-------|--------|----------|-------|----------|
| 1 | milk | Klim | dairy | $2.50 | 98 |
| 2 | bread | Wonder | bakery | $1.50 | 200 |
| 3 | apple | Granny Smith | fruit | $5.00 | 150 |
| 4 | cheese | Cheddar | dairy | $8.00 | 80 |
| 5 | banana | Cavendish | fruit | $3.00 | 120 |
| 6 | Book | Gabriel | book | $100.00 | 28 |

### Sales Records (sales.csv).

| Customer | Product | Author | Qty | Unit Price | Discount | Total | Date |
|----------|---------|--------|-----|------------|----------|-------|------|
| Juan | milk | Klim | 2 | $2.50 | 0% | $5.00 | 2026-02-01 17:13:31 |
| Juan | Book | Gabriel | 2 | $100.00 | 50% | $100.00 | 2026-02-01 17:15:42 |

---
## Project Structure.

```
PyTHON DS/Performance Test/
├── inventory.py      # Main application file with all functionality
├── inventory.csv     # Product inventory data file
├── sales.csv         # Sales records data file
└── README.md         # This documentation file
```
---
