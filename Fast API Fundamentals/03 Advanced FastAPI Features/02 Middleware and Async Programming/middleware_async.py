# %% middleware_async.py
# Setup: pip install fastapi uvicorn requests matplotlib pandas
from fastapi import FastAPI, Request
import uvicorn
import requests
import matplotlib.pyplot as plt
from collections import Counter
import threading
import time
import asyncio

app = FastAPI()

# Synthetic Data
requests_log = []

# Custom Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    requests_log.append({"path": str(request.url.path), "duration": duration})
    return response

# Async Endpoints
@app.get("/items")
async def get_items():
    await asyncio.sleep(0.1)  # Simulate async work
    return [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Phone"}]

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    await asyncio.sleep(0.05)  # Simulate async work
    items = {1: "Laptop", 2: "Phone"}
    return {"id": item_id, "name": items.get(item_id, "Not found")}

# Function to test middleware and async endpoints
def test_middleware_async():
    print("Synthetic Data: Requests log initialized")
    
    # Track request success
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Test async endpoints
    endpoints = [
        ("GET", "http://localhost:8000/items"),
        ("GET", "http://localhost:8000/items/1"),
        ("GET", "http://localhost:8000/items/999")
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
    
    # Visualization of request durations
    durations = [log["duration"] for log in requests_log]
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, len(durations) + 1), durations, marker='o', color='blue')
    plt.title("Request Durations (Middleware)")
    plt.xlabel("Request")
    plt.ylabel("Duration (seconds)")
    plt.grid(True)
    plt.savefig("middleware_async_output.png")
    print("Visualization: Request durations saved as middleware_async_output.png")

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
    
    # Test middleware and async
    test_middleware_async()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)