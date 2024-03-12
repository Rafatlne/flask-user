# seed.py
from app.main.service.users_json_service import save_users
from manage import app
from app.main.model.models import db
from app.main.model.models import UserInfo, Contact, Role
from faker import Faker


def create_seed_data():
    fake = Faker()

    with app.app_context():
        # Generate fake data for UserInfo model
        contact_ids = []
        role_ids = []
        contacts = {}
        roles = {}
        users_json_data = {}
        for _ in range(10):
            contact = Contact(
                phone=fake.phone_number()[:10],  # Extract first 10 characters of the phone number
                address=fake.address()[:100],  # Extract first 100 characters of the address
                city=fake.city(),
                country=fake.country()
            )
            db.session.add(contact)
            db.session.flush()
            contact_ids.append(contact.id)
            contacts[str(contact.id)] = {
                "id": contact.id,
                "phone": contact.phone,
                "address": contact.address,
                "city": contact.city,
                "country": contact.country,
            }

        db.session.commit()

        # Generate fake data for Role model
        for _ in range(10):
            role = Role(
                name=fake.job()
            )
            db.session.add(role)
            db.session.flush()
            role_ids.append(role.id)
            roles[str(role.id)] = {
                "id": role.id,
                "name": role.name,
            }

        db.session.commit()

        # Generate fake data for UserInfo model
        for _ in range(10):
            # Select a random contact_id from the list of existing contact_ids
            contact_id = fake.random_element(elements=contact_ids)
            role_id = fake.random_element(elements=role_ids)

            user = UserInfo(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                active=fake.boolean(),
                company=fake.company(),
                sex=fake.random_element(elements=('M', 'F')),
                contact_id=contact_id,
                role_id=role_id
            )
            db.session.add(user)
            db.session.flush()
            users_json_data[str(user.id)] = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "active": user.active,
                "company": user.company,
                "sex": user.sex,
                "contact": contact_id,
                "role": role_id,
            }

        db.session.commit()
        user_json_data = {"contacts": contacts, "roles": roles, "users": users_json_data}
        save_users(user_json_data)


if __name__ == '__main__':
    create_seed_data()