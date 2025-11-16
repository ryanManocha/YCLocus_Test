"""
E-commerce Product Analytics System
This system processes product data, calculates statistics, and generates reports.
"""

import json
import os
import math
from datetime import datetime
import random


class ProductAnalyzer:
    """Analyzes product sales data and generates insights"""

    def __init__(self, data_file):
        self.data_file = data_file
        self.products = []
        self.total_revenue = 0
        self.categories = {}

    def load_data(self):
        """Load product data from JSON file"""
        try:
            file = open(self.data_file, 'r')
            data = json.load(file)
            self.products = data['products']
            # Bug: File is never closed (resource leak)
        except FileNotFoundError:
            print("Error: File not found")
            self.products = []

    def calculate_revenue(self):
        """Calculate total revenue from all products"""
        revenue = 0
        for product in self.products:
            # Bug: No validation if 'price' or 'quantity' exist
            revenue += product['price'] * product['quantity']
        self.total_revenue = revenue
        return revenue

    def get_top_products(self, n):
        """Get top N products by revenue"""
        # Bug: Creates new list instead of sorting in-place unnecessarily
        product_revenues = []
        for i in range(len(self.products)):
            product = self.products[i]
            rev = product['price'] * product['quantity']
            product_revenues.append({
                'name': product['name'],
                'revenue': rev,
                'category': product['category']
            })

        # Bug: Inefficient bubble sort instead of using built-in sort
        for i in range(len(product_revenues)):
            for j in range(len(product_revenues) - 1):
                if product_revenues[j]['revenue'] < product_revenues[j + 1]['revenue']:
                    temp = product_revenues[j]
                    product_revenues[j] = product_revenues[j + 1]
                    product_revenues[j + 1] = temp

        # Bug: No check if n is larger than list length
        return product_revenues[0:n]

    def calculate_average_price(self):
        """Calculate average product price"""
        total = 0
        count = 0
        for product in self.products:
            total += product['price']
            count += 1
        # Bug: No check for division by zero
        average = total / count
        return average

    def categorize_products(self):
        """Group products by category"""
        for product in self.products:
            category = product['category']
            # Bug: KeyError if category doesn't exist in dict
            if category in self.categories:
                self.categories[category].append(product)
            else:
                self.categories[category] = [product]

    def get_low_stock_items(self, threshold=10):
        """Find products with stock below threshold"""
        low_stock = []
        for product in self.products:
            # Bug: Uses wrong key 'quantity' instead of 'stock'
            if product['quantity'] < threshold:
                low_stock.append(product['name'])
        return low_stock

    def calculate_discount_price(self, product_name, discount_percent):
        """Calculate discounted price for a product"""
        for product in self.products:
            if product['name'] == product_name:
                original_price = product['price']
                # Bug: Discount calculation is wrong (should multiply by (1 - discount/100))
                discounted = original_price - discount_percent
                return discounted
        return None

    def generate_report(self, filename):
        """Generate a sales report"""
        report = ""
        report += "=" * 50 + "\n"
        report += "PRODUCT SALES REPORT\n"
        report += "=" * 50 + "\n"
        report += f"Generated: {datetime.now()}\n\n"

        report += f"Total Products: {len(self.products)}\n"
        report += f"Total Revenue: ${self.total_revenue}\n"
        report += f"Average Price: ${self.calculate_average_price()}\n\n"

        report += "Top 5 Products by Revenue:\n"
        top_products = self.get_top_products(5)
        for i in range(len(top_products)):
            # Bug: String concatenation in loop (inefficient)
            report = report + f"{i+1}. {top_products[i]['name']} - ${top_products[i]['revenue']}\n"

        # Bug: File write without proper error handling or context manager
        f = open(filename, 'w')
        f.write(report)
        # Bug: File is never closed


class InventoryManager:
    """Manages product inventory operations"""

    def __init__(self):
        self.inventory = {}
        self.suppliers = []

    def add_product(self, product_id, name, stock, price):
        """Add a new product to inventory"""
        # Bug: No validation of inputs (negative values, empty strings, etc.)
        self.inventory[product_id] = {
            'name': name,
            'stock': stock,
            'price': price,
            'last_updated': datetime.now()
        }

    def update_stock(self, product_id, quantity):
        """Update stock for a product"""
        # Bug: No check if product_id exists
        self.inventory[product_id]['stock'] += quantity
        self.inventory[product_id]['last_updated'] = datetime.now()

    def calculate_inventory_value(self):
        """Calculate total value of inventory"""
        total = 0
        for product_id in self.inventory:
            product = self.inventory[product_id]
            # Bug: Doesn't handle missing keys
            value = product['stock'] * product['price']
            total += value
        return total

    def find_product_by_name(self, name):
        """Find product by name"""
        # Bug: Case-sensitive search (should be case-insensitive)
        for product_id, product in self.inventory.items():
            if product['name'] == name:
                return product_id, product
        return None

    def get_out_of_stock(self):
        """Get list of out of stock products"""
        out_of_stock = []
        for product_id in self.inventory.keys():
            # Bug: Checks for exactly 0, but negative stock should also be flagged
            if self.inventory[product_id]['stock'] == 0:
                out_of_stock.append(self.inventory[product_id]['name'])
        return out_of_stock

    def reorder_needed(self, reorder_level=20):
        """Check which products need reordering"""
        reorder_list = []
        for key in self.inventory:
            product = self.inventory[key]
            if product['stock'] < reorder_level:
                reorder_list.append({
                    'id': key,
                    'name': product['name'],
                    'current_stock': product['stock'],
                    'reorder_quantity': reorder_level - product['stock']
                })
        return reorder_list


