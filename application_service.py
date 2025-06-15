from tray_manager import TrayManager
from models import MaterialTray # DISABLED_SLOT is not directly used by this service's logic

class MaterialManagementService:
    def __init__(self):
        self.tray_manager = TrayManager()

    def initialize_default_trays(self, default_tray_configs: dict[str, int]):
        for name, capacity in default_tray_configs.items():
            success = self.tray_manager.create_tray(name, capacity)
            if success:
                print(f"Successfully created tray: {name} with capacity {capacity}")
            else:
                # Error message is already printed by tray_manager.create_tray
                print(f"Failed to create tray: {name}")


    def add_tray(self, name: str, capacity: int) -> bool:
        return self.tray_manager.create_tray(name, capacity)

    def get_tray_details_str(self, tray_name: str) -> str | None:
        tray = self.tray_manager.get_tray(tray_name)
        if tray is None:
            return None
        return str(tray) # Relies on MaterialTray.__repr__

    def remove_tray(self, name: str) -> bool:
        return self.tray_manager.delete_tray(name)

    def list_all_trays(self) -> list[str]:
        return self.tray_manager.list_trays()

    def find_sample_location(self, tray_name: str, sample_id: str) -> dict | None:
        tray = self.tray_manager.get_tray(tray_name)
        if tray is None:
            # Optionally print an error or let the caller handle None
            # print(f"Error: Tray '{tray_name}' not found.")
            return None

        slot_index = tray.find_sample(sample_id)
        if slot_index is not None:
            return {'tray_name': tray_name, 'slot_index': slot_index}
        else:
            return None

    def get_available_slot(self, tray_name: str) -> dict | None:
        tray = self.tray_manager.get_tray(tray_name)
        if tray is None:
            # print(f"Error: Tray '{tray_name}' not found.")
            return None

        slot_index = tray.get_available_slot_index()
        if slot_index is not None:
            return {'tray_name': tray_name, 'slot_index': slot_index}
        else:
            return None

    def place_sample_in_slot(self, tray_name: str, slot_index: int, sample_id: str) -> bool:
        tray = self.tray_manager.get_tray(tray_name)
        if tray is None:
            print(f"Error: Tray '{tray_name}' not found for placing sample.")
            return False
        return tray.place_sample(slot_index, sample_id)

    def place_sample_in_available_slot(self, tray_name: str, sample_id: str) -> dict | None:
        location_info = self.get_available_slot(tray_name)
        if location_info is None:
            # This means either tray not found or no available slot
            # get_available_slot or underlying get_tray would have printed an error if tray not found
            # or MaterialTray.get_available_slot_index returned None
            print(f"Info: No available slot in tray '{tray_name}' or tray not found.")
            return None

        # slot_index = location_info['slot_index'] # This is already available in location_info

        success = self.place_sample_in_slot(tray_name, location_info['slot_index'], sample_id)

        if success:
            return location_info
        else:
            # place_sample_in_slot or underlying tray.place_sample would have printed an error
            print(f"Info: Failed to place sample '{sample_id}' in tray '{tray_name}', slot {location_info['slot_index']}.")
            return None

    def clear_sample_from_slot(self, tray_name: str, slot_index: int) -> bool:
        tray = self.tray_manager.get_tray(tray_name)
        if tray is None:
            print(f"Error: Tray '{tray_name}' not found for clearing slot.")
            return False
        return tray.clear_slot(slot_index)

    def disable_tray_slot(self, tray_name: str, slot_index: int) -> bool:
        tray = self.tray_manager.get_tray(tray_name)
        if tray is None:
            print(f"Error: Tray '{tray_name}' not found for disabling slot.")
            return False
        return tray.disable_slot(slot_index)

    def enable_tray_slot(self, tray_name: str, slot_index: int) -> bool:
        tray = self.tray_manager.get_tray(tray_name)
        if tray is None:
            print(f"Error: Tray '{tray_name}' not found for enabling slot.")
            return False
        return tray.enable_slot(slot_index)
