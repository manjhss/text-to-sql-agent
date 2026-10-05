intent_classifier_cases = [
    {
        "id": "intent_001",
        "input": {"query": "What is the total number of transactions?"},
        "expected": {"intent": "relevant"},
    },
    {
        "id": "intent_002",
        "input": {"query": "Which products have the highest popularity score?"},
        "expected": {"intent": "relevant"},
    },
    {
        "id": "intent_003",
        "input": {"query": "How many customers are from India?"},
        "expected": {"intent": "relevant"},
    },
    {
        "id": "intent_004",
        "input": {"query": "What is the average session time for customers?"},
        "expected": {"intent": "relevant"},
    },
    {
        "id": "intent_005",
        "input": {"query": "I own a product."},
        "expected": {"intent": "irrelevant"},
    },
    {
        "id": "intent_006",
        "input": {"query": "Write a Python function to sort a list."},
        "expected": {"intent": "irrelevant"},
    },
    {
        "id": "intent_007",
        "input": {"query": "Tell me a joke about customers."},
        "expected": {"intent": "irrelevant"},
    },
    {
        "id": "intent_008",
        "input": {"query": "What's the weather like today?"},
        "expected": {"intent": "irrelevant"},
    },
]
