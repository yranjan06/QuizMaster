from flask import current_app as app
from backend.models import db
from flask_security import SQLAlchemyUserDatastore, hash_password

with app.app_context():
    db.create_all()

    userdatastore: SQLAlchemyUserDatastore = app.security.datastore

    # Create roles
    userdatastore.find_or_create_role(name='admin', description='quiz master')
    userdatastore.find_or_create_role(name='user', description='regular quiz taker')

    # Seed admin user (pre-created, no registration allowed)
    if not userdatastore.find_user(email='admin@quizmaster.app'):
        userdatastore.create_user(
            email='admin@quizmaster.app',
            password=hash_password('pass'),
            roles=['admin']
        )

    # Seed one normal user for testing
    if not userdatastore.find_user(email='user01@quizmaster.app'):
        userdatastore.create_user(
            email='user01@quizmaster.app',
            password=hash_password('pass'),
            roles=['user']
        )

    db.session.commit()
