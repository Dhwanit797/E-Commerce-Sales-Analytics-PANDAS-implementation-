import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# ---------------- CUSTOMERS ----------------
num_customers = 300
cities = ["Ahmedabad", "Delhi", "Mumbai", "Bangalore", "Pune"]

customer_ids = [f"CUST{str(i).zfill(3)}" for i in range(1, num_customers + 1)]

signup_dates = [
    datetime.now() - timedelta(days=np.random.randint(30, 730))
    for _ in range(num_customers)
]

customers = pd.DataFrame({
    "customer_id": customer_ids,
    "city": np.random.choice(cities, num_customers, p=[0.2, 0.25, 0.25, 0.2, 0.1]),
    "signup_date": signup_dates,
    "is_premium": np.random.choice(["Yes", "No"], num_customers, p=[0.25, 0.75])
})

customers.to_csv("customers.csv", index=False)

# ---------------- ORDERS ----------------
num_orders = 2000
categories = {
    "Electronics": (20000, 80000),
    "Fashion": (500, 5000),
    "Grocery": (100, 2000),
    "Home": (1000, 15000)
}

orders = []

for i in range(1, num_orders + 1):
    cust = customers.sample(1).iloc[0]
    category = np.random.choice(list(categories.keys()))
    price_range = categories[category]

    order = {
        "order_id": f"ORD{str(i).zfill(4)}",
        "customer_id": cust["customer_id"],
        "product_id": f"PROD{np.random.randint(1, 200):03}",
        "category": category,
        "quantity": np.random.randint(1, 6),
        "price": np.random.randint(*price_range),
        "discount_pct": np.random.choice([0, 5, 10, 20, 30]),
        "order_date": cust["signup_date"] + timedelta(days=np.random.randint(1, 400)),
        "delivery_days": np.random.randint(2, 10),
        "payment_mode": np.random.choice(["UPI", "Card", "COD"], p=[0.5, 0.3, 0.2])
    }

    orders.append(order)

orders_df = pd.DataFrame(orders)
orders_df.to_csv("orders.csv", index=False)

print("Datasets generated successfully.")