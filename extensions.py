# extensions.py
"""
Centralized Flask extensions to avoid circular imports.
Import these extensions in your app.py and models/controllers.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
mail = Mail()

# Export all extensions
__all__ = ['db', 'migrate', 'jwt', 'cors', 'mail']