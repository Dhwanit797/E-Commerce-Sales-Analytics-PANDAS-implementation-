import pandas as pd

# ---------------- Load Data ----------------
customers_df = pd.read_csv("customers.csv")
orders_df = pd.read_csv("orders.csv")

# ---------------- Merge ----------------
df = pd.merge(customers_df, orders_df, on="customer_id")

# ---------------- Derived Columns ----------------
df["gross_amount"] = df["quantity"] * df["price"]
df["discount_amount"] = df["gross_amount"] * (df["discount_pct"] / 100)
df["net_amount"] = df["gross_amount"] - df["discount_amount"]

df["order_date"] = pd.to_datetime(df["order_date"])
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

df["is_late_delivery"] = df["delivery_days"] > 5

# ---------------- Revenue Metrics ----------------
total_revenue = df["net_amount"].sum()

category_wise_revenue = (
    df.groupby("category", as_index=False)["net_amount"]
    .sum()
    .sort_values(by="net_amount", ascending=False)
)

month_wise_revenue = (
    df.groupby("order_month", as_index=False)["net_amount"]
    .sum()
    .sort_values(by="order_month")
)

avg_order_value = (
    df.groupby("category", as_index=False)["net_amount"]
    .mean()
    .rename(columns={"net_amount": "avg_order_value"})
    .sort_values(by="avg_order_value", ascending=False)
)

revenue_report = pd.merge(
    category_wise_revenue,
    avg_order_value,
    on="category"
)

# ---------------- Customer Analytics ----------------
repeat_customers = (
    df.groupby("customer_id")
    .size()
    .reset_index(name="order_count")
)

repeat_customers = repeat_customers[repeat_customers["order_count"] > 1]

customer_spend = (
    df.groupby("customer_id", as_index=False)["net_amount"]
    .sum()
    .sort_values(by="net_amount", ascending=False)
)

top_5_pct = int(len(customer_spend) * 0.05)
top_customers = customer_spend.head(top_5_pct)

premium_revenue = (
    df.groupby("is_premium", as_index=False)["net_amount"]
    .agg(
        total_revenue="sum",
        avg_order_value="mean",
        order_count="count"
    )
)

# ---------------- Delivery & Risk Analysis ----------------
late_delivery_rate = df["is_late_delivery"].mean() * 100

avg_delivery_time_category = (
    df.groupby("category", as_index=False)["delivery_days"]
    .mean()
    .sort_values(by="delivery_days", ascending=False)
)

city_delay_rate = (
    df.groupby("city", as_index=False)["is_late_delivery"]
    .mean()
    .sort_values(by="is_late_delivery", ascending=False)
)

payment_risk = (
    df.groupby("payment_mode", as_index=False)["is_late_delivery"]
    .sum()
    .sort_values(by="is_late_delivery", ascending=False)
)

# ---------------- Export Reports ----------------
revenue_report.to_csv("revenue_report.csv", index=False)
month_wise_revenue.to_csv("monthly_report.csv", index=False)
repeat_customers.to_csv("repeat_customers.csv", index=False)
top_customers.to_csv("top_customers.csv", index=False)
premium_revenue.to_csv("premium_revenue.csv", index=False)

avg_delivery_time_category.to_csv("delivery_by_category.csv", index=False)
city_delay_rate.to_csv("city_delay.csv", index=False)
payment_risk.to_csv("payment_risk.csv", index=False)