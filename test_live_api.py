#!/usr/bin/env python3
"""
Test your live API deployment on Render
"""

import requests
import json

# Your actual live Render URL
API_BASE = "https://tibetan-wisdom-api.onrender.com"

def test_endpoint(endpoint, description):
    """Test a single endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"🔗 URL: {API_BASE}{endpoint}")
    
    try:
        response = requests.get(f"{API_BASE}{endpoint}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if endpoint == "/wisdom/random":
                wisdom = data.get("wisdom", {})
                print(f"✨ Wisdom: \"{wisdom.get('text', 'N/A')[:100]}...\"")
                print(f"👤 Author: {wisdom.get('author', 'N/A')}")
            elif endpoint == "/health":
                print(f"🏥 Status: {data.get('status', 'N/A')}")
                print(f"📚 Total wisdom: {data.get('total_wisdom', 'N/A')}")
            else:
                print(f"📄 Response keys: {list(data.keys())}")
            print("✅ Success!")
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"📄 Response: {response.text[:200]}")
            
    except requests.exceptions.RequestException as e:
        print(f"💥 Connection error: {e}")

def main():
    print("🚀 Testing Live Tibetan Wisdom API")
    print("=" * 50)
    
    print(f"🌐 API Base URL: {API_BASE}")
    print("🎯 Testing your live deployment!")
    
    # Test key endpoints
    test_endpoint("/health", "Health Check")
    test_endpoint("/wisdom/random", "Random Wisdom")
    test_endpoint("/wisdom?per_page=2", "Wisdom Listing")
    test_endpoint("/wisdom/categories", "Categories")
    test_endpoint("/wisdom/search?q=wisdom&per_page=1", "Search")
    
    print("\n" + "=" * 50)
    print("🎉 Testing complete!")
    print(f"🌐 Visit your live API: {API_BASE}")
    print(f"📖 API Documentation: {API_BASE}/docs")
    print("💼 Perfect for showing recruiters!")
    print("\n🔗 Share these links:")
    print(f"   Landing Page: {API_BASE}")
    print(f"   API Docs: {API_BASE}/docs")
    print(f"   Random Wisdom: {API_BASE}/wisdom/random")

if __name__ == "__main__":
    main()