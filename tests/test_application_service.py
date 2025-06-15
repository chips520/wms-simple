import unittest
import sys
import os

# Ensure the root directory is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application_service import MaterialManagementService
from models import DISABLED_SLOT # For checking string representations

class TestMaterialManagementService(unittest.TestCase):
    def setUp(self):
        # Each test gets a fresh service and therefore a fresh TrayManager
        self.service = MaterialManagementService()

    def test_initialize_and_list_trays(self):
        configs = {"AGV1": 5, "AGV2": 8}
        self.service.initialize_default_trays(configs)
        self.assertCountEqual(self.service.list_all_trays(), ["AGV1", "AGV2"])

        # Check details of one tray to confirm capacity
        agv1_details = self.service.get_tray_details_str("AGV1")
        self.assertIsNotNone(agv1_details)
        self.assertIn("Name: AGV1", agv1_details)
        self.assertIn("Capacity: 5", agv1_details)
        # Check that all 5 slots are initially empty
        self.assertEqual(agv1_details.count("Empty"), 5)


    def test_add_remove_tray(self):
        self.assertTrue(self.service.add_tray("TB1", 10))
        self.assertIn("TB1", self.service.list_all_trays())
        self.assertTrue(self.service.remove_tray("TB1"))
        self.assertNotIn("TB1", self.service.list_all_trays())
        self.assertFalse(self.service.remove_tray("TB1")) # Not found, should be False

    def test_get_tray_details_str(self):
        self.service.add_tray("FL1", 3)
        details = self.service.get_tray_details_str("FL1")
        self.assertIsNotNone(details)
        self.assertIn("FL1", details)
        self.assertIn("Capacity: 3", details)
        self.assertIsNone(self.service.get_tray_details_str("UNKNOWN"))

    def test_find_sample_location(self):
        self.service.add_tray("T1", 3)
        # Need to place a sample first using the service methods
        self.service.place_sample_in_slot("T1", 0, "sampleA")

        location = self.service.find_sample_location("T1", "sampleA")
        self.assertIsNotNone(location)
        self.assertEqual(location['tray_name'], "T1")
        self.assertEqual(location['slot_index'], 0)

        self.assertIsNone(self.service.find_sample_location("T1", "sampleB")) # Not found in tray
        self.assertIsNone(self.service.find_sample_location("T_NONEXIST", "sampleA")) # Tray not found

    def test_get_available_slot(self):
        self.service.add_tray("T2", 1)
        available = self.service.get_available_slot("T2")
        self.assertIsNotNone(available)
        self.assertEqual(available['tray_name'], "T2")
        self.assertEqual(available['slot_index'], 0)

        self.service.place_sample_in_slot("T2", 0, "sX")
        self.assertIsNone(self.service.get_available_slot("T2")) # Tray full
        self.assertIsNone(self.service.get_available_slot("T_NONEXIST")) # Tray not found

    def test_place_sample_in_slot(self):
        self.service.add_tray("T3", 2)
        self.assertTrue(self.service.place_sample_in_slot("T3", 0, "sY"))
        details = self.service.get_tray_details_str("T3")
        self.assertIn("Sample: sY", details)

        self.assertFalse(self.service.place_sample_in_slot("T3", 0, "sZ")) # Occupied
        self.assertFalse(self.service.place_sample_in_slot("T3", 2, "sW")) # Invalid index
        self.assertFalse(self.service.place_sample_in_slot("T_NONEXIST", 0, "sV")) # Tray not found

    def test_place_sample_in_available_slot(self):
        self.service.add_tray("T4", 1)
        location = self.service.place_sample_in_available_slot("T4", "sP")
        self.assertIsNotNone(location)
        self.assertEqual(location['slot_index'], 0)
        details = self.service.get_tray_details_str("T4")
        self.assertIn("Sample: sP", details)

        self.assertIsNone(self.service.place_sample_in_available_slot("T4", "sQ")) # Tray full

        self.assertIsNone(self.service.place_sample_in_available_slot("T_NONEXIST", "sR")) # Tray not found

    def test_clear_sample_from_slot(self):
        self.service.add_tray("T5", 1)
        self.service.place_sample_in_slot("T5", 0, "sA")
        self.assertTrue(self.service.clear_sample_from_slot("T5", 0))
        details = self.service.get_tray_details_str("T5")
        self.assertIn("Slot 0: Empty", details)

        self.assertFalse(self.service.clear_sample_from_slot("T5", 1)) # Invalid index
        self.assertFalse(self.service.clear_sample_from_slot("T_NONEXIST", 0)) # Tray not found

    def test_disable_tray_slot(self):
        self.service.add_tray("T6", 2)
        self.assertTrue(self.service.disable_tray_slot("T6", 0))
        details = self.service.get_tray_details_str("T6")
        self.assertIn(f"Slot 0: {DISABLED_SLOT}", details)

        self.assertFalse(self.service.disable_tray_slot("T6", 2)) # Invalid index
        self.assertFalse(self.service.disable_tray_slot("T_NONEXIST", 0)) # Tray not found

    def test_enable_tray_slot(self):
        self.service.add_tray("T7", 2)
        self.service.disable_tray_slot("T7", 0) # Disable first
        self.assertTrue(self.service.enable_tray_slot("T7", 0))
        details = self.service.get_tray_details_str("T7")
        self.assertIn("Slot 0: Empty", details) # Becomes empty

        # Test enabling an already empty slot
        self.assertTrue(self.service.enable_tray_slot("T7", 1))
        details_after_enable_empty = self.service.get_tray_details_str("T7")
        self.assertIn("Slot 1: Empty", details_after_enable_empty)


        self.assertFalse(self.service.enable_tray_slot("T7", 2)) # Invalid index
        self.assertFalse(self.service.enable_tray_slot("T_NONEXIST", 0)) # Tray not found

if __name__ == '__main__':
    unittest.main()
