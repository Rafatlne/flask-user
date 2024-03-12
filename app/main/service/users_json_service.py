import json

USERS_FILE = "users.json"


def load_all_data():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_all_users():
    all_data = load_all_data()
    users = all_data.get("users")
    transformed_users = []
    for user_id, user_data in users.items():
        transformed_users.append(user_data)
    return transformed_users


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def get_user_by_id(user_id):
    users = load_all_data()
    return next((user for user in users if user["id"] == user_id), None)


def get_next_id(key_name):
    all_data = load_all_data()
    all_key = all_data.get(key_name)
    if not all_key:  # Check if users_data is empty
        id = 1
    else:
        id = max(map(int, all_key.keys())) + 1

    return id


def get_object(id, key_name):
    all_data = load_all_data()
    key_data = all_data.get(key_name)

    data = key_data.get(str(id))

    return data


def get_user_details(id):
    user = get_object(id, "users")
    if not user:
        return {"message": "User not found"}, 404

    return user, 200


def create_user(user_json):
    users_data = load_all_data()
    role = users_data.get("roles").get(str(user_json.pop("role_id")), None)
    user_id = get_next_id("users")
    contact_id = get_next_id("contacts")

    user_json["id"] = int(user_id)
    user_json["role"] = role

    contact = {
        "id": contact_id,
        "phone": user_json.pop("phone"),
        "address": user_json.pop("address"),
        "city": user_json.pop("city"),
        "country": user_json.pop("country"),
    }

    user_json["contact"] = contact

    users_data.get("users")[user_id] = user_json
    users_data.get("contacts")[contact_id] = contact
    save_users(users_data)

    return user_json, 201


def update_user(id, user_json):
    all_data = load_all_data()
    user = all_data.get("users").get(str(id), None)
    role = all_data.get("roles").get(str(user_json.pop("role_id")), None)

    if user is None:
        return {"message": "User not found"}, 404

    contact_id = user["contact"]["id"]
    contact = {
        "id": contact_id,
        "phone": user_json.pop("phone"),
        "address": user_json.pop("address"),
        "city": user_json.pop("city"),
        "country": user_json.pop("country"),
    }
    user_json["id"] = id
    user_json["role"] = role
    user_json["contact"] = contact

    all_data.get("users")[str(id)] = user_json
    all_data.get("contacts")[str(contact_id)] = contact

    save_users(all_data)
    return get_user_details(id)


def delete_user(id):
    all_data = load_all_data()
    user = all_data.get("users").get(str(id), None)
    if not user:
        return {"message": "User not found"}, 404
    del all_data.get("users")[str(id)]
    del all_data.get("contacts")[str(user["contact"]["id"])]
    save_users(all_data)

    return "", 204
