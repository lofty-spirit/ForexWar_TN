from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, utilities, oauth2
from ..database import engine, get_db

router=APIRouter(
    tags=['Trading']
)


@router.post("/orders/", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if order.currency_pair not in ["TNDEUR","EURUSD","USDCAD"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Available currency pairs TNDEUR, EURUSD or USDCAD")
    
    if order.type not in ["market","limit","stop"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Type can only be market, limit or stop")
    
    if order.objective not in ["buy","sell"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The objective of an order is either buy or sell")
    
    # Check if trigger_price is set and type is market
    if order.trigger_price is not None and order.type == "market":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="If trigger_price is set, type cannot be market")

    if order.trigger_price is None and order.type != "market":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A pending order has to include a trigger price")
    
    print(current_user)
    new_order = models.Order(owner_id=current_user.id, **order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/open_orders/", response_model=List[schemas.OrderOut])
def get_open_orders(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit : int = 100, search: Optional[str]=""):
    # Retrieve all open orders for the current user
    open_orders = db.query(models.Order).filter(models.Order.owner_id == current_user.id, models.Order.status == "open").filter(models.Order.type.contains(search)).order_by(models.Order.id.desc()).limit(limit).all()
    if not open_orders:
        raise HTTPException(status_code=404, detail="No open orders found")
    return open_orders

@router.get("/closed_orders/", response_model=List[schemas.OrderOut])
def get_open_orders(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int=100, search: Optional[str]=""):
    # Retrieve all open orders for the current user
    open_orders = db.query(models.Order).filter(models.Order.owner_id == current_user.id, models.Order.status == "closed").filter(models.Order.type.contains(search)).order_by(models.Order.id.desc()).limit(limit).all()
    if not open_orders:
        raise HTTPException(status_code=404, detail="No closed orders found")
    return open_orders


@router.put("/orders/{order_id}", response_model=schemas.OrderOut)
def update_order(order_id: int,order_update: schemas.OrderUpdate,db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    # Retrieve the order from the database
    existing_order = db.query(models.Order).filter(models.Order.id == order_id).first()

    # Check if the order exists
    if not existing_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Check if the current user owns the order
    if existing_order.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this order")


    if existing_order.status == "closed":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This order is closed. You cannot change its properties anymore. Create a new order")
    

    # Update the order fields if provided in the request
    if order_update.take_profit is not None:
        existing_order.take_profit = order_update.take_profit

    if order_update.stop_loss is not None:
        existing_order.stop_loss = order_update.stop_loss

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_order)

    return existing_order

@router.put("/orders_closing/{order_id}", response_model=schemas.OrderOut)
def update_order(order_id: int,db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    # Retrieve the order from the database
    existing_order = db.query(models.Order).filter(models.Order.id == order_id).first()

    # Check if the order exists
    if not existing_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Check if the current user owns the order
    if existing_order.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this order")

    # set status to closed
    existing_order.status = "closed"

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_order)

    return existing_order