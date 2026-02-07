# test_all_improved.py
import requests
import json
import sys

BASE_URL = "http://localhost:5000"


class DecisionAITester:
    def __init__(self):
        self.access_token = None
        self.user_id = None
        self.task_id = None

    def print_response(self, response, label):
        """Print formatted response"""
        print(f"\n{'=' * 60}")
        print(f"{label}")
        print(f"{'=' * 60}")
        print(f"Status: {response.status_code}")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            return data
        except:
            print(f"Response: {response.text}")
            return None

    def test_health(self):
        """Test health endpoint"""
        response = requests.get(f"{BASE_URL}/health")
        return self.print_response(response, "🏥 Health Check")

    def test_register_or_login(self):
        """Try to register, if user exists, login instead"""
        print("\n" + "=" * 60)
        print("🔐 Testing Authentication")
        print("=" * 60)

        # Try to register first
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "name": "Test User",
            "password": "password123"
        }

        register_response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=register_data)

        if register_response.status_code == 201:
            print("✅ New user registered")
            data = register_response.json()
            self.access_token = data['data']['access_token']
            self.user_id = data['data']['user']['id']
            return True
        elif register_response.status_code == 400 and "already exists" in register_response.text:
            print("⚠️  User already exists, trying login...")

            # Try to login instead
            login_data = {
                "email": "test@example.com",
                "password": "password123"
            }

            login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
            data = self.print_response(login_response, "🔐 Login")

            if login_response.status_code == 200:
                self.access_token = data['data']['access_token']
                self.user_id = data['data']['user']['id']
                print("✅ Login successful")
                return True
            else:
                print("❌ Login failed")
                return False
        else:
            print("❌ Registration failed")
            self.print_response(register_response, "🔐 Register")
            return False

    def test_profile(self):
        """Test getting user profile"""
        if not self.access_token:
            print("❌ No access token available")
            return False

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{BASE_URL}/api/v1/auth/profile", headers=headers)
        data = self.print_response(response, "👤 User Profile")

        return response.status_code == 200

    def test_create_task(self):
        """Test creating a task"""
        if not self.access_token:
            print("❌ No access token available")
            return False

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        task_data = {
            "title": "Complete API Testing Suite",
            "description": "Test all API endpoints thoroughly",
            "category": "Testing",
            "priority": 2,
            "impact": 9,
            "due_date": "2024-02-25T23:59:59Z",
            "tags": ["api", "testing", "backend"]
        }

        response = requests.post(f"{BASE_URL}/api/v1/tasks", headers=headers, json=task_data)
        data = self.print_response(response, "📝 Create Task")

        if response.status_code == 201:
            self.task_id = data['data']['id']
            return True
        return False

    def test_get_tasks(self):
        """Test getting tasks"""
        if not self.access_token:
            print("❌ No access token available")
            return False

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{BASE_URL}/api/v1/tasks", headers=headers)
        self.print_response(response, "📋 Get All Tasks")

        return response.status_code == 200

    def test_dashboard(self):
        """Test dashboard analytics"""
        if not self.access_token:
            print("❌ No access token available")
            return False

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{BASE_URL}/api/v1/analytics/dashboard", headers=headers)
        self.print_response(response, "📊 Dashboard Analytics")

        return response.status_code == 200

    def test_category_breakdown(self):
        """Test category breakdown"""
        if not self.access_token:
            print("❌ No access token available")
            return False

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{BASE_URL}/api/v1/analytics/category-breakdown", headers=headers)
        self.print_response(response, "📊 Category Breakdown")

        return response.status_code == 200

    def test_ai_recommendations(self):
        """Test AI recommendations"""
        if not self.access_token:
            print("❌ No access token available")
            return False

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{BASE_URL}/api/v1/analytics/ai/recommendations", headers=headers)
        self.print_response(response, "🤖 AI Recommendations")

        return response.status_code == 200

    def test_all_endpoints(self):
        """Test all endpoints"""
        print("🧪 Starting Complete DecisionAI API Tests")
        print("=" * 60)

        # Test health
        self.test_health()

        # Test authentication
        if not self.test_register_or_login():
            print("❌ Authentication failed, stopping tests")
            return

        # Test authenticated endpoints
        tests = [
            ("Profile", self.test_profile),
            ("Create Task", self.test_create_task),
            ("Get Tasks", self.test_get_tasks),
            ("Dashboard", self.test_dashboard),
            ("Category Breakdown", self.test_category_breakdown),
            ("AI Recommendations", self.test_ai_recommendations)
        ]

        results = []

        for test_name, test_func in tests:
            try:
                success = test_func()
                results.append((test_name, success, "✅" if success else "❌"))
            except Exception as e:
                results.append((test_name, False, f"❌ Error: {e}"))

        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)

        for test_name, success, status in results:
            print(f"{status} {test_name}")

        passed = sum(1 for _, success, _ in results if success)
        total = len(results)

        print(f"\n🎯 Results: {passed}/{total} tests passed")

        if passed == total:
            print("✅ All tests passed! Your API is fully functional!")
        else:
            print("⚠️ Some tests failed. Check the logs above.")


if __name__ == "__main__":
    tester = DecisionAITester()
    tester.test_all_endpoints()