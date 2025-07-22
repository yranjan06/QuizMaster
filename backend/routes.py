from flask import request, jsonify, render_template_string
from flask_security import verify_password, current_user, auth_token_required, login_user, logout_user
from backend.models import db, User, Subject, Chapter, Quiz, Question, Score, UserRole
import json
from datetime import datetime

def register_routes(app):
    
    @app.route('/')
    def home():
        """Serve the main SPA"""
        return app.send_static_file('index.html')
    
    @app.route('/<path:path>')
    def catch_all(path):
        """Catch all routes and serve the main SPA"""
        return app.send_static_file('index.html')

    @app.route('/api/login', methods=['POST'])
    def api_login():
        """User login API"""
        data = request.get_json()
        username = data.get('username')  # email
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        if user.check_password(password):
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Generate auth token (simple approach)
            token = f"user-{user.id}-{datetime.utcnow().timestamp()}"

            user_info = {
                'token': token,
                'username': user.username,
                'role': user.role.value,
                'id': user.id,
                'full_name': user.full_name,
                'is_admin': user.is_admin()
            }
            
            return jsonify(user_info), 200

        return jsonify({'message': 'Invalid password'}), 401

    @app.route('/api/register', methods=['POST'])
    def api_register():
        """Register a new user API"""
        data = request.get_json()
        
        username = data.get('username')  # email
        password = data.get('password')
        full_name = data.get('full_name')
        qualification = data.get('qualification')
        date_of_birth = data.get('date_of_birth')

        if not username or not password or not full_name:
            return jsonify({'message': 'Username, password, and full name are required'}), 400

        # Check if user already exists
        user = User.query.filter_by(username=username).first()
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
                email=username,  # Flask-Security requirement
                full_name=full_name,
                qualification=qualification,
                date_of_birth=dob,
                role=UserRole.USER,
                active=True
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

    @app.route('/api/subjects', methods=['GET'])
    def get_subjects():
        """Get all active subjects"""
        subjects = Subject.query.filter_by(is_active=True).all()
        result = []
        for subject in subjects:
            result.append({
                'id': subject.id,
                'name': subject.name,
                'description': subject.description,
                'chapter_count': subject.chapters.count()
            })
        return jsonify(result)

    @app.route('/api/subjects/<int:subject_id>/chapters', methods=['GET'])
    def get_chapters(subject_id):
        """Get chapters for a subject"""
        chapters = Chapter.query.filter_by(subject_id=subject_id, is_active=True)\
                                .order_by(Chapter.order_index).all()
        result = []
        for chapter in chapters:
            result.append({
                'id': chapter.id,
                'name': chapter.name,
                'description': chapter.description,
                'quiz_count': chapter.quizzes.count()
            })
        return jsonify(result)
