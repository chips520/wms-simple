from application_service import MaterialManagementService

def demonstrate_material_management():
    print("Initializing Material Management Service...")
    service = MaterialManagementService()

    print("\n--- Initializing Default Trays ---")
    default_trays = {
        "AGV1": 5,
        "AGV2": 3,
        "TB1": 4,
        "FL1": 2
    }
    service.initialize_default_trays(default_trays)
    print("Default trays initialized.")

    print("\n--- Listing All Trays ---")
    all_trays = service.list_all_trays()
    if all_trays:
        for tray_name in all_trays:
            print(f"- {tray_name}")
    else:
        print("No trays available.")

    print("\n--- Details for Tray AGV1 ---")
    print(service.get_tray_details_str("AGV1"))

    print("\n--- Placing Samples ---")
    print(f"Placing 'sample001' in AGV1, Slot 0: {service.place_sample_in_slot('AGV1', 0, 'sample001')}")
    print(f"Placing 'sample002' in AGV1, Slot 2: {service.place_sample_in_slot('AGV1', 2, 'sample002')}")
    print(f"Placing 'sample003' in AGV2 (available): {service.place_sample_in_available_slot('AGV2', 'sample003')}")

    print("\n--- Details for Tray AGV1 (after placements) ---")
    print(service.get_tray_details_str("AGV1"))
    print("\n--- Details for Tray AGV2 (after placements) ---")
    print(service.get_tray_details_str("AGV2"))

    print("\n--- Finding Samples ---")
    location1 = service.find_sample_location("AGV1", "sample001")
    print(f"Location of 'sample001': {location1}")
    location2 = service.find_sample_location("AGV1", "sampleXYZ") # Not found
    print(f"Location of 'sampleXYZ': {location2}")

    print("\n--- Getting Available Slot ---")
    available_agv1 = service.get_available_slot("AGV1")
    print(f"Available slot in AGV1: {available_agv1}")

    # Fill AGV2 to test available slot when full
    service.place_sample_in_available_slot("AGV2", "sample004")
    service.place_sample_in_available_slot("AGV2", "sample005") # AGV2 capacity is 3
    available_agv2 = service.get_available_slot("AGV2")
    print(f"Available slot in AGV2 (should be None if full): {available_agv2}")
    print("\n--- Details for Tray AGV2 (should be full) ---")
    print(service.get_tray_details_str("AGV2"))


    print("\n--- Disabling a Slot ---")
    # AGV1, Slot 1 should be empty
    print(f"Disabling AGV1, Slot 1: {service.disable_tray_slot('AGV1', 1)}")
    print(service.get_tray_details_str("AGV1"))

    print("\n--- Attempting to place in disabled slot ---")
    print(f"Placing 'sample007' in AGV1, Slot 1 (disabled): {service.place_sample_in_slot('AGV1', 1, 'sample007')}")


    print("\n--- Enabling a Slot ---")
    print(f"Enabling AGV1, Slot 1: {service.enable_tray_slot('AGV1', 1)}")
    print(service.get_tray_details_str("AGV1"))
    print(f"Placing 'sample008' in AGV1, Slot 1 (now enabled): {service.place_sample_in_slot('AGV1', 1, 'sample008')}")
    print(service.get_tray_details_str("AGV1"))


    print("\n--- Clearing a Sample ---")
    print(f"Clearing AGV1, Slot 0 ('sample001'): {service.clear_sample_from_slot('AGV1', 0)}")
    print(service.get_tray_details_str("AGV1"))

    print("\n--- Adding a New Tray ---")
    print(f"Adding tray 'NEWTRAY' with capacity 2: {service.add_tray('NEWTRAY', 2)}")
    print(service.get_tray_details_str('NEWTRAY'))

    print("\n--- Removing a Tray ---")
    print(f"Removing tray 'FL1': {service.remove_tray('FL1')}")
    print(f"Attempting to get details for 'FL1': {service.get_tray_details_str('FL1')}")

    print("\n--- Final list of trays ---")
    for tray_name in service.list_all_trays():
        print(f"- {tray_name}")
        print(service.get_tray_details_str(tray_name))


    print("\n--- Demonstration Complete ---")

if __name__ == "__main__":
    demonstrate_material_management()
