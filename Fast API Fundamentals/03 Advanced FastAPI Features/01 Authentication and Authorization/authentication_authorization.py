# %% authentication_authorization.py
# Setup: pip install fastapi uvicorn pydantic python-jose[cryptography] passlib[bcrypt] requests matplotlib pandas
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
import uvicorn
import requests
import matplotlib.pyplot as plt
from collections import Counter
import threading
import time

app = FastAPI()

# JWT Configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic Models
class User(BaseModel):
    username: str
    role: str

# Synthetic Data
users_db = {
    "admin": {"username": "admin", "password": pwd_context.hash("adminpass"), "role": "admin"},
    "user": {"username": "user", "password": pwd_context.hash("userpass"), "role": "user"}
}

# JWT Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username not in users_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return User(username=username, role=users_db[username]["role"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Endpoints
@app.post("/token")
async def login(username: str, password: str):
    user = users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": "This is a protected admin route", "user": current_user.username}

# Function to test authentication and authorization
def test_auth():
    print("Synthetic Data: Users created")
    print(f"Users: {list(users_db.keys())}")
    
    # Track request success
    success_counts = {"Successful": 0, "Failed": 0}
    
    # Test login and protected route
    tests = [
        ("POST", "http://localhost:8000/token", {"username": "admin", "password": "adminpass"}),
        ("POST", "http://localhost:8000/token", {"username": "user", "password": "wrongpass"}),
        ("GET", "http://localhost:8000/protected", None, "admin"),
        ("GET", "http://localhost:8000/protected", None, "user")
    ]
    
    admin_token = None
    for method, url, data, *user in tests:
        try:
            if method == "POST":
                response = requests.post(url, json=data)
                if response.status_code == 200 and data["username"] == "admin":
                    admin_token = response.json()["access_token"]
            else:
                headers = {"Authorization": f"Bearer {admin_token}" if user[0] == "admin" else "Bearer invalid"}
                response = requests.get(url, headers=headers)
            response.raise_for_status()
            success_counts["Successful"] += 1
            print(f"{method} {url}: {response.status_code}")
        except requests.RequestException as e:
            success_counts["Failed"] += 1
            print(f"Error for {method} {url}: {e}")
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(success_counts.keys(), success_counts.values(), color=['green', 'red'])
    plt.title("Authentication Request Success")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.savefig("authentication_authorization_output.png")
    print("Visualization: Auth success saved as authentication_authorization_output.png")

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
    
    # Test authentication
    test_auth()
    
    # Keep the main thread alive briefly to view results
    time.sleep(2)