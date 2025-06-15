# Material Management Application Service

This project implements a material management application service as per the requirements in `require.md`. It allows for the management of material trays and the samples placed within their slots.

## Project Structure

-   `require.md`: The product requirements document.
-   `models.py`: Contains the data models:
    -   `Slot`: Represents a single slot in a tray, capable of holding a sample ID, being empty, or disabled.
    -   `MaterialTray`: Represents a tray with a defined name and capacity, holding multiple `Slot` objects. Contains logic for managing slots within that tray (placing samples, clearing, disabling/enabling, finding samples, finding available slots).
-   `tray_manager.py`:
    -   `TrayManager`: Handles the creation, retrieval, updating (name), and deletion of `MaterialTray` objects. Manages a collection of trays.
-   `application_service.py`:
    -   `MaterialManagementService`: Provides a high-level API to interact with the system. It uses `TrayManager` and `MaterialTray` objects to fulfill the application requirements (e.g., initializing default trays, finding samples across trays by name, placing samples in available slots).
-   `main.py`: An example script that demonstrates the usage of the `MaterialManagementService` and its various features.
-   `tests/`: Contains unit tests for the project.
    -   `test_models.py`: Tests for `Slot` and `MaterialTray`.
    -   `test_tray_manager.py`: Tests for `TrayManager`.
    -   `test_application_service.py`: Tests for `MaterialManagementService`.

## Running the Example

To see a demonstration of the application's features, run the `main.py` script from the root directory of the project:

```bash
python main.py
```

This script will initialize some default trays, perform various operations like placing samples, querying slot states, and managing trays, printing the results to the console.

## Running Tests

To run the unit tests, navigate to the root directory of the project and execute:

```bash
python -m unittest discover tests
```
Or, for more verbose output:
```bash
python -m unittest discover -v tests
```

This will discover and run all tests in the `tests/` directory.
