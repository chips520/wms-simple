import unittest
import sys
import os

# Ensure the root directory is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Slot, MaterialTray, DISABLED_SLOT

class TestSlot(unittest.TestCase):
    def test_slot_creation_and_states(self):
        s_empty = Slot()
        self.assertIsNone(s_empty.sample_id)
        self.assertTrue(s_empty.is_empty())
        self.assertFalse(s_empty.is_disabled())
        self.assertEqual(repr(s_empty), "Empty")

        s_filled = Slot("sample1")
        self.assertEqual(s_filled.sample_id, "sample1")
        self.assertFalse(s_filled.is_empty())
        self.assertFalse(s_filled.is_disabled())
        self.assertEqual(repr(s_filled), "Sample: sample1")

        # Create a slot and then disable it to test repr of disabled
        s_to_disable = Slot()
        s_to_disable.disable()
        self.assertEqual(s_to_disable.sample_id, DISABLED_SLOT)
        self.assertFalse(s_to_disable.is_empty()) # is_empty is strictly for None
        self.assertTrue(s_to_disable.is_disabled())
        self.assertEqual(repr(s_to_disable), DISABLED_SLOT)

    def test_slot_operations(self):
        s = Slot()
        s.assign_sample("sample2")
        self.assertEqual(s.sample_id, "sample2")

        s.disable()
        self.assertTrue(s.is_disabled())

        s.clear()
        self.assertTrue(s.is_empty())
        self.assertIsNone(s.sample_id)

class TestMaterialTray(unittest.TestCase):
    def setUp(self):
        self.tray = MaterialTray("T1", 3)

    def test_tray_creation(self):
        self.assertEqual(self.tray.name, "T1")
        self.assertEqual(self.tray.capacity, 3)
        self.assertEqual(len(self.tray.slots), 3)
        for slot in self.tray.slots:
            self.assertTrue(slot.is_empty())
        self.assertEqual(repr(self.tray), "MaterialTray(Name: T1, Capacity: 3, Slots: [Slot 0: Empty, Slot 1: Empty, Slot 2: Empty])")

    def test_place_sample(self):
        self.assertTrue(self.tray.place_sample(0, "s1"))
        self.assertEqual(self.tray.slots[0].sample_id, "s1")
        self.assertFalse(self.tray.place_sample(0, "s2")) # Occupied
        self.assertFalse(self.tray.place_sample(3, "s3")) # Invalid index

        self.tray.slots[1].disable()
        self.assertFalse(self.tray.place_sample(1, "s4")) # Disabled

    def test_clear_slot(self):
        self.tray.place_sample(0, "s1")
        self.assertTrue(self.tray.clear_slot(0))
        self.assertTrue(self.tray.slots[0].is_empty())
        self.assertFalse(self.tray.clear_slot(3)) # Invalid index

    def test_disable_enable_slot(self):
        self.assertTrue(self.tray.disable_slot(0))
        self.assertTrue(self.tray.slots[0].is_disabled())

        self.assertTrue(self.tray.enable_slot(0))
        self.assertTrue(self.tray.slots[0].is_empty()) # Disabled slot becomes empty

        self.tray.place_sample(1, "s1")
        self.assertTrue(self.tray.enable_slot(1)) # Occupied, not disabled, remains occupied
        self.assertEqual(self.tray.slots[1].sample_id, "s1")

        self.assertTrue(self.tray.enable_slot(2)) # Already empty, remains empty
        self.assertTrue(self.tray.slots[2].is_empty())

        self.assertFalse(self.tray.disable_slot(3)) # Invalid index
        self.assertFalse(self.tray.enable_slot(3))  # Invalid index

    def test_find_sample(self):
        self.tray.place_sample(0, "s1")
        self.tray.place_sample(2, "s2")
        self.assertEqual(self.tray.find_sample("s1"), 0)
        self.assertEqual(self.tray.find_sample("s2"), 2)
        self.assertIsNone(self.tray.find_sample("s3"))

    def test_get_available_slot_index(self):
        self.assertEqual(self.tray.get_available_slot_index(), 0)
        self.tray.place_sample(0, "s1")
        self.assertEqual(self.tray.get_available_slot_index(), 1)
        self.tray.place_sample(1, "s2")
        self.tray.place_sample(2, "s3")
        self.assertIsNone(self.tray.get_available_slot_index()) # Full

if __name__ == '__main__':
    unittest.main()
