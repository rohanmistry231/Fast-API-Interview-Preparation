# %% fastapi_setup.py
# Setup: pip install fastapi uvicorn requests matplotlib pandas
from fastapi import FastAPI
import uvicorn
import requests
import matplotlib.pyplot as plt
from collections import Counter
import threading
import time

app = FastAPI()

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to your first FastAPI application!"}

# Function to test API setup
def test_api_setup():
    print("Testing FastAPI Setup")
    
    # Track request success
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Test root endpoint
    url = "http://localhost:8000/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        success_counts["Successful"] += 1
        print(f"GET {url}: {response.status_code} - {response.json()}")
    except requests.RequestException as e:
        success_counts["Failed"] += 1
        print(f"Error for {url}: {e}")
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("API Setup Request Success")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.savefig("fastapi_setup_output.png")
    print("Visualization: Setup success saved as fastapi_setup_output.png")

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
    
    # Test API setup
    test_api_setup()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)