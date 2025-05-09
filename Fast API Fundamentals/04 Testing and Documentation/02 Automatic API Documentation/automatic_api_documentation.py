# %% automatic_api_documentation.py
# Setup: pip install fastapi uvicorn requests matplotlib pandas
from fastapi import FastAPI
import uvicorn
import requests
import matplotlib.pyplot as plt
from collections import Counter
import threading
import time

app = FastAPI(
    title="Sample FastAPI App",
    description="A sample API for demonstrating automatic documentation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Synthetic Data
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

# Endpoints with documentation
@app.get("/users", summary="Get all users", description="Returns a list of all users")
def get_users():
    return users

@app.get("/users/{user_id}", summary="Get a user by ID", description="Returns a single user by ID")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}, 404

@app.post("/users", summary="Create a user", description="Creates a new user")
def create_user(user: dict):
    users.append(user)
    return user, 201

# Function to test documentation accessibility
def test_documentation():
    print("Synthetic Data: Users created")
    print(f"Users: {users}")
    
    # Track request success
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Test documentation endpoints
    endpoints = [
        ("GET", "http://localhost:8000/docs"),  # Swagger UI
        ("GET", "http://localhost:8000/redoc"),  # ReDoc
        ("GET", "http://localhost:8000/users")  # API endpoint for reference
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
    plt.title("Documentation Accessibility")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.savefig("automatic_api_documentation_output.png")
    print("Visualization: Documentation access saved as automatic_api_documentation_output.png")

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
    
    # Test documentation
    test_documentation()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)