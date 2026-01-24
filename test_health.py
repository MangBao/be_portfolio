"""
Direct test of health endpoint
"""
from wsgi import app

with app.test_client() as client:
    print("\n" + "="*60)
    print("Testing /health endpoint directly")
    print("="*60)
    
    try:
        response = client.get('/health')
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Data: {response.get_json()}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
