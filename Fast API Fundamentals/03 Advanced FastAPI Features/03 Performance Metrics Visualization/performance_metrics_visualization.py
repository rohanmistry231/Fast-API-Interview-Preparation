# %% performance_metrics_visualization.py
# Setup: pip install fastapi uvicorn requests matplotlib pandas
from fastapi import FastAPI
import uvicorn
import requests
import matplotlib.pyplot as plt
import time
import threading

app = FastAPI()

# Synthetic Data
items = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Phone", "price": 499.99}
]

# Endpoints
@app.get("/items")
async def get_items():
    return items

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}, 404

@app.post("/items")
async def create_item(item: dict):
    items.append(item)
    return item, 201

# Function to measure and visualize performance metrics
def visualize_performance():
    print("Synthetic Data: Items created")
    print(f"Items: {items}")
    
    # Track performance metrics
    response_times = []
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Test endpoints with multiple requests
    requests_list = [
        ("GET", "http://localhost:8000/items"),
        ("GET", "http://localhost:8000/items/1"),
        ("GET", "http://localhost:8000/items/999"),
        ("POST", "http://localhost:8000/items", {"id": 3, "name": "Tablet", "price": 299.99})
    ]
    
    for method, url, *data in requests_list:
        start_time = time.time()
        try:
            if method == "GET":
                response = requests.get(url)
            else:
                response = requests.post(url, json=data[0])
            response.raise_for_status()
            elapsed_time = time.time() - start_time
            response_times.append(elapsed_time)
            success_counts["Successful"] += 1
            print(f"{method} {url}: {response.status_code} ({elapsed_time:.3f}s)")
        except requests.RequestException as e:
            response_times.append(0)
            success_counts["Failed"] += 1
            print(f"Error for {method} {url}: {e}")
    
    # Visualization
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(response_times) + 1), response_times, marker='o', color='blue')
    plt.title("Response Times")
    plt.xlabel("Request")
    plt.ylabel("Time (seconds)")
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("Request Success")
    plt.xlabel("Status")
    plt.ylabel("Count")
    
    plt.tight_layout()
    plt.savefig("performance_metrics_visualization_output.png")
    print("Visualization: Performance metrics saved as performance_metrics_visualization_output.png")

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
    
    # Visualize performance
    visualize_performance()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)