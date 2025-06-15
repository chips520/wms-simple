DISABLED_SLOT = "#999"

class Slot:
    def __init__(self, sample_id=None):
        self.sample_id = sample_id

    def is_empty(self):
        return self.sample_id is None

    def is_disabled(self):
        return self.sample_id == DISABLED_SLOT

    def assign_sample(self, sample_id):
        self.sample_id = sample_id

    def clear(self):
        self.sample_id = None

    def disable(self):
        self.sample_id = DISABLED_SLOT

    def __repr__(self):
        if self.is_empty():
            return "Empty"
        elif self.is_disabled():
            return DISABLED_SLOT
        else:
            return f"Sample: {self.sample_id}"

class MaterialTray:
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.slots = [Slot() for _ in range(capacity)]

    def __repr__(self):
        slot_reprs = [f"Slot {i}: {repr(slot)}" for i, slot in enumerate(self.slots)]
        return f"MaterialTray(Name: {self.name}, Capacity: {self.capacity}, Slots: [{', '.join(slot_reprs)}])"

    def place_sample(self, slot_index: int, sample_id: str) -> bool:
        if not (0 <= slot_index < self.capacity):
            print(f"Error: Slot index {slot_index} is out of bounds for tray '{self.name}'.")
            return False

        slot = self.slots[slot_index]
        if slot.is_empty():
            slot.assign_sample(sample_id)
            return True
        else:
            print(f"Error: Slot {slot_index} in tray '{self.name}' is occupied or disabled.")
            return False

    def clear_slot(self, slot_index: int) -> bool:
        if not (0 <= slot_index < self.capacity):
            print(f"Error: Slot index {slot_index} is out of bounds for tray '{self.name}'.")
            return False

        slot = self.slots[slot_index]
        slot.clear()
        return True

    def disable_slot(self, slot_index: int) -> bool:
        if not (0 <= slot_index < self.capacity):
            print(f"Error: Slot index {slot_index} is out of bounds for tray '{self.name}'.")
            return False

        slot = self.slots[slot_index]
        slot.disable()
        return True

    def enable_slot(self, slot_index: int) -> bool:
        if not (0 <= slot_index < self.capacity):
            print(f"Error: Slot index {slot_index} is out of bounds for tray '{self.name}'.")
            return False

        slot = self.slots[slot_index]
        if slot.is_disabled():
            slot.clear()  # Make it empty, thus enabling it
        return True

    def find_sample(self, sample_id_to_find: str) -> int | None:
        for index, slot in enumerate(self.slots):
            if slot.sample_id == sample_id_to_find:
                return index
        return None

    def get_available_slot_index(self) -> int | None:
        for index, slot in enumerate(self.slots):
            if slot.is_empty():
                return index
        return None
