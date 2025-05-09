# %% data_validation_pydantic.py
# Setup: pip install fastapi uvicorn pydantic requests matplotlib pandas
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import uvicorn
import requests
import matplotlib.pyplot as plt
from collections import Counter
import threading
import time

app = FastAPI()

# Pydantic Model
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int | None = None

# Synthetic Data
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 25}
]

# Endpoints
@app.get("/users")
def get_users():
    return users

@app.post("/users")
def create_user(user: User):
    users.append(user.dict())
    return user, 201

# Function to test data validation
def test_validation():
    print("Synthetic Data: Users created")
    print(f"Users: {users}")
    
    # Track request success
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Test endpoints
    requests_list = [
        ("GET", "http://localhost:8000/users", None),
        ("POST", "http://localhost:8000/users", {"id": 3, "name": "Charlie", "email": "charlie@example.com", "age": 28}),
        ("POST", "http://localhost:8000/users", {"id": 4, "name": "David", "email": "invalid-email", "age": 22}),  # Invalid email
        ("POST", "http://localhost:8000/users", {"name": "Eve", "email": "eve@example.com"})  # Missing id
    ]
    
    for method, url, data in requests_list:
        try:
            if method == "GET":
                response = requests.get(url)
            else:
                response = requests.post(url, json=data)
            response.raise_for_status()
            success_counts["Successful"] += 1
            print(f"{method} {url}: {response.status_code}")
        except requests.RequestException as e:
            success_counts["Failed"] += 1
            print(f"Error for {method} {url}: {e}")
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("Data Validation Request Success")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.savefig("data_validation_pydantic_output.png")
    print("Visualization: Validation success saved as data_validation_pydantic_output.png")

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
    
    # Test validation
    test_validation()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)