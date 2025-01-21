import json

with open("db_export.json", "r", encoding="utf-8") as file:
    try:
        data = json.load(file)
        print("JSON is valid!")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")