import secrets
import string

from werkzeug.security import generate_password_hash

from app.main.service.users_json_service import save_users
from app.main.util.constant import RoleType
from manage import app
from app.main.model.models import db, UserInfo, Contact, Role
from faker import Faker


def generate_random_string(length=10):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


def create_seed_data():
    fake = Faker()

    with app.app_context():
        # Generate fake data for models
        contacts = [
            Contact(
                phone=fake.phone_number()[:10],
                address=fake.address()[:100],
                city=fake.city(),
                country=fake.country(),
            )
            for _ in range(10)
        ]
        db.session.add_all(contacts)
        db.session.flush()

        roles = [
            Role(name=role_name.name) for role_name in RoleType
        ]
        db.session.add_all(roles)

        # Efficiently find the admin role using filter_by
        admin_role = Role.query.filter_by(name=RoleType.ADMIN.name).first()

        # Create users with random combinations
        users = [
            UserInfo(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                active=fake.boolean(),
                company=fake.company(),
                sex=fake.random_element(elements=("M", "F")),
                contact=fake.random_element(elements=contacts),  # Random contact selection
                role=fake.random_element(elements=roles),  # Random role assignment
                username=generate_random_string(15),
                password_hash=generate_password_hash("password123", method="pbkdf2"),
            )
            for _ in range(10)
        ]
        db.session.add_all(users)

        # Create admin user with separate logic and secure password
        admin_contact = Contact(
            phone=fake.phone_number()[:10],
            address=fake.address()[:100],
            city=fake.city(),
            country=fake.country(),
        )
        db.session.add(admin_contact)

        admin_user = UserInfo(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            active=True,  # Set active to True for admin
            company=fake.company(),
            sex=fake.random_element(elements=("M", "F")),
            contact=admin_contact,
            role=admin_role,
            username="admin",
            password_hash=generate_password_hash("admin@123", method="pbkdf2"),  # Use secure password
        )
        db.session.add(admin_user)

        db.session.commit()

        # Prepare data for saving
        user_json_data = {
            "contacts": [contact.to_dict() for contact in contacts],
            "roles": [role.to_dict() for role in roles],
            "users": [user.to_dict() for user in users],
        }

        save_users(user_json_data)


if __name__ == "__main__":
    create_seed_data()
