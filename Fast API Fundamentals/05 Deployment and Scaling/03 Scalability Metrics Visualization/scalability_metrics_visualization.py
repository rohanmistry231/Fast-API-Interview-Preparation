# %% scalability_metrics_visualization.py
# Setup: pip install fastapi uvicorn requests matplotlib pandas
from fastapi import FastAPI
import uvicorn
import requests
import matplotlib.pyplot as plt
import time
import threading
import concurrent.futures

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

# Function to simulate load testing and visualize scalability
def visualize_scalability():
    print("Synthetic Data: Items created")
    print(f"Items: {items}")
    
    # Track response times
    response_times = []
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Simulate load with concurrent requests
    endpoints = [
        ("GET", "http://localhost:8000/items"),
        ("GET", "http://localhost:8000/items/1"),
        ("GET", "http://localhost:8000/items/999")
    ]
    load_requests = endpoints * 5  # Simulate 15 requests
    
    def make_request(method, url):
        start_time = time.time()
        try:
            response = requests.get(url)
            response.raise_for_status()
            elapsed_time = time.time() - start_time
            return elapsed_time, True
        except requests.RequestException:
            return 0, False
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda x: make_request(*x), [(m, u) for m, u in load_requests]))
    
    for elapsed_time, success in results:
        response_times.append(elapsed_time)
        success_counts["Successful" if success else "Failed"] += 1
        print(f"Request: {'Success' if success else 'Failed'} ({elapsed_time:.3f}s)")
    
    # Visualization
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(response_times) + 1), response_times, marker='o', color='blue')
    plt.title("Response Times Under Load")
    plt.xlabel("Request")
    plt.ylabel("Time (seconds)")
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("Request Success Under Load")
    plt.xlabel("Status")
    plt.ylabel("Count")
    
    plt.tight_layout()
    plt.savefig("scalability_metrics_visualization_output.png")
    print("Visualization: Scalability metrics saved as scalability_metrics_visualization_output.png")

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
    
    # Visualize scalability
    visualize_scalability()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)