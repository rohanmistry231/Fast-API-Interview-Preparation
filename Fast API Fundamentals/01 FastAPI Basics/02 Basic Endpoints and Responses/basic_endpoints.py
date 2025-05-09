# %% basic_endpoints.py
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
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

# Endpoints
@app.get("/users")
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users")
def create_user(user: dict):
    if "id" not in user or "name" not in user or "email" not in user:
        raise HTTPException(status_code=400, detail="Invalid user data")
    users.append(user)
    return user, 201

# Function to test endpoints
def test_endpoints():
    print("Synthetic Data: Users created")
    print(f"Users: {users}")
    
    # Track request success
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Test endpoints
    endpoints = [
        ("GET", "http://localhost:8000/users"),
        ("GET", "http://localhost:8000/users/1"),
        ("GET", "http://localhost:8000/users/999")
    ]
    
    for method, url in endpoints:
        try:
            response = requests.get(url)
            response.raise_for_status()
            success_counts["Successful"] += 1
            print(f"{method} {url}: {response.status_code}")
        except requests.RequestException as e:
            success_counts["Failed"] += 1
            print(f"Error for {url}: {e}")
    
    # Test POST
    new_user = {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    try:
        response = requests.post("http://localhost:8000/users", json=new_user)
        response.raise_for_status()
        success_counts["Successful"] += 1
        print(f"POST /users: {response.status_code}")
    except requests.RequestException as e:
        success_counts["Failed"] += 1
        print(f"Error for POST /users: {e}")
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("Endpoint Request Success")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.savefig("basic_endpoints_output.png")
    print("Visualization: Endpoint success saved as basic_endpoints_output.png")

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
    
    # Test endpoints
    test_endpoints()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)