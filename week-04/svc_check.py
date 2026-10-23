import json
from pathlib import Path

ALLOWED_REGIONS = {"eu-west-1"}
REQUIRED_FIELDS = {"name" ,"owner", "region" ,"replicas"}


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

    return(problems)

service = {
    "name" : "payment-api",
    "owner" : "team-payment-api",
    "region" : "eu-west-1",
    "replicas" : "3"
}
def load_inventory(path: Path) -> list:
    with path.open(encoding="utf-8") as file:
        services = json.load(file)

    return services
inventory_path = Path(__file__).parent / "inventory.json"
services = load_inventory(inventory_path)

for service in services:
    print(validate_service(service))