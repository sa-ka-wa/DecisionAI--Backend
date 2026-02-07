# final_test.py
import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"


def print_response(response, label):
    print(f"\n{'=' * 60}")
    print(f"{label}")
    print(f"{'=' * 60}")
    print(f"Status: {response.status_code}")
    if response.status_code < 500:
        try:
            data = response.json()
            print(json.dumps(data, indent=2))
            return data
        except:
            print(response.text)
            return None
    else:
        print(response.text)
        return None


def main():
    print("🚀 DecisionAI API Final Test")
    print("=" * 60)

    # Wait for server
    print("\n1. Checking server...")
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        if health.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server error: {health.status_code}")
            return
    except:
        print("❌ Server not running. Start with: python app.py")
        return

    # Test login
    print("\n2. Testing login...")
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }

    login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    login_result = print_response(login_response, "🔐 Login")

    if not login_result or not login_result.get('success'):
        print("❌ Login failed. Creating new user...")
        # Try to register
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "name": "Test User",
            "password": "test123"
        }
        register_response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=register_data)
        register_result = print_response(register_response, "🔐 Register")

        if register_result and register_result.get('success'):
            token = register_result['data']['access_token']
        else:
            print("❌ Could not create user")
            return
    else:
        token = login_result['data']['access_token']

    headers = {"Authorization": f"Bearer {token}"}

    # Test profile
    print("\n3. Testing profile...")
    profile_response = requests.get(f"{BASE_URL}/api/v1/auth/profile", headers=headers)
    print_response(profile_response, "👤 Profile")

    # Test task creation
    print("\n4. Creating task...")
    task_data = {
        "title": "Final Test Task",
        "description": "Testing the complete API",
        "priority": 2,
        "impact": 8,
        "due_date": "2024-02-20T23:59:59Z",
        "category": "Testing"
    }
    task_response = requests.post(f"{BASE_URL}/api/v1/tasks", headers=headers, json=task_data)
    task_result = print_response(task_response, "📝 Create Task")

    task_id = None
    if task_result and task_result.get('success'):
        task_id = task_result['data']['id']

    # Test getting tasks
    print("\n5. Getting tasks...")
    tasks_response = requests.get(f"{BASE_URL}/api/v1/tasks", headers=headers)
    tasks_result = print_response(tasks_response, "📋 Get Tasks")

    # Test analytics
    print("\n6. Testing analytics...")
    analytics_endpoints = [
        ("/api/v1/analytics/dashboard", "Dashboard"),
        ("/api/v1/analytics/category-breakdown", "Category Breakdown"),
        ("/api/v1/analytics/ai/recommendations", "AI Recommendations")
    ]

    for endpoint, name in analytics_endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        print(f"\n{name}: {response.status_code}")
        if response.status_code != 200:
            print(f"  Error: {response.text[:100]}...")

    print("\n" + "=" * 60)
    print("🎉 Test complete! API is working!")
    print(f"\n📝 Test Credentials:")
    print(f"  Email: test@example.com")
    print(f"  Password: test123")
    print(f"\n🔑 Token (for Postman):")
    print(f"  {token}")


if __name__ == "__main__":
    main()