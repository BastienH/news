import json

global data
with open("checkout.json") as f:
    data = json.loads(f.read())
    
