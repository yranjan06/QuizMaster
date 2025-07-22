from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum
import secrets

db = SQLAlchemy()

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

class User(db.Model):
    """Simplified User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)  # email
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.USER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    auth_token = db.Column(db.String(100), unique=True)
    
    # Relationships
    quiz_attempts = db.relationship('Score', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_auth_token()
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == UserRole.ADMIN
    
    def generate_auth_token(self):
        """Generate a new auth token"""
        self.auth_token = secrets.token_urlsafe(32)
        return self.auth_token
    
    def __repr__(self):
        return f'<User {self.username}>'

class Subject(db.Model):
    """Subject model for organizing quizzes by field of study"""
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    chapters = db.relationship('Chapter', backref='subject', lazy='dynamic', cascade='all, delete-orphan')
    creator = db.relationship('User', backref='created_subjects')
    
    def __repr__(self):
        return f'<Subject {self.name}>'

class Chapter(db.Model):
    """Chapter model for subdividing subjects"""
    __tablename__ = 'chapters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    quizzes = db.relationship('Quiz', backref='chapter', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Chapter {self.name}>'

class Quiz(db.Model):
    """Quiz model for tests within chapters"""
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.Integer, nullable=False)
    total_marks = db.Column(db.Integer, default=0)
    passing_marks = db.Column(db.Integer, default=0)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    questions = db.relationship('Question', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')
    scores = db.relationship('Score', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')
    creator = db.relationship('User', backref='created_quizzes')
    
    @property
    def question_count(self):
        return self.questions.filter_by(is_active=True).count()
    
    def __repr__(self):
        return f'<Quiz {self.title}>'

class Question(db.Model):
    """Question model for MCQ questions in quizzes"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200))
    option4 = db.Column(db.String(200))
    correct_option = db.Column(db.Integer, nullable=False)
    marks = db.Column(db.Integer, default=1)
    explanation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    def get_options(self):
        options = [self.option1, self.option2]
        if self.option3:
            options.append(self.option3)
        if self.option4:
            options.append(self.option4)
        return options
    
    def __repr__(self):
        return f'<Question {self.id}>'

class Score(db.Model):
    """Score model for storing quiz attempt results"""
    __tablename__ = 'scores'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_scored = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer)
    percentage = db.Column(db.Float)
    timestamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    is_passed = db.Column(db.Boolean, default=False)
    remarks = db.Column(db.Text)
    user_answers = db.Column(db.Text)
    
    def calculate_percentage(self):
        if self.total_questions > 0:
            self.percentage = (self.correct_answers / self.total_questions) * 100
        return self.percentage
    
    def __repr__(self):
        return f'<Score {self.user_id}-{self.quiz_id}>'
