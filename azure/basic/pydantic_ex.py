from pydantic import BaseModel, ValidationError

# --- 1. Define the "shape" of your data using a Pydantic model ---
# This class defines the rules: id must be an integer, name a string, etc.
class Product(BaseModel):
    id: int
    name: str
    price: float

# --- 2. Create some raw data (e.g., from an API or user input) ---
# This data is valid and matches our model's rules.
valid_data = {
    "id": 123,
    "name": "Smartphone",
    "price": 599.99
}

# This data is invalid because the price is not a valid number.
invalid_data = {
    "id": 456,
    "name": "Book",
    "price": "twenty dollars" # This will cause an error
}

# --- 3. Use the model to validate the data ---
print("--- Testing Valid Data ---")
try:
    # We pass the dictionary to the model.
    # If the data is valid, Pydantic creates an instance of the class.
    product_instance = Product(**valid_data)
    print("✅ Validation successful!")
    print("Created Product object:", product_instance)
    print("Accessing data like an object:", product_instance.name)
except ValidationError as e:
    print("❌ Validation failed!")
    print(e)

print("\n--- Testing Invalid Data ---")
try:
    # Pydantic will check the invalid data and raise a ValidationError.
    invalid_product = Product(**invalid_data)
except ValidationError as e:
    print("❌ Validation failed, as expected!")
    # Pydantic gives you a clear, human-readable error message.
    print(e)