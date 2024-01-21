from datetime import datetime
from pydantic import BaseModel, EmailStr
from decimal import Decimal, getcontext
from typing import Optional
getcontext().prec = 8



# auth router
class UserLogin(BaseModel):
    email :EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]=None












# user router
class UserCreate(BaseModel):
    username: str
    full_name: str
    email :EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    email :EmailStr
    balance: Decimal
    profit: Decimal
    equity:Decimal
    leverage:Decimal 
    required_margin:Decimal 
    free_margin:Decimal
    performance:Decimal 
    status: str
    created_at: datetime

    class Config:
        orm_mode=True




















class OrderBase(BaseModel):
    type: str
    objective: str
    currency_pair: str
    trigger_price: Decimal
    triggered: bool
    quantity_in_lots: Decimal
    take_profit: Decimal
    stop_loss: Decimal 
    status: str
    created_at: str