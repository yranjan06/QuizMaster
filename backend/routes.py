from flask import request, jsonify, render_template, current_app, send_file
from flask_security import auth_required, verify_password, hash_password, current_user
from backend.models import db, User, Subject, Chapter, Quiz, Question, Score, UserActivity, ExportJob
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash
import os
import json
from datetime import datetime, timedelta
from celery import current_app as celery_app
import csv
import io

def register_routes(app):
    #############################################
    # Basic Routes & Authentication
    #############################################
    
    @app.get('/')
    def home():
        """Home page route"""
        return render_template('index.html')

    @app.get('/admin')
    def admin_dashboard():
        """Admin dashboard route"""
        return render_template('admin.html')

    @app.get('/user')
    def user_dashboard():
        """User dashboard route"""
        return render_template('user.html')

    @app.route('/login', methods=['POST'])
    def login():
        """User login with role-specific information in the response"""
        datastore = app.security.datastore
        data = request.get_json()
        username = data.get('username')  # email
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        user = datastore.find_user(username=username)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        if verify_password(password, user.password):
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()

            # Log activity
            activity = UserActivity(
                user_id=user.id,
                activity_type='login',
                activity_data=json.dumps({'login_time': datetime.utcnow().isoformat()})
            )
            db.session.add(activity)
            db.session.commit()

            user_info = {
                'token': user.get_auth_token(),
                'username': user.username,
                'role': user.role.value,
                'id': user.id,
                'full_name': user.full_name,
                'is_admin': user.is_admin()
            }
            
            return jsonify(user_info), 200

        return jsonify({'message': 'Invalid password'}), 401

    #############################################
    # User Registration Routes
    #############################################
    
    @app.route('/register', methods=['POST'])
    def register_user():
        """Register a new user"""
        datastore = app.security.datastore
        data = request.get_json()
        
        # Extract user data
        username = data.get('username')  # email
        password = data.get('password')
        full_name = data.get('full_name')
        qualification = data.get('qualification')
        date_of_birth = data.get('date_of_birth')

        # Validate required fields
        if not username or not password or not full_name:
            return jsonify({'message': 'Username, password, and full name are required'}), 400

        # Check if user already exists
        user = datastore.find_user(username=username)
        if user:
            return jsonify({'message': 'User already exists'}), 409

        try:
            # Parse date of birth if provided
            dob = None
            if date_of_birth:
                dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

            # Create new user
            user = User(
                username=username,
                full_name=full_name,
                qualification=qualification,
                date_of_birth=dob,
                role=UserRole.USER,
                is_active=True
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            return jsonify({
                'message': 'User registered successfully',
                'user_id': user.id
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error creating user: {str(e)}'}), 500