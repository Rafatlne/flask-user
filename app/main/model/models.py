import secrets
from datetime import datetime, timedelta
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# Define SQLAlchemy models
class UserInfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    active = db.Column(db.Boolean)
    company = db.Column(db.String(100))
    sex = db.Column(db.String(1))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = relationship("Contact", back_populates="user_infos_contact")
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = relationship("Role", back_populates="user_infos_role")
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    # ...
    def get_token(self, expires_in=120):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_urlsafe(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def check_token(token):
        user = UserInfo.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15))
    address = db.Column(db.String(100))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    user_infos_contact = relationship("UserInfo", back_populates="contact")


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_infos_role = relationship("UserInfo", back_populates="role")
