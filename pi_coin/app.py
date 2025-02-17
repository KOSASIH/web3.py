from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from constant import PiCoinConfig
import uvicorn

app = FastAPI(title=PiCoinConfig.General.PROJECT_NAME, version=PiCoinConfig.General.VERSION)

# OAuth2 password bearer for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock database for users and transactions
fake_users_db = {
    "user@example.com": {
        "username": "user@example.com",
        "full_name": "John Doe",
        "email": "user@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}

fake_transactions_db = []

# Pydantic models for request and response
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool = None

class Transaction(BaseModel):
    sender: str
    receiver: str
    amount: float

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility functions
def fake_hash_password(password: str):
    return "fakehashed" + password

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_users_db.get(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not user['hashed_password'] == fake_hash_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user['username'], "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/transactions/", response_model=Transaction)
async def create_transaction(transaction: Transaction, current_user: User = Depends(get_current_user)):
    if transaction.amount < PiCoinConfig.Transaction.MIN_TRANSACTION_AMOUNT:
        raise HTTPException(status_code=400, detail="Transaction amount is below the minimum limit.")
    if transaction.amount > PiCoinConfig.General.VALUE:
        raise HTTPException(status_code=400, detail="Transaction amount exceeds available balance.")
    
    # Simulate saving the transaction
    fake_transactions_db.append(transaction)
    return transaction

@app.get("/transactions/", response_model=List[Transaction])
async def get_transactions(current_user: User = Depends(get_current_user)):
    return fake_transactions_db

@app.get("/")
async def root():
    return {"message": f"Welcome to {PiCoinConfig.General.PROJECT_NAME} API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
