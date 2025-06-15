from models import MaterialTray

class TrayManager:
    def __init__(self):
        self._trays: dict[str, MaterialTray] = {}

    def create_tray(self, name: str, capacity: int) -> bool:
        if name in self._trays:
            print(f"Error: Tray with name '{name}' already exists.")
            return False

        tray = MaterialTray(name, capacity)
        self._trays[name] = tray
        return True

    def get_tray(self, name: str) -> MaterialTray | None:
        return self._trays.get(name)

    def update_tray_name(self, old_name: str, new_name: str) -> bool:
        if old_name not in self._trays:
            print(f"Error: Tray with name '{old_name}' not found.")
            return False

        if new_name in self._trays:
            print(f"Error: Tray with name '{new_name}' already exists.")
            return False

        tray = self._trays.pop(old_name)
        tray.name = new_name
        self._trays[new_name] = tray
        return True

    def delete_tray(self, name: str) -> bool:
        if name in self._trays:
            del self._trays[name]
            return True
        else:
            print(f"Error: Tray with name '{name}' not found.")
            return False

    def list_trays(self) -> list[str]:
        return list(self._trays.keys())
