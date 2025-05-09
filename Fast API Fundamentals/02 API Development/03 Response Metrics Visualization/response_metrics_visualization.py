# %% response_metrics_visualization.py
# Setup: pip install fastapi uvicorn pydantic requests matplotlib pandas
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import requests
import matplotlib.pyplot as plt
import time
import threading

app = FastAPI()

# Pydantic Model
class Item(BaseModel):
    id: int
    name: str
    price: float

# Synthetic Data
items = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Phone", "price": 499.99}
]

# Endpoints
@app.get("/items")
def get_items():
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}, 404

@app.post("/items")
def create_item(item: Item):
    items.append(item.dict())
    return item, 201

# Function to measure and visualize response metrics
def visualize_metrics():
    print("Synthetic Data: Items created")
    print(f"Items: {items}")
    
    # Track response times
    response_times = []
    
    # Test endpoints
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
            print(f"{method} {url}: {response.status_code} ({elapsed_time:.3f}s)")
        except requests.RequestException as e:
            response_times.append(0)  # Record 0 for failed requests
            print(f"Error for {method} {url}: {e}")
    
    # Visualization
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, len(response_times) + 1), response_times, marker='o', color='blue')
    plt.title("API Response Times")
    plt.xlabel("Request")
    plt.ylabel("Response Time (seconds)")
    plt.grid(True)
    plt.savefig("response_metrics_visualization_output.png")
    print("Visualization: Response times saved as response_metrics_visualization_output.png")

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
    
    # Visualize metrics
    visualize_metrics()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)