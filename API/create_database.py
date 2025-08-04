#!/usr/bin/env python3
"""
Script to create the PostgreSQL database for FastAPI application.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create the fastapidb database if it doesn't exist."""
    
    # Connection parameters for connecting to PostgreSQL server (not specific database)
    conn_params = {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'ujwal',  # Your password from the connection string
        'port': 5432
    }
    
    try:
        # Connect to PostgreSQL server (to postgres database by default)
        print("Connecting to PostgreSQL server...")
        connection = psycopg2.connect(**conn_params)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Create a cursor
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'fastapidb'")
        exists = cursor.fetchone()
        
        if exists:
            print("Database 'fastapidb' already exists!")
        else:
            # Create the database
            print("Creating database 'fastapidb'...")
            cursor.execute('CREATE DATABASE fastapidb')
            print("Database 'fastapidb' created successfully!")
        
        # Close cursor and connection
        cursor.close()
        connection.close()
        print("Connection closed.")
        
    except psycopg2.Error as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_database()
