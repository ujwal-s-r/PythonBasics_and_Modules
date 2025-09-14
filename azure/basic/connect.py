import psycopg2 
import sys
from dotenv import load_dotenv
load_dotenv()
import os
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
conn = None

try:
    conn = psycopg2.connect(AZURE_CONNECTION_STRING)
    print("connected to dB")
except Exception as e:
    print(e)
    sys.exit(1)
finally:
    if conn:
        conn.close()
        print("connection closed")
        
def connect_db():
    conn = psycopg2.connect(AZURE_CONNECTION_STRING)
    print("connected to dB")
    return conn