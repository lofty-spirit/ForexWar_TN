from datetime import datetime
from pydantic import BaseModel, EmailStr, validator, Field
from decimal import Decimal
from typing import Optional

#currencies router:

class CurrencyRequest(BaseModel):
    from_currency: str
    to_currency: str

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


class UserUpdate(BaseModel):
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
    leverage:int
    required_margin:Decimal 
    free_margin:Decimal
    performance:Decimal 
    status: str
    created_at: datetime

    class Config:
        orm_mode=True

class UserList(BaseModel):
    id: int
    username: str
    balance: Decimal
    profit: Decimal
    equity:Decimal
    performance:Decimal 
    status: str
    created_at: datetime

    class Config:
        orm_mode=True




# order route
class OrderOut(BaseModel):
    id: int
    type: str
    objective: str
    currency_pair: str
    current_profit: Decimal
    trigger_price: Optional[Decimal] = None
    triggered: bool
    quantity_in_lots: Decimal
    take_profit: Optional[Decimal] = None
    stop_loss: Optional[Decimal] = None
    status: str
    created_at: datetime

    class Config:
        orm_mode=True


class OrderCreate(BaseModel):
    type: str
    objective: str
    currency_pair: str
    trigger_price: Optional[Decimal]
    quantity_in_lots: Decimal
    take_profit: Optional[Decimal] = None
    stop_loss: Optional[Decimal] = None


class OrderUpdate(BaseModel):
    take_profit: Optional[float] = Field(None, description="New take profit value")
    stop_loss: Optional[float] = Field(None, description="New stop loss value")
