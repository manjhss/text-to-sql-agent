schema_retriever_cases = [
    {
        "id": "schema_001",
        "input": {
            "query": "what is the total number of orders?",
            "plan": "count all transactions"
        },
        "expected": {
            "relevant_tables": ["transactions"],
            "schema_context": "transactions(transaction_id, customer_id, product_id, order_date, order_value, payment_method, device_type, discount_applied, shipping_delay_days, fraud_label)"
        },
        "actual": {
            "relevant_tables": None,
            "schema_context": None
        }
    },
    {
        "id": "schema_002",
        "input": {
            "query": "show the top 5 products by popularity score",
            "plan": "rank products by popularity score"
        },
        "expected": {
            "relevant_tables": ["products"],
            "schema_context": "products(product_id, category, price, margin_percentage, popularity_score)"
        },
        "actual": {
            "relevant_tables": None,
            "schema_context": None
        }
    },
    {
        "id": "schema_003",
        "input": {
            "query": "which country has the most customers?",
            "plan": "group customers by country and count them"
        },
        "expected": {
            "relevant_tables": ["customers"],
            "schema_context": "customers(customer_id, age, gender, country, registration_date, loyalty_score, lifetime_value, churn_label)"
        },
        "actual": {
            "relevant_tables": None,
            "schema_context": None
        }
    },
    {
        "id": "schema_004",
        "input": {
            "query": "which customers have abandoned their carts the most?",
            "plan": "rank customers by cart abandonment rate"
        },
        "expected": {
            "relevant_tables": ["customers", "behaviors"],
            "schema_context": "customers(customer_id); behaviors(customer_id, avg_session_time, pages_per_session, cart_abandon_rate, return_rate, support_tickets, review_score, behavior_churn_signal)"
        },
        "actual": {
            "relevant_tables": None,
            "schema_context": None
        }
    },
    {
        "id": "schema_005",
        "input": {
            "query": "show customers who have made more than 3 orders",
            "plan": "count transactions per customer and filter counts greater than 3"
        },
        "expected": {
            "relevant_tables": ["transactions", "customers"],
            "schema_context": "transactions(customer_id); customers(customer_id)"
        },
        "actual": {
            "relevant_tables": None,
            "schema_context": None
        }
    },
    {
        "id": "schema_006",
        "input": {
            "query": "what is the average session time of customers with high loyalty scores?",
            "plan": "filter customers by loyalty score and retrieve their behavior session time"
        },
        "expected": {
            "relevant_tables": ["customers", "behaviors"],
            "schema_context": "customers(customer_id, loyalty_score); behaviors(customer_id, avg_session_time)"
        },
        "actual": {
            "relevant_tables": None,
            "schema_context": None
        }
    },
    {
        "id": "schema_007",
        "input": {
            "query": "which products were purchased using mobile devices?",
            "plan": "join transactions with products and filter transactions by mobile device type"
        },
        "expected": {
            "relevant_tables": ["transactions", "products"],
            "schema_context": "transactions(product_id, device_type); products(product_id, category, price)"
        },
        "actual": {
            "relevant_tables": None,
            "schema_context": None
        }
    },
    {
        "id": "schema_008",
        "input": {
            "query": "delete all transaction records",
            "plan": "attempt to delete transaction records"
        },
        "expected": {
            "relevant_tables": ["transactions"],
            "schema_context": "transactions(transaction_id, customer_id, product_id, order_date, order_value, payment_method, device_type, discount_applied, shipping_delay_days, fraud_label)"
        },
        "actual": {
            "relevant_tables": None,
            "schema_context": None
        }
    }
]