"""
E-commerce Product Analytics System (Improved Version)
Cleaned, optimized, validated, and bug-fixed.
"""

import json
import os
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
        """Load product data safely"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            self.products = data.get('products', [])
        except Exception as e:
            print(f"Error loading data: {e}")
            self.products = []

    def calculate_revenue(self):
        """Calculate total revenue from all products."""
        self.total_revenue = sum(
            p.get('price', 0) * p.get('quantity', 0)
            for p in self.products
        )
        return self.total_revenue

    def get_top_products(self, n):
        """Return top N products by revenue."""
        product_revenues = [
            {
                'name': p.get('name'),
                'revenue': p.get('price', 0) * p.get('quantity', 0),
                'category': p.get('category')
            }
            for p in self.products
        ]

        product_revenues.sort(key=lambda x: x['revenue'], reverse=True)
        return product_revenues[:n]

    def calculate_average_price(self):
        """Calculate the average product price safely."""
        prices = [p.get('price', 0) for p in self.products]
        if not prices:
            return 0
        return sum(prices) / len(prices)

    def categorize_products(self):
        """Group products by category."""
        self.categories = {}
        for p in self.products:
            self.categories.setdefault(p.get('category', 'Unknown'), []).append(p)

    def get_low_stock_items(self, threshold=10):
        """Return items where stock < threshold."""
        return [
            p.get('name')
            for p in self.products
            if p.get('stock', 0) < threshold
        ]

    def calculate_discount_price(self, product_name, discount_percent):
        """Calculate discounted price correctly."""
        for p in self.products:
            if p.get('name') == product_name:
                original = p.get('price', 0)
                return original * (1 - discount_percent / 100)
        return None

    def generate_report(self, filename):
        """Generate a clean sales report."""
        try:
            top_products = self.get_top_products(5)
            avg_price = self.calculate_average_price()

            report_lines = [
                "="*50,
                "PRODUCT SALES REPORT",
                "="*50,
                f"Generated: {datetime.now()}",
                "",
                f"Total Products: {len(self.products)}",
                f"Total Revenue: ${self.total_revenue:.2f}",
                f"Average Price: ${avg_price:.2f}",
                "",
                "Top 5 Products by Revenue:"
            ]

            for i, p in enumerate(top_products, 1):
                report_lines.append(f"{i}. {p['name']} - ${p['revenue']:.2f}")

            with open(filename, "w") as f:
                f.write("\n".join(report_lines))

        except Exception as e:
            print(f"Error generating report: {e}")


class InventoryManager:
    """Manages product inventory operations."""

    def __init__(self):
        self.inventory = {}

    def add_product(self, product_id, name, stock, price):
        if stock < 0 or price < 0:
            raise ValueError("Invalid stock or price.")
        self.inventory[product_id] = {
            'name': name,
            'stock': stock,
            'price': price,
            'last_updated': datetime.now()
        }

    def update_stock(self, product_id, quantity):
        if product_id not in self.inventory:
            raise KeyError("Product not found.")
        self.inventory[product_id]['stock'] += quantity
        self.inventory[product_id]['last_updated'] = datetime.now()

    def calculate_inventory_value(self):
        return sum(
            p['stock'] * p['price']
            for p in self.inventory.values()
        )

    def find_product_by_name(self, name):
        name = name.lower()
        for pid, p in self.inventory.items():
            if p['name'].lower() == name:
                return pid, p
        return None

    def get_out_of_stock(self):
        return [
            p['name']
            for p in self.inventory.values()
            if p['stock'] <= 0
        ]

    def reorder_needed(self, reorder_level=20):
        return [
            {
                'id': pid,
                'name': p['name'],
                'current_stock': p['stock'],
                'reorder_quantity': max(0, reorder_level - p['stock'])
            }
            for pid, p in self.inventory.items()
            if p['stock'] < reorder_level
        ]


class SalesAnalytics:
    """Sales analytics and forecasting."""

    def __init__(self, sales_data):
        self.sales_data = sales_data
        self.daily_sales = {}
        self.monthly_sales = {}

    def process_daily_sales(self):
        for sale in self.sales_data:
            date = sale.get('date')
            amount = sale.get('amount', 0)
            self.daily_sales.setdefault(date, []).append(amount)

    def calculate_moving_average(self, window_size):
        dates = sorted(self.daily_sales.keys())
        moving_averages = {}

        for i in range(len(dates)):
            start = max(0, i - window_size + 1)
            window = []
            for j in range(start, i + 1):
                window.extend(self.daily_sales[dates[j]])

            moving_averages[dates[i]] = sum(window) / len(window)
        return moving_averages

    def find_peak_sales_day(self):
        peak_day = max(self.daily_sales, key=lambda d: sum(self.daily_sales[d]), default=None)
        if peak_day:
            return peak_day, sum(self.daily_sales[peak_day])
        return None, 0

    def calculate_growth_rate(self, p1, p2):
        if p1 == 0:
            return float('inf')
        return (p2 - p1) / p1 * 100

    def predict_next_month(self):
        if not self.monthly_sales:
            return 0
        last_month = max(self.monthly_sales)
        return self.monthly_sales[last_month] * 1.1  # simple forecast


def validate_email(email):
    return "@" in email and "." in email.split("@")[-1]


def calculate_shipping_cost(weight, distance):
    if weight < 0 or distance < 0:
        raise ValueError("Invalid weight/distance.")
    return round(5 + weight * 0.5 + distance * 0.1, 2)


def format_currency(amount):
    return f"${amount:,.2f}"


def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except Exception:
        return None


def generate_product_id():
    return f"PROD{random.randint(10000, 99999)}"
