#!/usr/bin/env python3
"""
Test script for authentication endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_registration():
    """Test user registration"""
    print("Testing user registration...")
    
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+1234567890"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 201 else None

def test_login():
    """Test user login"""
    print("Testing user login...")
    
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 200 else None

def test_profile(access_token):
    """Test profile endpoint"""
    print("Testing profile endpoint...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

if __name__ == "__main__":
    print("🚗 Car Rental API Authentication Tests")
    print("=" * 50)
    
    # Test registration
    registration_result = test_registration()
    
    # Test login
    login_result = test_login()
    
    # Test profile if login was successful
    if login_result and 'data' in login_result:
        access_token = login_result['data']['tokens']['access']
        test_profile(access_token)
    
    print("✅ Authentication tests completed!") 