# app.py - Final version
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from backend.config import LocalDevelopmentConfig
from backend.models import db, User, Role
from backend.routes import register_routes
from backend.resources import api
from backend.create_intial_data import initialize_database

def create_app():
    app = Flask(__name__, static_folder='frontend', static_url_path='/')
    app.config.from_object(LocalDevelopmentConfig)
    
    # Initialize database
    db.init_app(app)
    
    # Flask-Security setup
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)
    
    # Initialize API and routes
    api.init_app(app)
    register_routes(app)
    
    # Create initial data
    initialize_database(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
