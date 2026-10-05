validate_execute_cases = [
    {
        "id": "validate_001",
        "input": {
            "raw_sql": "SELECT COUNT(transaction_id) FROM transactions;"
        },
        "expected": {
            "query_result": "<actual DB result>",
            "error": None,
            "should_retry": False
        },
        "actual": {
            "query_result": None,
            "error": None,
            "should_retry": None
        }
    },
    {
        "id": "validate_002",
        "input": {
            "raw_sql": "SELECT AVG(order_value) FROM transactions;"
        },
        "expected": {
            "query_result": "<actual DB result>",
            "error": None,
            "should_retry": False
        },
        "actual": {
            "query_result": None,
            "error": None,
            "should_retry": None
        }
    },
    {
        "id": "validate_003",
        "input": {
            "raw_sql": "SELECT COUNT(*) FROM customers;"
        },
        "expected": {
            "query_result": "<actual DB result>",
            "error": None,
            "should_retry": False
        },
        "actual": {
            "query_result": None,
            "error": None,
            "should_retry": None
        }
    },
    {
        "id": "validate_004",
        "input": {
            "raw_sql": "SELECT COUNT(wrong_column) FROM transactions;"
        },
        "expected": {
            "query_result": None,
            "error": "<database error>",
            "error_type": "runtime",
            "should_retry": True
        },
        "actual": {
            "query_result": None,
            "error": None,
            "error_type": None,
            "should_retry": None
        }
    },
    {
        "id": "validate_005",
        "input": {
            "raw_sql": "SELECT * FROM nonexistent_table;"
        },
        "expected": {
            "query_result": None,
            "error": "<database error>",
            "error_type": "runtime",
            "should_retry": True
        },
        "actual": {
            "query_result": None,
            "error": None,
            "error_type": None,
            "should_retry": None
        }
    },
    {
        "id": "validate_006",
        "input": {
            "raw_sql": "SELECT customer_id, COUNT(transaction_id) FROM transactions GROUP BY customer_id;"
        },
        "expected": {
            "query_result": "<actual DB result>",
            "error": None,
            "should_retry": False
        },
        "actual": {
            "query_result": None,
            "error": None,
            "should_retry": None
        }
    },
    {
        "id": "validate_007",
        "input": {
            "raw_sql": "SELECT p.category, COUNT(t.transaction_id) FROM products p JOIN transactions t ON p.product_id = t.product_id GROUP BY p.category;"
        },
        "expected": {
            "query_result": "<actual DB result>",
            "error": None,
            "should_retry": False
        },
        "actual": {
            "query_result": None,
            "error": None,
            "should_retry": None
        }
    },
    {
        "id": "validate_008",
        "input": {
            "raw_sql": "DROP TABLE transactions;"
        },
        "expected": {
            "query_result": None,
            "error": "<operation should be rejected>",
            "should_retry": False
        },
        "actual": {
            "query_result": None,
            "error": None,
            "should_retry": None
        }
    }
]

reflector_cases = [
    {
        "id": "reflector_001",
        "input": {
            "raw_query": "SELECT COUNT(wrong_column) FROM transactions;",
            "error": "column wrong_column does not exist",
            "iterations": 0
        },
        "expected": {
            "raw_query": "SELECT COUNT(transaction_id) FROM transactions;",
            "iterations": 1,
            "should_retry": True
        },
        "actual": {
            "raw_query": None,
            "iterations": None,
            "should_retry": None
        }
    },
    {
        "id": "reflector_002",
        "input": {
            "raw_query": "SELECT * FROM nonexistent_table;",
            "error": "table nonexistent_table does not exist",
            "iterations": 0
        },
        "expected": {
            "raw_query": "SELECT * FROM customers;",
            "iterations": 1,
            "should_retry": True
        },
        "actual": {
            "raw_query": None,
            "iterations": None,
            "should_retry": None
        }
    },
    {
        "id": "reflector_003",
        "input": {
            "raw_query": "SELECT customer_id COUNT(*) FROM transactions GROUP BY customer_id;",
            "error": "syntax error",
            "iterations": 0
        },
        "expected": {
            "raw_query": "SELECT customer_id, COUNT(*) FROM transactions GROUP BY customer_id;",
            "iterations": 1,
            "should_retry": True
        },
        "actual": {
            "raw_query": None,
            "iterations": None,
            "should_retry": None
        }
    },
    {
        "id": "reflector_004",
        "input": {
            "raw_query": "SELECT p.category FROM products p JOIN transactions t ON p.id = t.product_id;",
            "error": "column p.id does not exist",
            "iterations": 0
        },
        "expected": {
            "raw_query": "SELECT p.category FROM products p JOIN transactions t ON p.product_id = t.product_id;",
            "iterations": 1,
            "should_retry": True
        },
        "actual": {
            "raw_query": None,
            "iterations": None,
            "should_retry": None
        }
    },
    {
        "id": "reflector_005",
        "input": {
            "raw_query": "SELECT customer_id, AVG(order_value) FROM transactions;",
            "error": "column customer_id must appear in GROUP BY",
            "iterations": 1
        },
        "expected": {
            "raw_query": "SELECT customer_id, AVG(order_value) FROM transactions GROUP BY customer_id;",
            "iterations": 2,
            "should_retry": True
        },
        "actual": {
            "raw_query": None,
            "iterations": None,
            "should_retry": None
        }
    },
    {
        "id": "reflector_006",
        "input": {
            "raw_query": "SELECT * FROM transactions;",
            "error": "query failed",
            "iterations": 2
        },
        "expected": {
            "raw_query": None,
            "iterations": 3,
            "should_retry": False
        },
        "actual": {
            "raw_query": None,
            "iterations": None,
            "should_retry": None
        }
    },
    {
        "id": "reflector_007",
        "input": {
            "raw_query": "SELECT * FROM transactions; DROP TABLE customers;",
            "error": "unsafe SQL operation",
            "iterations": 0
        },
        "expected": {
            "raw_query": None,
            "iterations": 1,
            "should_retry": False
        },
        "actual": {
            "raw_query": None,
            "iterations": None,
            "should_retry": None
        }
    },
    {
        "id": "reflector_008",
        "input": {
            "raw_query": "SELECT COUNT(transaction_id) FROM transactions;",
            "error": "unexpected validation failure",
            "iterations": 3
        },
        "expected": {
            "raw_query": None,
            "iterations": 4,
            "should_retry": False
        },
        "actual": {
            "raw_query": None,
            "iterations": None,
            "should_retry": None
        }
    }
]