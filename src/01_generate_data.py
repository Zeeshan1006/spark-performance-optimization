import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# -----------------------------
# Configuration
# -----------------------------
NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 500
NUM_ORDERS = 5000

# Output files
CUSTOMERS_FILE = "customers.csv"
PRODUCTS_FILE = "products.csv"
ORDERS_FILE = "orders.csv"


# -----------------------------
# Product data
# -----------------------------
CATEGORIES = {
    "Electronics": [
        "Smartphone", "Laptop", "Tablet", "Headphones",
        "Smartwatch", "Keyboard", "Mouse", "Monitor"
    ],
    "Clothing": [
        "T-Shirt", "Jeans", "Jacket", "Sneakers",
        "Dress", "Hoodie", "Shirt", "Socks"
    ],
    "Home & Kitchen": [
        "Coffee Maker", "Blender", "Cookware Set",
        "Bedsheet", "Lamp", "Chair", "Storage Box"
    ],
    "Books": [
        "Novel", "Biography", "Science Book",
        "Business Book", "Self-Help Book", "History Book"
    ],
    "Beauty": [
        "Face Wash", "Moisturizer", "Shampoo",
        "Perfume", "Lipstick", "Sunscreen"
    ],
    "Sports": [
        "Running Shoes", "Yoga Mat", "Football",
        "Cricket Bat", "Dumbbells", "Tennis Racket"
    ]
}

BRANDS = [
    "Nova", "UrbanX", "TechPro", "Prime",
    "Apex", "Zenith", "Vertex", "Elite",
    "Fusion", "Evergreen"
]


# -----------------------------
# Generate Customers
# -----------------------------
def generate_customers():
    customers = []

    for customer_id in range(1, NUM_CUSTOMERS + 1):
        customers.append({
            "customer_id": customer_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "phone": fake.phone_number(),
            "city": fake.city(),
            "state": fake.state(),
            "country": "India",
            "postal_code": fake.postcode(),
            "registration_date": (
                datetime.now() -
                timedelta(days=random.randint(1, 1500))
            ).date()
        })

    with open(CUSTOMERS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=customers[0].keys()
        )
        writer.writeheader()
        writer.writerows(customers)

    return customers


# -----------------------------
# Generate Products
# -----------------------------
def generate_products():
    products = []

    for product_id in range(1, NUM_PRODUCTS + 1):
        category = random.choice(list(CATEGORIES.keys()))
        product_type = random.choice(CATEGORIES[category])
        brand = random.choice(BRANDS)

        price = round(random.uniform(199, 100000), 2)

        products.append({
            "product_id": product_id,
            "product_name": f"{brand} {product_type}",
            "category": category,
            "brand": brand,
            "price": price,
            "stock_quantity": random.randint(0, 500),
            "rating": round(random.uniform(2.5, 5.0), 1),
            "review_count": random.randint(0, 5000),
            "is_active": random.choice([True, True, True, False]),
            "created_date": (
                datetime.now() -
                timedelta(days=random.randint(1, 1000))
            ).date()
        })

    with open(PRODUCTS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=products[0].keys()
        )
        writer.writeheader()
        writer.writerows(products)

    return products


# -----------------------------
# Generate Orders
# -----------------------------
def generate_orders(customers, products):
    orders = []

    payment_methods = [
        "Credit Card",
        "Debit Card",
        "UPI",
        "Net Banking",
        "Cash on Delivery",
        "Wallet"
    ]

    order_statuses = [
        "Delivered",
        "Delivered",
        "Delivered",
        "Shipped",
        "Processing",
        "Cancelled",
        "Returned"
    ]

    for order_id in range(1, NUM_ORDERS + 1):

        customer = random.choice(customers)

        # Select 1–5 products for the order
        order_products = random.sample(
            products,
            random.randint(1, 5)
        )

        order_date = (
            datetime.now() -
            timedelta(days=random.randint(0, 730))
        )

        status = random.choice(order_statuses)

        for product in order_products:
            quantity = random.randint(1, 4)

            unit_price = product["price"]

            discount = random.choice([
                0, 0, 0, 5, 10, 15, 20
            ])

            discounted_price = round(
                unit_price * (1 - discount / 100),
                2
            )

            total_amount = round(
                discounted_price * quantity,
                2
            )

            orders.append({
                "order_id": order_id,
                "customer_id": customer["customer_id"],
                "product_id": product["product_id"],
                "order_date": order_date.date(),
                "quantity": quantity,
                "unit_price": unit_price,
                "discount_percent": discount,
                "total_amount": total_amount,
                "payment_method": random.choice(payment_methods),
                "order_status": status
            })

    with open(ORDERS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=orders[0].keys()
        )
        writer.writeheader()
        writer.writerows(orders)

    return orders


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    print("Generating customers...")
    customers = generate_customers()

    print("Generating products...")
    products = generate_products()

    print("Generating orders...")
    orders = generate_orders(customers, products)

    print("\nDataset generated successfully!")
    print(f"Customers : {CUSTOMERS_FILE}")
    print(f"Products  : {PRODUCTS_FILE}")
    print(f"Orders    : {ORDERS_FILE}")

    print("\nRecord counts:")
    print(f"Customers : {len(customers)}")
    print(f"Products  : {len(products)}")
    print(f"Order rows: {len(orders)}")
