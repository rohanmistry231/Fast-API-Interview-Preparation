# %% dockerizing_fastapi.py
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

# Simulate Dockerfile creation
def create_dockerfile():
    dockerfile_content = """
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    print("Simulated Dockerfile created:")
    print(dockerfile_content)
    return dockerfile_content

# Function to simulate Docker deployment and test
def test_docker_deployment():
    print("Synthetic Data: Items created")
    print(f"Items: {items}")
    
    # Simulate Docker build and run
    print("Simulating Docker build and run...")
    create_dockerfile()
    
    # Track request success
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Test API endpoints (simulating containerized app)
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
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("Dockerized API Request Success")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.savefig("dockerizing_fastapi_output.png")
    print("Visualization: Docker deployment success saved as dockerizing_fastapi_output.png")

# Run FastAPI server in a thread (simulating Docker container)
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Test Docker deployment
    test_docker_deployment()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)