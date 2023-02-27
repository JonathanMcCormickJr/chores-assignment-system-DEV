import unittest
import sys
import os

# Add parent directory to Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# Now we can import main.py
from main import app



class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        
    def test_hello(self):
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')

if __name__ == '__main__':
    unittest.main()
