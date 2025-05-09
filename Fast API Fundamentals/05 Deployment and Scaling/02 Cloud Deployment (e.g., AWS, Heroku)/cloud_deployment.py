# %% cloud_deployment.py
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
    return {"error": "User not found"}, 404

# Simulate cloud deployment configuration
def create_cloud_config():
    procfile_content = "web: uvicorn main:app --host=0.0.0.0 --port=$PORT"
    requirements_content = """
fastapi==0.68.0
uvicorn==0.15.0
"""
    print("Simulated cloud configuration created:")
    print("Procfile:")
    print(procfile_content)
    print("requirements.txt:")
    print(requirements_content)
    return procfile_content, requirements_content

# Function to simulate cloud deployment and test
def test_cloud_deployment():
    print("Synthetic Data: Users created")
    print(f"Users: {users}")
    
    # Simulate cloud deployment
    print("Simulating cloud deployment (e.g., AWS, Heroku)...")
    create_cloud_config()
    
    # Track request success
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Test API endpoints (simulating cloud-deployed app)
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
            print(f"Error for {method} {url}: {e}")
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("Cloud Deployed API Request Success")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.savefig("cloud_deployment_output.png")
    print("Visualization: Cloud deployment success saved as cloud_deployment_output.png")

# Run FastAPI server in a thread (simulating cloud environment)
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Test cloud deployment
    test_cloud_deployment()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)