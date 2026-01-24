"""
Test database connection with current .env configuration
"""
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

db_uri = os.getenv('FLASK_DB_URI')
print("="*60)
print("Testing Database Connection")
print("="*60)
print(f"\nDatabase URI: {db_uri[:50]}...{db_uri[-20:]}")  # Hide sensitive parts

try:
    from sqlalchemy import create_engine, text
    
    print("\n[OK] SQLAlchemy imported successfully")
    
    # Create engine
    engine = create_engine(db_uri, echo=True)
    print("\n[OK] Engine created successfully")
    
    # Test connection
    with engine.connect() as connection:
        print("\n[OK] Connection established")
        
        # Execute simple query
        result = connection.execute(text("SELECT 1"))
        print(f"\n[OK] Query executed successfully: {result.fetchone()}")
        
        # Try to query About table
        try:
            result = connection.execute(text("SELECT COUNT(*) FROM about"))
            count = result.fetchone()[0]
            print(f"\n[OK] About table accessible, row count: {count}")
        except Exception as e:
            print(f"\n[WARN] About table query failed: {e}")
    
    print("\n" + "="*60)
    print("[SUCCESS] DATABASE CONNECTION TEST PASSED!")
    print("="*60)
    
except Exception as e:
    print("\n" + "="*60)
    print("[FAILED] DATABASE CONNECTION TEST FAILED!")
    print("="*60)
    print(f"\nError: {e}")
    
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
