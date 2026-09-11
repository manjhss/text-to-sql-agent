from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(String, primary_key=True)
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    registration_date: Mapped[str] = mapped_column(String)
    loyalty_score: Mapped[float] = mapped_column(Float)
    lifetime_value: Mapped[float] = mapped_column(Float)
    churn_label: Mapped[int] = mapped_column(Integer)

    # relationships
    behavior: Mapped[Behavior] = relationship(
        back_populates="customer", uselist=False, cascade="all, delete-orphan"
    )
    transactions: Mapped[list[Transaction]] = relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<customer {self.customer_id} ({self.country})>"


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(String, primary_key=True)
    category: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    margin_percentage: Mapped[float] = mapped_column(Float)
    popularity_score: Mapped[float] = mapped_column(Float)

    # relationships
    transactions: Mapped[list[Transaction]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<product {self.product_id} ({self.category})>"


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(
        String, ForeignKey("customers.customer_id"), index=True
    )
    product_id: Mapped[str] = mapped_column(
        String, ForeignKey("products.product_id"), index=True
    )
    order_date: Mapped[str] = mapped_column(String)
    order_value: Mapped[float] = mapped_column(Float)
    payment_method: Mapped[str] = mapped_column(String)
    device_type: Mapped[str] = mapped_column(String)
    discount_applied: Mapped[float] = mapped_column(Float)
    shipping_delay_days: Mapped[int] = mapped_column(Integer)
    fraud_label: Mapped[int] = mapped_column(Integer)

    # relationships
    customer: Mapped[Customer] = relationship(back_populates="transactions")
    product: Mapped[Product] = relationship(back_populates="transactions")

    def __repr__(self) -> str:
        return f"<transaction {self.transaction_id} cust={self.customer_id} prod={self.product_id}>"


class Behavior(Base):
    __tablename__ = "behaviors"

    customer_id: Mapped[str] = mapped_column(
        String, ForeignKey("customers.customer_id"), primary_key=True
    )
    avg_session_time: Mapped[float] = mapped_column(Float)
    pages_per_session: Mapped[int] = mapped_column(Integer)
    cart_abandon_rate: Mapped[float] = mapped_column(Float)
    return_rate: Mapped[float] = mapped_column(Float)
    support_tickets: Mapped[int] = mapped_column(Integer)
    review_score: Mapped[float] = mapped_column(Float)
    behavior_churn_signal: Mapped[int] = mapped_column(Integer)

    # relationship
    customer: Mapped[Customer] = relationship(back_populates="behavior")

    def __repr__(self) -> str:
        return f"<behavior cust={self.customer_id}>"
