import os
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
load_dotenv()
import os
## 1. Configuration & Setup
# Use an in-memory SQLite database for this example for simplicity.
# Replace with your PostgreSQL DATABASE_URL for a real application.
DATABASE_URL =os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

## 2. Pydantic Schema (for data validation and API modeling)
# This defines the shape of data for creating or reading a product.
class ProductSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)

    class Config:
        orm_mode = True # Allows Pydantic to work with ORM objects

## 3. SQLAlchemy Model (for database table definition)
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Numeric(10, 2))

## 4. Database Utility Class
class DatabaseManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """Provides a database session."""
        return self.SessionLocal()

    # --- Utility Functions for CRUD Operations ---

    def create_product(self, product_data: ProductSchema) -> Product:
        """Creates a new product in the database."""
        with self.get_session() as db:
            db_product = Product(**product_data.dict())
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return db_product

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Fetches a single product by its ID."""
        with self.get_session() as db:
            return db.query(Product).filter(Product.id == product_id).first()

    def get_all_products(self) -> List[Product]:
        """Fetches all products from the database."""
        with self.get_session() as db:
            return db.query(Product).all()

    def update_product(self, product_id: int, update_data: dict) -> Optional[Product]:
        """Updates an existing product."""
        with self.get_session() as db:
            db_product = db.query(Product).filter(Product.id == product_id).first()
            if db_product:
                for key, value in update_data.items():
                    setattr(db_product, key, value)
                db.commit()
                db.refresh(db_product)
            return db_product

    def delete_product(self, product_id: int) -> bool:
        """Deletes a product from the database."""
        with self.get_session() as db:
            db_product = db.query(Product).filter(Product.id == product_id).first()
            if db_product:
                db.delete(db_product)
                db.commit()
                return True
            return False

## 5. Example Usage
if __name__ == "__main__":
    # Clean up previous database file for a fresh run
    if os.path.exists("./test.db"):
        os.remove("./test.db")
        
    print("--- Initializing Database Manager ---")
    db_manager = DatabaseManager(DATABASE_URL)

    # CREATE
    print("\n--- 1. CREATE Operation ---")
    product_to_create = ProductSchema(name="Laptop", price=1299.99)
    created_product = db_manager.create_product(product_to_create)
    print(f"Created Product: ID={created_product.id}, Name='{created_product.name}'")
    
    product_to_create_2 = ProductSchema(name="Wireless Mouse", price=75.50)
    created_product_2 = db_manager.create_product(product_to_create_2)
    print(f"Created Product: ID={created_product_2.id}, Name='{created_product_2.name}'")


    # READ (All)
    print("\n--- 2. READ (All) Operation ---")
    all_products = db_manager.get_all_products()
    print(f"Found {len(all_products)} products.")
    for p in all_products:
        print(f"  - ID: {p.id}, Name: {p.name}, Price: {p.price}")

    # READ (By ID)
    print("\n--- 3. READ (By ID) Operation ---")
    fetched_product = db_manager.get_product_by_id(product_id=1)
    if fetched_product:
        print(f"Fetched Product by ID=1: Name='{fetched_product.name}'")

    # UPDATE
    print("\n--- 4. UPDATE Operation ---")
    update_payload = {"price": 1249.00}
    updated_product = db_manager.update_product(product_id=1, update_data=update_payload)
    if updated_product:
        print(f"Updated Product ID=1: New Price={updated_product.price}")

    # DELETE
    print("\n--- 5. DELETE Operation ---")
    was_deleted = db_manager.delete_product(product_id=2)
    print(f"Was Product ID=2 deleted? {'Yes' if was_deleted else 'No'}")

    # Final READ to confirm changes
    print("\n--- 6. Final State of Database ---")
    final_products = db_manager.get_all_products()
    for p in final_products:
        print(f"  - ID: {p.id}, Name: {p.name}, Price: {p.price}")