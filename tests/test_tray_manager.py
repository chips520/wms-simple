import unittest
import sys
import os

# Ensure the root directory is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tray_manager import TrayManager
from models import MaterialTray # Needed for type checking

class TestTrayManager(unittest.TestCase):
    def setUp(self):
        self.tm = TrayManager()

    def test_create_tray(self):
        self.assertTrue(self.tm.create_tray("AGV1", 5))
        self.assertIn("AGV1", self.tm._trays) # Accessing internal for verification
        self.assertIsInstance(self.tm._trays["AGV1"], MaterialTray)
        self.assertEqual(self.tm._trays["AGV1"].name, "AGV1")
        self.assertEqual(self.tm._trays["AGV1"].capacity, 5)
        self.assertFalse(self.tm.create_tray("AGV1", 10)) # Name conflict

    def test_get_tray(self):
        self.tm.create_tray("AGV1", 5)
        tray = self.tm.get_tray("AGV1")
        self.assertIsNotNone(tray)
        self.assertEqual(tray.name, "AGV1")
        self.assertIsNone(self.tm.get_tray("UNKNOWN"))

    def test_update_tray_name(self):
        self.tm.create_tray("AGV1", 5)
        self.assertTrue(self.tm.update_tray_name("AGV1", "AGV_NEW"))
        self.assertNotIn("AGV1", self.tm._trays)
        self.assertIn("AGV_NEW", self.tm._trays)
        self.assertEqual(self.tm._trays["AGV_NEW"].name, "AGV_NEW") # Check name attribute in object
        self.assertEqual(self.tm.get_tray("AGV_NEW").name, "AGV_NEW")


        self.assertFalse(self.tm.update_tray_name("NONEXISTENT", "OTHER")) # Old name does not exist
        self.tm.create_tray("AGV2", 3)
        self.assertFalse(self.tm.update_tray_name("AGV_NEW", "AGV2")) # New name conflict
        # Ensure original name is still there after failed update due to conflict
        self.assertIn("AGV_NEW", self.tm._trays)


    def test_delete_tray(self):
        self.tm.create_tray("AGV1", 5)
        self.assertTrue(self.tm.delete_tray("AGV1"))
        self.assertNotIn("AGV1", self.tm._trays)
        self.assertFalse(self.tm.delete_tray("AGV1")) # Already deleted, should return False

    def test_list_trays(self):
        self.assertEqual(self.tm.list_trays(), [])
        self.tm.create_tray("AGV1", 5)
        self.tm.create_tray("TB1", 10)
        # Order is not guaranteed by dict keys, so use assertCountEqual
        self.assertCountEqual(self.tm.list_trays(), ["AGV1", "TB1"])

if __name__ == '__main__':
    unittest.main()
