import random
import string
from datetime import datetime, timedelta
import secrets

from werkzeug.security import generate_password_hash

from app.main.model.models import UserInfo, Contact, Role
from app.main.model.models import db
from manage import app


# Function to generate random string
def generate_random_string(length=10):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


# Function to create a user with associated contact and role
def create_user():
    user = UserInfo(
        first_name=generate_random_string(),
        last_name=generate_random_string(),
        active=bool(random.getrandbits(1)),  # Randomly set active
        company=generate_random_string(20),
        sex=random.choice(['M', 'F']),
        username=generate_random_string(15),
        email=generate_random_string(20) + "@" + generate_random_string(5) + ".com",
        about_me=generate_random_string(100),
        password_hash=generate_password_hash("password123", method="pbkdf2"),  # Set default password
        last_seen=datetime.utcnow(),
        timestamp=datetime.utcnow(),
        token=generate_random_string(32),
        token_expiration=datetime.utcnow() + timedelta(seconds=120),
    )

    contact = Contact(
        phone=generate_random_string(12),
        address=generate_random_string(30),
        city=generate_random_string(15),
        country=generate_random_string(10),
    )

    user.contacts.append(contact)

    role_choices = ["admin", "user", "manager"]
    user.roles.append(Role(name=random.choice(role_choices)))

    return user


def create_seed_data():
    with app.app_context():
        for _ in range(20):
            user = create_user()
            db.session.add(user)

        db.session.commit()
        print("Database seeded with 20 users!")


if __name__ == '__main__':
    create_seed_data()
