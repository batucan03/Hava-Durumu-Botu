import json
import os

DATA_FILE = "user_locations.json"

def _load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_user_location(user_id, city):
    data = _load_data()
    data[user_id] = city
    _save_data(data)

def get_user_location(user_id):
    data = _load_data()
    return data.get(user_id)

def get_all_users():
    return _load_data().items()
