"""
Run with: python seed_data.py
Populates the database with sample categories and products.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product

categories_data = [
    ('Electronics', 'Phones, laptops, gadgets and accessories'),
    ('Clothing', 'Men and women fashion'),
    ('Books', 'Fiction, non-fiction and educational books'),
    ('Home & Kitchen', 'Furniture, appliances and kitchen tools'),
    ('Sports', 'Fitness equipment and outdoor gear'),
]

print("Creating categories...")
categories = {}
for name, desc in categories_data:
    cat, created = Category.objects.get_or_create(name=name, defaults={'description': desc})
    categories[name] = cat
    print(f"  {'Created' if created else 'Exists'}: {name}")

products_data = [
    ('iPhone 15 Pro', 'Latest Apple smartphone with titanium design', 1199.99, 'Electronics', 25),
    ('Samsung Galaxy S24', 'Flagship Android phone with AI features', 999.99, 'Electronics', 30),
    ('MacBook Air M3', '13-inch laptop with Apple Silicon chip', 1299.99, 'Electronics', 15),
    ('Sony WH-1000XM5', 'Industry-leading noise cancelling headphones', 349.99, 'Electronics', 40),
    ('iPad Pro 12.9"', 'Powerful tablet for creative professionals', 1099.99, 'Electronics', 20),
    ("Men's Classic T-Shirt", 'Premium cotton everyday t-shirt', 29.99, 'Clothing', 100),
    ("Women's Slim Jeans", 'Comfortable stretch denim jeans', 59.99, 'Clothing', 80),
    ('Running Sneakers', 'Lightweight and breathable running shoes', 89.99, 'Clothing', 60),
    ('Winter Jacket', 'Warm and stylish jacket for cold weather', 149.99, 'Clothing', 45),
    ('The Great Gatsby', 'Classic novel by F. Scott Fitzgerald', 12.99, 'Books', 200),
    ('Atomic Habits', 'Build good habits and break bad ones', 16.99, 'Books', 150),
    ('Python Crash Course', 'Hands-on introduction to programming', 39.99, 'Books', 75),
    ('Coffee Maker', 'Programmable drip coffee maker 12-cup', 79.99, 'Home & Kitchen', 35),
    ('Air Fryer 5.8QT', 'Large capacity digital air fryer', 89.99, 'Home & Kitchen', 50),
    ('Yoga Mat', 'Non-slip premium yoga and exercise mat', 34.99, 'Sports', 90),
    ('Dumbbell Set', 'Adjustable dumbbell set 5-50 lbs', 299.99, 'Sports', 20),
]

print("\nCreating products...")
for name, desc, price, cat_name, stock in products_data:
    p, created = Product.objects.get_or_create(
        name=name,
        defaults={
            'description': desc,
            'price': price,
            'category': categories[cat_name],
            'stock': stock,
        }
    )
    print(f"  {'Created' if created else 'Exists'}: {name}")

print(f"\nDone! {Category.objects.count()} categories, {Product.objects.count()} products.")
