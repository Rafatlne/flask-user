from flask_restx import Namespace


class AuthDto:
    """Data Transfer object for Auth"""
    api = Namespace("auth", description="Auth related operations")