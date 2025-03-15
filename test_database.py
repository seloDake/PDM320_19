from models.db import get_db

try:
    conn = get_db()
    print("Database connection successful!")
    conn.close()
except Exception as e:
    print(f"Database connection failed: {e}")