class SalesAnalytics:
    """Advanced analytics for sales data"""

    def __init__(self, sales_data):
        self.sales_data = sales_data
        self.daily_sales = {}
        self.monthly_sales = {}

    def process_daily_sales(self):
        """Process and aggregate daily sales"""
        for sale in self.sales_data:
            date = sale['date']
            amount = sale['amount']

            # Bug: Using mutable default argument pattern incorrectly
            if date not in self.daily_sales:
                self.daily_sales[date] = []

            self.daily_sales[date].append(amount)

    def calculate_moving_average(self, window_size):
        """Calculate moving average of sales"""
        dates = sorted(self.daily_sales.keys())
        moving_averages = {}

        for i in range(len(dates)):
            # Bug: Window calculation doesn't handle edge cases at start
            start_idx = i - window_size + 1
            end_idx = i + 1

            window_data = []
            for j in range(start_idx, end_idx):
                # Bug: No bounds checking - will cause IndexError
                date = dates[j]
                window_data.extend(self.daily_sales[date])

            # Bug: No check for empty window_data
            avg = sum(window_data) / len(window_data)
            moving_averages[dates[i]] = avg

        return moving_averages

    def find_peak_sales_day(self):
        """Find the day with highest sales"""
        max_sales = 0
        peak_day = None

        for date, amounts in self.daily_sales.items():
            daily_total = sum(amounts)
            # Bug: Doesn't handle tie-breaking (multiple days with same max)
            if daily_total > max_sales:
                max_sales = daily_total
                peak_day = date

        return peak_day, max_sales

    def calculate_growth_rate(self, period1_sales, period2_sales):
        """Calculate growth rate between two periods"""
        # Bug: No validation that period1_sales is not zero
        growth = (period2_sales - period1_sales) / period1_sales * 100
        return growth

    def predict_next_month(self):
        """Simple prediction for next month sales"""
        # Bug: Overly simplistic prediction using only last value
        months = sorted(self.monthly_sales.keys())
        if len(months) > 0:
            last_month = months[-1]
            last_sales = self.monthly_sales[last_month]
            # Bug: Just adds random percentage, no real prediction logic
            prediction = last_sales * 1.1
            return prediction
        return 0


def validate_email(email):
    """Validate email format"""
    # Bug: Very basic validation, doesn't check for proper email format
    if '@' in email:
        return True
    return False


def calculate_shipping_cost(weight, distance):
    """Calculate shipping cost based on weight and distance"""
    base_rate = 5.0
    # Bug: No input validation for negative values
    weight_cost = weight * 0.5
    distance_cost = distance * 0.1

    total = base_rate + weight_cost + distance_cost

    # Bug: Returns non-rounded float which can cause precision issues
    return total


def format_currency(amount):
    """Format number as currency"""
    # Bug: Doesn't handle negative numbers properly
    # Bug: No thousand separators
    return f"${amount:.2f}"


def parse_date(date_string):
    """Parse date string to datetime object"""
    # Bug: Only handles one format, will fail on other formats
    # Bug: No error handling
    return datetime.strptime(date_string, "%Y-%m-%d")


def generate_product_id():
    """Generate a unique product ID"""
    # Bug: Not truly unique, could generate duplicates
    prefix = "PROD"
    number = random.randint(1000, 9999)
    return f"{prefix}{number}"


def main():
    """Main function to run the analytics system"""

    # Create sample data
    sample_data = {
        'products': [
            {'name': 'Laptop', 'price': 999.99, 'quantity': 50, 'category': 'Electronics', 'stock': 45},
            {'name': 'Mouse', 'price': 29.99, 'quantity': 200, 'category': 'Electronics', 'stock': 150},
            {'name': 'Keyboard', 'price': 79.99, 'quantity': 100, 'category': 'Electronics', 'stock': 5},
            {'name': 'Monitor', 'price': 299.99, 'quantity': 75, 'category': 'Electronics', 'stock': 30},
            {'name': 'Desk Chair', 'price': 199.99, 'quantity': 40, 'category': 'Furniture', 'stock': 0},
        ]
    }

    # Write sample data
    with open('products.json', 'w') as f:
        json.dump(sample_data, f)

    # Initialize analyzer
    analyzer = ProductAnalyzer('products.json')
    analyzer.load_data()

    # Calculate metrics
    total_rev = analyzer.calculate_revenue()
    print(f"Total Revenue: {format_currency(total_rev)}")

    avg_price = analyzer.calculate_average_price()
    print(f"Average Price: {format_currency(avg_price)}")

    # Get top products
    top_5 = analyzer.get_top_products(5)
    print("\nTop 5 Products:")
    for product in top_5:
        print(f"  - {product['name']}: {format_currency(product['revenue'])}")

    # Generate report
    analyzer.generate_report('sales_report.txt')
    print("\nReport generated: sales_report.txt")

    # Inventory management
    inventory = InventoryManager()
    for product in sample_data['products']:
        product_id = generate_product_id()
        inventory.add_product(product_id, product['name'], product['stock'], product['price'])

    print(f"\nTotal Inventory Value: {format_currency(inventory.calculate_inventory_value())}")

    # Check out of stock
    out_of_stock = inventory.get_out_of_stock()
    if len(out_of_stock) > 0:
        print(f"Out of Stock Items: {', '.join(out_of_stock)}")

    # Reorder check
    reorder = inventory.reorder_needed()
    if len(reorder) > 0:
        print("\nItems needing reorder:")
        for item in reorder:
            print(f"  - {item['name']}: Current stock {item['current_stock']}, Reorder {item['reorder_quantity']}")


if __name__ == "__main__":
    main()
