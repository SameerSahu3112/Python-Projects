# Backend Integration Guide

This guide explains how to connect your FastAPI backend to the React frontend.

## Table of Contents

1. [FastAPI Backend Setup](#fastapi-backend-setup)
2. [API Endpoints Structure](#api-endpoints-structure)
3. [Frontend API Integration](#frontend-api-integration)
4. [Authentication Flow](#authentication-flow)
5. [Example Implementations](#example-implementations)

---

## 1. FastAPI Backend Setup

### Step 1: Install Required Dependencies

```bash
pip install fastapi uvicorn python-multipart python-jose[cryptography] passlib[bcrypt]
```

### Step 2: Configure CORS

In your `main.py`, add CORS middleware to allow the React frontend to communicate:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 3: Set Up Database Models

Example using SQLAlchemy:

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(String)
    payment_method = Column(String)
    status = Column(String, default="Processing")
    created_at = Column(DateTime, default=datetime.utcnow)

class WishlistItem(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_name = Column(String)
    product_description = Column(String)
    price = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

## 2. API Endpoints Structure

### Authentication Endpoints

```python
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt

# Models
class UserSignIn(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    full_name: str
    email: str
    phone: str = None
    password: str

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Secret Key
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

@app.post("/api/signin")
async def signin(user: UserSignIn):
    # 1. Find user by email
    # 2. Verify password
    # 3. Generate JWT token
    # 4. Return token and user data
    pass

@app.post("/api/create-account")
async def create_account(user: UserCreate):
    # 1. Check if email already exists
    # 2. Hash password
    # 3. Create user in database
    # 4. Return success message
    pass
```

### User Profile Endpoints

```python
class UserUpdate(BaseModel):
    full_name: str = None
    email: str = None
    phone: str = None

@app.get("/api/user/profile")
async def get_user_profile(token: str = Depends(verify_token)):
    # 1. Verify token and get user_id
    # 2. Fetch user data from database
    # 3. Return user profile
    pass

@app.put("/api/user/profile")
async def update_user_profile(
    user_update: UserUpdate,
    token: str = Depends(verify_token)
):
    # 1. Verify token and get user_id
    # 2. Update user in database
    # 3. Return updated profile
    pass
```

### Orders Endpoints

```python
@app.get("/api/orders")
async def get_orders(token: str = Depends(verify_token)):
    # 1. Verify token and get user_id
    # 2. Fetch user's orders from database
    # 3. Return orders list
    pass

@app.post("/api/orders")
async def create_order(order_data: dict, token: str = Depends(verify_token)):
    # 1. Verify token and get user_id
    # 2. Create order in database
    # 3. Return order confirmation
    pass
```

### Wishlist Endpoints

```python
@app.get("/api/wishlist")
async def get_wishlist(token: str = Depends(verify_token)):
    # 1. Verify token and get user_id
    # 2. Fetch wishlist items from database
    # 3. Return wishlist
    pass

@app.post("/api/wishlist")
async def add_to_wishlist(item: dict, token: str = Depends(verify_token)):
    # 1. Verify token and get user_id
    # 2. Add item to wishlist
    # 3. Return success message
    pass

@app.delete("/api/wishlist/{item_id}")
async def remove_from_wishlist(item_id: int, token: str = Depends(verify_token)):
    # 1. Verify token and get user_id
    # 2. Remove item from wishlist
    # 3. Return success message
    pass
```

---

## 3. Frontend API Integration

The frontend includes a centralized API utility file at `src/utils/api.js` that handles all API calls.

### Using the API Utilities

```javascript
import { authAPI, userAPI, ordersAPI, wishlistAPI } from '../utils/api';

// Sign In
const handleSignIn = async () => {
  try {
    const data = await authAPI.signIn(email, password);
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    navigate('/account-settings');
  } catch (error) {
    setError('Sign in failed');
  }
};

// Get User Profile
const loadProfile = async () => {
  try {
    const data = await userAPI.getProfile();
    setPersonalInfo(data);
  } catch (error) {
    console.error('Failed to load profile');
  }
};

// Get Orders
const loadOrders = async () => {
  try {
    const data = await ordersAPI.getOrders();
    setOrders(data);
  } catch (error) {
    console.error('Failed to load orders');
  }
};
```

---

## 4. Authentication Flow

### Sign In Flow

1. User enters email and password in React frontend
2. Frontend sends POST request to `/api/signin`
3. FastAPI verifies credentials against database
4. FastAPI generates JWT token
5. FastAPI returns token and user data
6. Frontend stores token in localStorage
7. Frontend redirects to account settings page

### Authenticated Requests Flow

1. Frontend makes request with Authorization header
2. Header format: `Bearer <token>`
3. FastAPI verifies token signature
4. FastAPI extracts user_id from token
5. FastAPI fetches/updates data
6. FastAPI returns response

### Sign Out Flow

1. User clicks sign out
2. Frontend calls `authAPI.signOut()`
3. Frontend removes token from localStorage
4. Frontend redirects to sign in page

---

## 5. Example Implementations

### Complete Sign In Implementation

**FastAPI Backend (`main.py`):**

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Models
class UserSignIn(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    full_name: str
    email: str
    phone: str = None
    password: str

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoints
@app.post("/api/signin")
async def signin(user: UserSignIn):
    # In production, fetch from database
    if user.email == "manoj@gmail.com" and user.password == "manoj123":
        access_token = create_access_token(data={"sub": user.email})
        return {
            "access_token": access_token,
            "user": {
                "email": user.email,
                "full_name": "Manoj Sahu",
                "is_admin": False
            }
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/create-account")
async def create_account(user: UserCreate):
    # In production, save to database
    return {"message": "Account created successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**React Frontend (already updated in SignIn.jsx):**

The SignIn page has been updated to use the API. See `src/pages/SignIn.jsx` for the implementation.

---

## Running Both Servers

### Start FastAPI Backend

```bash
cd /Users/manojsahu/Desktop/College/Python_Programs/FastAPI
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start React Frontend

```bash
cd frontend
npm run dev
```

The React frontend will be available at `http://localhost:5173`
The FastAPI backend will be available at `http://localhost:8000`

---

## Testing the Connection

1. Start both servers
2. Open React frontend in browser
3. Try signing in with demo credentials
4. Check browser console for API responses
5. Check FastAPI terminal for incoming requests

---

## Next Steps

1. Implement database models in FastAPI
2. Create all API endpoints
3. Update all React pages to use API utilities
4. Add proper error handling
5. Implement loading states
6. Add form validation
7. Implement password reset flow
8. Add admin panel for order management

---

## Security Notes

- Change `SECRET_KEY` in production
- Use environment variables for sensitive data
- Implement rate limiting
- Add input validation
- Use HTTPS in production
- Implement proper password policies
