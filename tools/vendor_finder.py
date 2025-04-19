import json

def get_mock_vendors(service_type: str, city: str) -> list:
    with open("data/vendors.json") as f:
        return json.load(f)
