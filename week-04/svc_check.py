import json
import sys
from pathlib import Path


ALLOWED_REGIONS = {"eu-west-1"}
REQUIRED_FIELDS = {"name" ,"owner", "region" ,"replicas"}

class InventoryError(Exception):
    pass

def validate_service(service:dict) -> list[str]:

    problems = []

    missing = REQUIRED_FIELDS - service.keys()

    for fields in sorted(missing):
        problems.append(f"Missing fields: {fields}")

    if "replicas" in service:
        replicas = service["replicas"]

        if type(replicas) is not int or replicas < 1:
            problems.append("Replicas must be an integer of at least 1")

    if "region" in service:
        if service["region"] not in ALLOWED_REGIONS:
            problems.append("REGION IS NOT ALLOWED")

    return problems


def load_inventory(path: Path) -> list:
    try:
            with path.open(encoding="utf-8") as file:
                services = json.load(file)
    except FileNotFoundError as exc:
        raise InventoryError(
        f"Inventory file not found: {path.name}"
        )from exc
    except json.JSONDecodeError as exc:
        raise InventoryError(
            f"Invalid JSON in inventory file: {path.name}"
        )from exc
    if not isinstance(services, list):
        raise InventoryError("Inventory must be a list of services")
    for index, service in enumerate(services):
        if not isinstance(service, dict):
            raise InventoryError(
                f"Service at index {index} must be an object"
            )


    return services


inventory_path = Path(__file__).parent / "inventory.json"

try:

    services = load_inventory(inventory_path)
except InventoryError as exc:
    print(exc)
    sys.exit(1)
else:
    passed = 0
    failed = 0


    for service in services:
        problems = validate_service(service)
        name = service.get("name" ,"unnamed")
        if problems:
            failed += 1
            print(f"{name}: FAIL - {problems}")
        else:
            passed += 1
            print(f"{name}: PASS")
    print(f"Summary: {passed + failed} services, {passed} passed, {failed} failed")
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)