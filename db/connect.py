from typing import List
from sqlalchemy import create_engine, ForeignKey, BIGINT
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, Session

from db.config import Config

engine = create_engine(Config().DB_URL)
Base = declarative_base()
session = Session(engine)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, __type_pos=BIGINT)
    full_name: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    lang: Mapped[str]
    firlansers: Mapped[List['Firlanser']] = relationship(back_populates="user")
    customers: Mapped[List['Customer']] = relationship(back_populates="user")

class ProgLang(Base):
    __tablename__ = "prog_langs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    firlansers: Mapped[List['Firlanser']] = relationship(back_populates="prog_lang")

class Firlanser(Base):
    __tablename__ = "firlansers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column("user_id", BIGINT, ForeignKey("users.id"))
    prog_lang_id: Mapped[int] = mapped_column(ForeignKey("prog_langs.id"))
    user: Mapped['User'] = relationship(back_populates="firlansers")
    prog_lang: Mapped['ProgLang'] = relationship(back_populates="firlansers")

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column("user_id", BIGINT,ForeignKey("users.id"))
    products: Mapped[List['Product']] = relationship(back_populates="customer")
    user: Mapped['User'] = relationship(back_populates="customers")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[str]
    status: Mapped[str] = mapped_column(default='sent')
    customer_id: Mapped[int] = mapped_column("customer_id", BIGINT, ForeignKey("customers.id"))
    customer: Mapped['Customer'] = relationship(back_populates="products")











