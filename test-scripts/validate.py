import json
from jsonschema import validate, RefResolver

with open('../schema/constraint/policy-schema.json') as f:
    policy_schema = json.load(f)

with open('samples/usage-policy.json') as f:
    data = json.load(f)

validate(instance=data, schema=policy_schema)
print("Valid!")