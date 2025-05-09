# %% path_query_parameters.py
# Setup: pip install fastapi uvicorn requests matplotlib pandas
from fastapi import FastAPI
import uvicorn
import requests
import matplotlib.pyplot as plt
from collections import Counter
import threading
import time

app = FastAPI()

# Synthetic Data
items = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 999.99},
    {"id": 2, "name": "Phone", "category": "Electronics", "price": 499.99},
    {"id": 3, "name": "Book", "category": "Stationery", "price": 19.99}
]

# Endpoints
@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}, 404

@app.get("/items")
def get_items_by_category(category: str = None, max_price: float = None):
    filtered_items = items
    if category:
        filtered_items = [item for item in filtered_items if item["category"].lower() == category.lower()]
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item["price"] <= max_price]
    return filtered_items if filtered_items else {"error": "No items found"}, 404

# Function to test path and query parameters
def test_parameters():
    print("Synthetic Data: Items created")
    print(f"Items: {items}")
    
    # Track request success
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Test endpoints
    endpoints = [
        ("GET", "http://localhost:8000/items/1"),
        ("GET", "http://localhost:8000/items/999"),
        ("GET", "http://localhost:8000/items?category=Electronics"),
        ("GET", "http://localhost:8000/items?category=Electronics&max_price=500.0"),
        ("GET", "http://localhost:8000/items?category=Unknown")
    ]
    
    for method, url in endpoints:
        try:
            response = requests.get(url)
            response.raise_for_status()
            success_counts["Successful"] += 1
            print(f"{method} {url}: {response.status_code}")
        except requests.RequestException as e:
            success_counts["Failed"] += 1
            print(f"Error for {method} {url}: {e}")
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("Path and Query Parameter Request Success")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.savefig("path_query_parameters_output.png")
    print("Visualization: Request success saved as path_query_parameters_output.png")

# Run FastAPI server in a thread
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Test parameters
    test_parameters()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)