# Service Inventory Checker

A Python tool that validates a JSON service inventory.

## Validation rules

- The inventory must be a list.
- Each service must be an object.
- Required fields: name, owner, region, replicas.
- Allowed region: eu-west-1.
- Replicas must be an integer of at least 1.

## Run

From the week-04 folder:

```bash
python svc_check.py
```

The script reads inventory.json from the same folder as svc_check.py.

## Example output

```text
api: PASS
worker: PASS
Summary: 2 services, 2 passed, 0 failed
```

## Exit codes

- 0: All services passed validation.
- 1: Inventory loading, structure validation, or service validation failed.

## Manual tests performed

- Valid services.
- Missing required fields.
- Zero replicas.
- Replicas supplied as text.
- Disallowed region.
- Multiple services with mixed results.
- Missing inventory file.
- Invalid JSON.
- Incorrect outer inventory structure.
- Incorrect service-item structure.