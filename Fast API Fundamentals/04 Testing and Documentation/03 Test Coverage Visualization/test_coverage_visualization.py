# %% test_coverage_visualization.py
# Setup: pip install fastapi uvicorn pytest pytest-cov requests matplotlib pandas
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
import uvicorn
import requests
import matplotlib.pyplot as plt
import subprocess
import re
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

@app.post("/items")
def create_item(item: dict):
    items.append(item)
    return item, 201

# Unit Tests
@pytest.fixture
def client():
    return TestClient(app)

def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == items

def test_get_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Laptop", "price": 999.99}

# Function to run tests and visualize coverage
def visualize_coverage():
    print("Synthetic Data: Items created")
    print(f"Items: {items}")
    
    # Run pytest with coverage
    try:
        result = subprocess.run(
            ["pytest", "--cov=.", "--cov-report=term", __file__],
            capture_output=True, text=True
        )
        output = result.stdout
        print("Pytest Output:", output)
        
        # Extract coverage percentage
        match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", output)
        coverage = int(match.group(1)) if match else 0
    except Exception as e:
        print(f"Error running pytest: {e}")
        coverage = 0
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(["Covered", "Uncovered"], [coverage, 100 - coverage], color=['green', 'red'])
    plt.title("Test Coverage")
    plt.xlabel("Status")
    plt.ylabel("Percentage")
    plt.savefig("test_coverage_visualization_output.png")
    print("Visualization: Coverage saved as test_coverage_visualization_output.png")

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
    
    # Visualize coverage
    visualize_coverage()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)