from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
load_dotenv()
import os
DATABASE_URL = os.getenv("DATABASE_URL")

# The engine is the central point of contact with the database.
engine = create_engine(DATABASE_URL)

# The session is your "workspace" for adding and querying objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the base class our ORM models will inherit from.
Base = declarative_base()


# --- 2. Define the Table as a Python Class (Declarative Model) ---
class Product(Base):
    __tablename__ = "products"  # The actual name of the table in the database

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Numeric(10, 2))

# This line tells SQLAlchemy to create the table if it doesn't already exist.
Base.metadata.create_all(bind=engine)


# --- 3. Perform CRUD Operations using the ORM ---
db_session = SessionLocal()

try:
    print("--- Performing CRUD with SQLAlchemy ---")

    # CREATE: Create a Python object and add it to the session.
    print("\n[CREATE] Adding new products...")
    new_product1 = Product(name="Laptop", price=1200.50)
    new_product2 = Product(name="Mouse", price=25.00)
    db_session.add(new_product1)
    db_session.add(new_product2)
    db_session.commit() # Commit saves the transaction to the database.
    print("Products added.")

    # READ: Query the database for objects.
    print("\n[READ] Reading all products...")
    all_products = db_session.query(Product).all()
    for product in all_products:
        print(f"  ID: {product.id}, Name: {product.name}, Price: {product.price}")

    # UPDATE: Query for an object, change its attributes, and commit.
    print("\n[UPDATE] Updating 'Laptop' price...")
    laptop_to_update = db_session.query(Product).filter(Product.name == "Laptop").first()
    if laptop_to_update:
        laptop_to_update.price = 1150.00
        db_session.commit()
        print("Laptop price updated.")

    # DELETE: Query for an object and delete it.
    print("\n[DELETE] Deleting 'Mouse'...")
    mouse_to_delete = db_session.query(Product).filter(Product.name == "Mouse").first()
    if mouse_to_delete:
        db_session.delete(mouse_to_delete)
        db_session.commit()
        print("Mouse deleted.")

    # Final READ to see changes
    print("\n[READ] Reading final product list...")
    final_products = db_session.query(Product).all()
    for product in final_products:
        print(f"  ID: {product.id}, Name: {product.name}, Price: {product.price}")


except Exception as e:
    print(f"❌ An error occurred: {e}")
    db_session.rollback() # Roll back the transaction on error

finally:
    db_session.close()
    print("\n🔌 Database session closed.")