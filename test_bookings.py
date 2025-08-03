#!/usr/bin/env python3
"""
Test script for booking management endpoints
"""
import requests
import json
from datetime import datetime, timedelta

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

def get_available_vehicle(access_token):
    """Get an available vehicle for booking"""
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/vehicles/search/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['results']['data']:
            return data['results']['data'][0]['id']
    return None

def test_create_booking(access_token, vehicle_id):
    """Test booking creation"""
    print("Testing booking creation...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Set dates for tomorrow and day after tomorrow
    tomorrow = datetime.now() + timedelta(days=1)
    day_after = datetime.now() + timedelta(days=2)
    
    data = {
        "vehicle_id": vehicle_id,
        "start_date": tomorrow.isoformat(),
        "end_date": day_after.isoformat(),
        "pickup_location": "Lahore Airport",
        "return_location": "Lahore Airport",
        "notes": "Airport pickup and return"
    }
    
    response = requests.post(f"{BASE_URL}/bookings/", json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 201 else None

def test_list_bookings(access_token):
    """Test booking listing"""
    print("Testing booking listing...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/bookings/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 200 else None

def test_get_booking_detail(access_token, booking_id):
    """Test booking detail retrieval"""
    print(f"Testing booking detail for ID: {booking_id}...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/bookings/{booking_id}/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 200 else None

def test_confirm_booking(access_token, booking_id):
    """Test booking confirmation"""
    print(f"Testing booking confirmation for ID: {booking_id}...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{BASE_URL}/bookings/{booking_id}/confirm/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 200 else None

def test_cancel_booking(access_token, booking_id):
    """Test booking cancellation"""
    print(f"Testing booking cancellation for ID: {booking_id}...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "cancellation_reason": "Change of plans"
    }
    
    response = requests.post(f"{BASE_URL}/bookings/{booking_id}/cancel/", json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 200 else None

def test_search_bookings(access_token):
    """Test booking search"""
    print("Testing booking search...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Test search with filters
    params = {
        "status": "pending",
        "from": "2024-01-01"
    }
    
    response = requests.get(f"{BASE_URL}/bookings/search/", headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json() if response.status_code == 200 else None

if __name__ == "__main__":
    print("🚗 Car Rental API Booking Management Tests")
    print("=" * 50)
    
    # Login and get token
    access_token = login_and_get_token()
    if not access_token:
        print("❌ Failed to get access token")
        exit(1)
    
    print("✅ Login successful")
    
    # Get available vehicle
    vehicle_id = get_available_vehicle(access_token)
    if not vehicle_id:
        print("❌ No available vehicles found")
        exit(1)
    
    print(f"✅ Found available vehicle ID: {vehicle_id}")
    
    # Test booking creation
    create_result = test_create_booking(access_token, vehicle_id)
    
    # Test booking listing
    list_result = test_list_bookings(access_token)
    
    # Test booking detail if creation was successful
    if create_result and 'data' in create_result:
        booking_id = create_result['data']['id']
        test_get_booking_detail(access_token, booking_id)
        test_confirm_booking(access_token, booking_id)
        # test_cancel_booking(access_token, booking_id)  # Uncomment to test cancellation
    
    # Test booking search
    test_search_bookings(access_token)
    
    print("✅ Booking management tests completed!") 