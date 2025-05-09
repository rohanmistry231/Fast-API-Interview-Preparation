# %% unit_integration_testing.py
# Setup: pip install fastapi uvicorn pytest requests matplotlib pandas
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
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

@app.post("/items")
def create_item(item: dict):
    items.append(item)
    return item, 201

# Unit and Integration Tests
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

def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Item not found"}

def test_create_item(client):
    new_item = {"id": 3, "name": "Tablet", "price": 299.99}
    response = client.post("/items", json=new_item)
    assert response.status_code == 201
    assert response.json() == new_item

# Function to run tests and visualize results
def run_tests():
    print("Synthetic Data: Items created")
    print(f"Items: {items}")
    
    # Track test results
    success_counts = {"Passed": 0, "Failed": 0}
    
    # Run tests manually to capture results
    client = TestClient(app)
    tests = [
        test_get_items,
        test_get_item,
        test_get_item_not_found,
        test_create_item
    ]
    
    for test_func in tests:
        try:
            test_func(client)
            success_counts["Passed"] += 1
            print(f"Test {test_func.__name__}: Passed")
        except AssertionError as e:
            success_counts["Failed"] += 1
            print(f"Test {test_func.__name__}: Failed - {e}")
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("Test Results")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.savefig("unit_integration_testing_output.png")
    print("Visualization: Test results saved as unit_integration_testing_output.png")

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
    
    # Run tests
    run_tests()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)