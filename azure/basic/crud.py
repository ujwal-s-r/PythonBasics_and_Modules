import psycopg2
import sys
from connect import connect_db

import psycopg2
import sys

conn = connect_db()
try:
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    print("✅ Connection successful, cursor created.")

    # --- 1. CREATE Operation ---
    # We use "CREATE TABLE IF NOT EXISTS" so the script can be run multiple times.
    print("\n[CREATE] Creating table 'products' if it doesn't exist...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price NUMERIC(10, 2)
        );
    """)
    # Commit the transaction to make the change permanent
    conn.commit()
    print("Table 'products' is ready.")

    # --- 2. INSERT Operation ---
    # Note: Use %s placeholders to prevent SQL injection. NEVER use f-strings for values.
    print("\n[INSERT] Inserting new products...")
    products_to_insert = [
        ('Laptop', 1200.50),
        ('Mouse', 25.00),
        ('Keyboard', 75.99)
    ]
    cursor.executemany("INSERT INTO products (name, price) VALUES (%s, %s);", products_to_insert)
    conn.commit()
    print(f"{cursor.rowcount} products inserted.")

    # --- 3. READ (SELECT) Operation ---
    print("\n[READ] Reading all products from the table...")
    cursor.execute("SELECT id, name, price FROM products;")
    all_products = cursor.fetchall() # Fetch all rows from the query result
    for product in all_products:
        print(f"  ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")

    # --- 4. UPDATE Operation ---
    print("\n[UPDATE] Updating the price of 'Laptop'...")
    cursor.execute("UPDATE products SET price = %s WHERE name = %s;", (1150.00, 'Laptop'))
    conn.commit()
    print(f"{cursor.rowcount} row updated.")

    # --- 5. DELETE Operation ---
    print("\n[DELETE] Deleting 'Mouse' from the table...")
    cursor.execute("DELETE FROM products WHERE name = %s;", ('Mouse',))
    conn.commit()
    print(f"{cursor.rowcount} row deleted.")

    # --- Final READ to see changes ---
    print("\n[READ] Reading final product list...")
    cursor.execute("SELECT id, name, price FROM products;")
    final_products = cursor.fetchall()
    for product in final_products:
        print(f"  ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")
        
    # DROP TABLE Operation
    print("\n[DROP] Dropping table 'products'...")
    cursor.execute("DROP TABLE IF EXISTS products;")
    conn.commit()
    print("✅ Table 'products' dropped successfully.")
    

except Exception as e:
    print(f"❌ An error occurred: {e}")
    # Rollback any changes if an error occurs
    if conn:
        conn.rollback()
    sys.exit(1)

finally:
    # Close the cursor and connection
    if 'cursor' in locals() and cursor:
        cursor.close()
    if conn:
        conn.close()
    print("\n🔌 Cursor and connection closed.") 