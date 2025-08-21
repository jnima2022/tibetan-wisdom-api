#!/usr/bin/env python3
"""
Test script to verify rate limiting is working correctly.
Run this after starting your API server to test rate limits.
"""

import requests
import time
import sys

API_BASE = "http://localhost:8000"

def test_rate_limit(endpoint, limit_per_minute, test_name):
    """Test rate limiting for a specific endpoint"""
    print(f"\n🧪 Testing {test_name}")
    print(f"📊 Expected limit: {limit_per_minute} requests per minute")
    print(f"🎯 Endpoint: {endpoint}")
    
    success_count = 0
    rate_limited_count = 0
    
    # Test rapid requests (should hit rate limit)
    print("⚡ Sending rapid requests...")
    
    for i in range(limit_per_minute + 5):  # Try to exceed the limit
        try:
            response = requests.get(f"{API_BASE}{endpoint}")
            
            if response.status_code == 200:
                success_count += 1
                print(f"✅ Request {i+1}: Success")
            elif response.status_code == 429:
                rate_limited_count += 1
                print(f"🚫 Request {i+1}: Rate limited (expected)")
                retry_after = response.headers.get('Retry-After', 'Not specified')
                print(f"   Retry-After: {retry_after}")
                break
            else:
                print(f"❌ Request {i+1}: Unexpected status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"💥 Request {i+1}: Connection error - {e}")
            return False
            
        # Small delay to avoid overwhelming
        time.sleep(0.1)
    
    print(f"\n📈 Results:")
    print(f"✅ Successful requests: {success_count}")
    print(f"🚫 Rate limited requests: {rate_limited_count}")
    
    if rate_limited_count > 0:
        print("🎉 Rate limiting is working correctly!")
        return True
    else:
        print("⚠️  Rate limiting may not be working - no 429 responses received")
        return False

def test_api_health():
    """Test if API is running"""
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print("🏥 API Health Check:")
            print(f"   Status: {data['status']}")
            print(f"   Version: {data['api_version']}")
            print(f"   Total wisdom: {data['total_wisdom']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"💥 Cannot connect to API: {e}")
        print("🔧 Make sure your API server is running on http://localhost:8000")
        return False

def main():
    print("🧪 Tibetan Wisdom API - Rate Limiting Test")
    print("=" * 50)
    
    # Check if API is running
    if not test_api_health():
        print("\n❌ API is not accessible. Please start your server first:")
        print("   python main.py")
        sys.exit(1)
    
    print("\n🚀 Starting rate limit tests...")
    
    # Test different endpoints with their limits
    tests = [
        ("/wisdom/random", 30, "Random Wisdom"),
        ("/wisdom", 20, "Wisdom Listings"),
        ("/wisdom/search?q=wisdom", 15, "Search Endpoint"),
        ("/wisdom/categories", 10, "Categories Endpoint"),
        ("/health", 5, "Health Check"),
    ]
    
    all_passed = True
    
    for endpoint, limit, name in tests:
        if not test_rate_limit(endpoint, limit, name):
            all_passed = False
        time.sleep(2)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All rate limiting tests completed!")
        print("✅ Your API is properly protected against abuse.")
    else:
        print("⚠️  Some tests showed unexpected results.")
        print("🔧 Check your rate limiting configuration.")
    
    print("\n💡 Pro tip: Rate limits reset every minute, so normal usage won't be affected!")

if __name__ == "__main__":
    main()