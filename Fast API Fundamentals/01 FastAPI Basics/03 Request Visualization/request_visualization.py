# %% request_visualization.py
# Setup: pip install fastapi uvicorn requests matplotlib pandas
from fastapi import FastAPI, HTTPException
import uvicorn
import requests
import matplotlib.pyplot as plt
from collections import Counter
import threading
import time

app = FastAPI()

# Synthetic Data
items = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Phone", "price": 499.99}
]

# Endpoints for testing
@app.get("/items")
def get_items():
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items")
def create_item(item: dict):
    if "id" not in item or "name" not in item or "price" not in item:
        raise HTTPException(status_code=400, detail="Invalid item data")
    items.append(item)
    return item, 201

# Function to simulate and visualize requests
def visualize_requests():
    print("Synthetic Data: Items created")
    print(f"Items: {items}")
    
    # Track request success
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Simulate requests
    requests_list = [
        ("GET", "http://localhost:8000/items"),
        ("GET", "http://localhost:8000/items/1"),
        ("GET", "http://localhost:8000/items/999"),
        ("POST", "http://localhost:8000/items", {"id": 3, "name": "Tablet", "price": 299.99}),
        ("POST", "http://localhost:8000/items", {"name": "Invalid"})  # Invalid data
    ]
    
    for method, url, *data in requests_list:
        try:
            if method == "GET":
                response = requests.get(url)
            else:
                response = requests.post(url, json=data[0])
            response.raise_for_status()
            success_counts["Successful"] += 1
            print(f"{method} {url}: {response.status_code}")
        except requests.RequestException as e:
            success_counts["Failed"] += 1
            print(f"Error for {method} {url}: {e}")
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("API Request Success Rates")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.savefig("request_visualization_output.png")
    print("Visualization: Request success saved as request_visualization_output.png")

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
    
    # Simulate and visualize requests
    visualize_requests()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)