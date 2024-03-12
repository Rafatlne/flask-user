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
    users = all_data.get('users')
    contacts = all_data.get('contacts')
    roles = all_data.get('roles')
    transformed_users = []
    for user_id, user_data in users.items():
        transformed_user = {
            "id": user_id,
            "firstName": user_data["first_name"],
            "lastName": user_data["last_name"],
            "active": user_data["active"],
            "company": user_data["company"],
            "sex": user_data["sex"],
            "contact": {
                "id": user_data["contact"],
                "phone": contacts.get(str(user_data["contact"]))["phone"],
                "address": contacts.get(str(user_data["contact"]))["address"],
                "city": contacts.get(str(user_data["contact"]))["city"],
                "country": contacts.get(str(user_data["contact"]))["country"]
            },
            "role": {
                "id": user_data["role"],
                "name": roles.get(str(user_data["role"]))["name"]
            }
        }
        transformed_users.append(transformed_user)
    return transformed_users


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def get_user_by_id(user_id):
    users = load_all_data()
    return next((user for user in users if user["id"] == user_id), None)


def get_next_id(key_name):
    all_data = load_all_data()
    users = all_data.get(key_name)
    if not users:  # Check if users_data is empty
        user_id = 1
    else:
        user_id = max(map(int, users.keys())) + 1

    return user_id


def get_object(id, key_name):
    all_data = load_all_data()
    key_data = all_data.get(key_name)

    data = key_data.get(str(id))

    return data


def get_user_details(id):
    user = get_object(id, "users")
    if not user:
        return {'message': 'User not found'}, 404

    role = get_object(user["role"], "roles")
    contact = get_object(user["contact"], "contacts")

    transformed_user = {
        "id": user["id"],
        "firstName": user["first_name"],
        "lastName": user["last_name"],
        "active": user["active"],
        "company": user["company"],
        "sex": user["sex"],
        "contact": {
            "id": user["contact"],
            "phone": contact["phone"],
            "address": contact["address"],
            "city": contact["city"],
            "country": contact["country"]
        },
        "role": {
            "id": user["role"],
            "name": role["name"]
        }
    }

    return transformed_user, 200


def create_user(user_json):
    users_data = load_all_data()

    user_id = get_next_id("users")
    contact_id = get_next_id("users")

    user_json['id'] = int(user_id)
    user_json['role'] = user_json.pop('role_id')
    user_json['contact'] = contact_id

    contact = {
        "id": contact_id,
        "phone": user_json.pop("phone"),
        "address": user_json.pop("address"),
        "city": user_json.pop("city"),
        "country": user_json.pop("country")
    }

    users_data.get("users")[user_id] = user_json
    users_data.get("contacts")[contact] = contact
    save_users(users_data)

    return user_json, 201


def update_user(id, user_json):
    all_data = load_all_data()
    user = all_data.get("users").get(str(id), None)

    if user is None:
        return {'message': 'User not found'}, 404

    contact_id = user["contact"]
    contact = {
        "id": contact_id,
        "phone": user_json.pop("phone"),
        "address": user_json.pop("address"),
        "city": user_json.pop("city"),
        "country": user_json.pop("country")
    }
    user_json['id'] = id
    user_json['role'] = user_json.pop("role_id")
    user_json['contact'] = contact_id

    all_data.get("users")[str(id)] = user_json
    all_data.get("contacts")[str(contact_id)] = contact

    save_users(all_data)
    return get_user_details(id)


def delete_user(id):
    all_data = load_all_data()
    user = all_data.get("users").get(str(id), None)
    if not user:
        return {'message': 'User not found'}, 404
    del all_data.get("users")[str(id)]
    del all_data.get("contacts")[str(user['contact'])]
    save_users(all_data)

    return '', 204
