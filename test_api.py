"""
Quick API test script
Tests the running API server endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"


def test_endpoint(endpoint, method="GET"):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*60}")
    print(f"Testing: {method} {url}")
    print('='*60)
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        else:
            response = requests.request(method, url, timeout=5)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            data = response.json()
            print(f"Response Body:\n{json.dumps(data, indent=2)}")
        except:
            print(f"Response Body (text):\n{response.text[:500]}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n🧪 API Testing Script")
    print("="*60)
    
    # Test endpoints
    endpoints = [
        "/",
        "/health",
        "/api/v1/about",
        "/apidocs",
    ]
    
    results = {}
    for endpoint in endpoints:
        results[endpoint] = test_endpoint(endpoint)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Summary")
    print('='*60)
    for endpoint, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {endpoint}")
    
    print(f"\n{'='*60}")
