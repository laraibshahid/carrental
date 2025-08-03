#!/usr/bin/env python3
"""
Test script for vehicle management endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def login_and_get_token():
    """Login and get access token"""
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=data)
    if response.status_code == 200:
        return response.json()['data']['tokens']['access']
    return None

def test_create_vehicle(access_token):
    """Test vehicle creation"""
    print("Testing vehicle creation...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2022,
        "license_plate": "ABC123",
        "vehicle_type": "sedan",
        "fuel_type": "petrol",
        "transmission": "automatic",
        "engine_size": 2.5,
        "mileage": 15000,
        "daily_rate": 50.00,
        "weekly_rate": 300.00,
        "monthly_rate": 1200.00,
        "color": "Silver",
        "seats": 5,
        "description": "Comfortable sedan for daily use"
    }
    
    response = requests.post(f"{BASE_URL}/vehicles/", json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 201 else None

def test_list_vehicles(access_token):
    """Test vehicle listing"""
    print("Testing vehicle listing...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/vehicles/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 200 else None

def test_get_vehicle_detail(access_token, vehicle_id):
    """Test vehicle detail retrieval"""
    print(f"Testing vehicle detail for ID: {vehicle_id}...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/vehicles/{vehicle_id}/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 200 else None

def test_update_vehicle(access_token, vehicle_id):
    """Test vehicle update"""
    print(f"Testing vehicle update for ID: {vehicle_id}...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "daily_rate": 55.00,
        "description": "Updated description - Comfortable sedan for daily use"
    }
    
    response = requests.patch(f"{BASE_URL}/vehicles/{vehicle_id}/", json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 200 else None

def test_search_vehicles(access_token):
    """Test vehicle search"""
    print("Testing vehicle search...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Test search with filters
    params = {
        "vehicle_type": "sedan",
        "search": "Toyota"
    }
    
    response = requests.get(f"{BASE_URL}/vehicles/search/", headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 200 else None

if __name__ == "__main__":
    print("🚗 Car Rental API Vehicle Management Tests")
    print("=" * 50)
    
    # Login and get token
    access_token = login_and_get_token()
    if not access_token:
        print("❌ Failed to get access token")
        exit(1)
    
    print("✅ Login successful")
    
    # Test vehicle creation
    create_result = test_create_vehicle(access_token)
    
    # Test vehicle listing
    list_result = test_list_vehicles(access_token)
    
    # Test vehicle detail if creation was successful
    if create_result and 'data' in create_result:
        vehicle_id = create_result['data']['id']
        test_get_vehicle_detail(access_token, vehicle_id)
        test_update_vehicle(access_token, vehicle_id)
    
    # Test vehicle search
    test_search_vehicles(access_token)
    
    print("✅ Vehicle management tests completed!") 