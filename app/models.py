from sqlalchemy import Column, Integer, String, Numeric, Boolean, text, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    balance = Column(Numeric, server_default='5000000.0000')
    profit = Column(Numeric, server_default='0.0000')
    equity = Column(Numeric, server_default='5000000.0000')
    leverage = Column(Integer, server_default='50')
    required_margin = Column(Numeric, server_default='0.0000')
    free_margin = Column(Numeric, server_default='5000000.0000')
    performance = Column(Numeric, server_default='0.0000')
    status = Column(String, server_default="competing")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class Order(Base):
    __tablename__ = "orders"
    id= Column(Integer, primary_key=True, nullable=False)
    type=Column(String,nullable=False, server_default="market")
    objective=Column(String,nullable=False)
    currency_pair=Column(String,nullable=False)
    trigger_price=Column(Numeric(precision=11, scale=4, asdecimal=True), server_default=text("NULL"))
    triggered=Column(Boolean, server_default='FALSE')
    quantity_in_lots= Column(Numeric(precision=11, scale=4, asdecimal=True),nullable=False)
    take_profit=Column(Numeric(precision=11, scale=4, asdecimal=True), server_default=text("NULL"))
    stop_loss=Column(Numeric(precision=11, scale=4, asdecimal=True), server_default=text("NULL"))
    current_profit=Column(Numeric(precision=11,scale=4,asdecimal=True), server_default='0.0000')
    status=Column(String, server_default="open")
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)