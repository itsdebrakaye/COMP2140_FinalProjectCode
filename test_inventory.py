import unittest
from inventory import load_inventory, save_inventory

class TestInventory(unittest.TestCase):
    def test_load_inventory(self):
        # Test with valid data
        data = load_inventory("test_data.json")
        self.assertIsInstance(data, list)

    def test_save_inventory(self):
        # Test saving and reloading inventory
        test_data = [{"name": "Test Item", "quantity": 5, "user_id": "test_user"}]
        save_inventory(test_data, "test_data.json")
        data = load_inventory("test_data.json")
        self.assertEqual(data, test_data)

if __name__ == "__main__":
    unittest.main()
