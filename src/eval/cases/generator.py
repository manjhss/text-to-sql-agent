generator_cases = [
    {
        "id": "generator_001",
        "input": {
            "query": "what is the total number of orders?",
            "plan": "count all transactions",
            "schema_context": "transactions(transaction_id, customer_id, product_id, order_date, order_value, payment_method, device_type, discount_applied, shipping_delay_days, fraud_label)"
        },
        "expected": {
            "raw_sql": "SELECT COUNT(transaction_id) FROM transactions;"
        },
        "actual": {
            "raw_sql": None
        }
    },
    {
        "id": "generator_002",
        "input": {
            "query": "show the top 5 products by popularity score",
            "plan": "rank products by popularity score descending and return top 5",
            "schema_context": "products(product_id, category, price, margin_percentage, popularity_score)"
        },
        "expected": {
            "raw_sql": "SELECT product_id, category, popularity_score FROM products ORDER BY popularity_score DESC LIMIT 5;"
        },
        "actual": {
            "raw_sql": None
        }
    },
    {
        "id": "generator_003",
        "input": {
            "query": "what is the average order value?",
            "plan": "calculate average order value",
            "schema_context": "transactions(order_value)"
        },
        "expected": {
            "raw_sql": "SELECT AVG(order_value) FROM transactions;"
        },
        "actual": {
            "raw_sql": None
        }
    },
    {
        "id": "generator_004",
        "input": {
            "query": "which country has the most customers?",
            "plan": "group customers by country and count them",
            "schema_context": "customers(customer_id, country)"
        },
        "expected": {
            "raw_sql": "SELECT country, COUNT(customer_id) AS customer_count FROM customers GROUP BY country ORDER BY customer_count DESC LIMIT 1;"
        },
        "actual": {
            "raw_sql": None
        }
    },
    {
        "id": "generator_005",
        "input": {
            "query": "show customers who have made more than 3 orders",
            "plan": "count transactions per customer and filter counts greater than 3",
            "schema_context": "transactions(customer_id)"
        },
        "expected": {
            "raw_sql": "SELECT customer_id, COUNT(transaction_id) AS order_count FROM transactions GROUP BY customer_id HAVING COUNT(transaction_id) > 3;"
        },
        "actual": {
            "raw_sql": None
        }
    },
    {
        "id": "generator_006",
        "input": {
            "query": "what is the average session time of customers with high loyalty scores?",
            "plan": "join customers and behaviors and calculate average session time for high loyalty customers",
            "schema_context": "customers(customer_id, loyalty_score); behaviors(customer_id, avg_session_time)"
        },
        "expected": {
            "raw_sql": "SELECT AVG(b.avg_session_time) FROM customers c JOIN behaviors b ON c.customer_id = b.customer_id WHERE c.loyalty_score > 0.8;"
        },
        "actual": {
            "raw_sql": None
        }
    },
    {
        "id": "generator_007",
        "input": {
            "query": "which products were purchased using mobile devices?",
            "plan": "join transactions with products and filter mobile transactions",
            "schema_context": "transactions(product_id, device_type); products(product_id, category, price)"
        },
        "expected": {
            "raw_sql": "SELECT DISTINCT p.product_id, p.category FROM products p JOIN transactions t ON p.product_id = t.product_id WHERE t.device_type = 'mobile';"
        },
        "actual": {
            "raw_sql": None
        }
    },
    {
        "id": "generator_008",
        "input": {
            "query": "delete all transaction records",
            "plan": "attempt to delete transaction records",
            "schema_context": "transactions(transaction_id, customer_id, product_id, order_date, order_value, payment_method, device_type, discount_applied, shipping_delay_days, fraud_label)"
        },
        "expected": {
            "raw_sql": None
        },
        "actual": {
            "raw_sql": None
        }
    }
]