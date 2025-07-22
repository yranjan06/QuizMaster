from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

class User(db.Model):
    """User model for both admin and regular users"""
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
    
    # Relationships
    quiz_attempts = db.relationship('Score', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == UserRole.ADMIN
    
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
    
    # Relationships
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
    order_index = db.Column(db.Integer, default=0)  # For ordering chapters
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
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
    time_duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    total_marks = db.Column(db.Integer, default=0)
    passing_marks = db.Column(db.Integer, default=0)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')
    scores = db.relationship('Score', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')
    creator = db.relationship('User', backref='created_quizzes')
    
    @property
    def question_count(self):
        """Get total number of questions in quiz"""
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
    correct_option = db.Column(db.Integer, nullable=False)  # 1, 2, 3, or 4
    marks = db.Column(db.Integer, default=1)
    explanation = db.Column(db.Text)  # Optional explanation for answer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_index = db.Column(db.Integer, default=0)  # For ordering questions
    is_active = db.Column(db.Boolean, default=True)
    
    def get_options(self):
        """Return list of options"""
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
    time_taken = db.Column(db.Integer)  # Time taken in minutes
    percentage = db.Column(db.Float)
    timestamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    is_passed = db.Column(db.Boolean, default=False)
    remarks = db.Column(db.Text)
    
    # Store user answers as JSON or separate table
    user_answers = db.Column(db.Text)  # JSON string of {question_id: selected_option}
    
    def calculate_percentage(self):
        """Calculate and set percentage score"""
        if self.total_questions > 0:
            self.percentage = (self.correct_answers / self.total_questions) * 100
        return self.percentage
    
    def __repr__(self):
        return f'<Score {self.user_id}-{self.quiz_id}>'

class UserActivity(db.Model):
    """Track user activity for notifications and reports"""
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'login', 'quiz_attempt', 'quiz_completion'
    activity_data = db.Column(db.Text)  # JSON data for additional info
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='activities')
    
    def __repr__(self):
        return f'<UserActivity {self.user_id}-{self.activity_type}>'

class ExportJob(db.Model):
    """Track CSV export jobs"""
    __tablename__ = 'export_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)  # 'user_quiz_export', 'admin_user_export'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'processing', 'completed', 'failed'
    file_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    
    # Relationship
    user = db.relationship('User', backref='export_jobs')
    
    def __repr__(self):
        return f'<ExportJob {self.id}-{self.job_type}>'

# Initialize database function
def init_db(app):
    """Initialize database and create admin user"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Create admin user if doesn't exist
        admin = User.query.filter_by(role=UserRole.ADMIN).first()
        if not admin:
            admin = User(
                username='admin@quizmaster.com',
                full_name='Quiz Master Admin',
                role=UserRole.ADMIN,
                is_active=True
            )
            admin.set_password('admin123')  # Change this in production
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")

# Utility functions for common queries
def get_user_quiz_history(user_id):
    """Get user's quiz attempt history with details"""
    return db.session.query(Score, Quiz, Chapter, Subject)\
        .join(Quiz)\
        .join(Chapter)\
        .join(Subject)\
        .filter(Score.user_id == user_id)\
        .order_by(Score.timestamp_of_attempt.desc())\
        .all()

def get_quiz_statistics(quiz_id):
    """Get quiz statistics (attempts, average score, etc.)"""
    scores = Score.query.filter_by(quiz_id=quiz_id).all()
    if not scores:
        return None
    
    return {
        'total_attempts': len(scores),
        'average_score': sum(s.percentage for s in scores) / len(scores),
        'highest_score': max(s.percentage for s in scores),
        'lowest_score': min(s.percentage for s in scores),
        'pass_rate': len([s for s in scores if s.is_passed]) / len(scores) * 100
    }
