from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

# -----------------------------------------
# Role Table for Flask-Security
# -----------------------------------------
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# -----------------------------------------
# User Model with Security integration
# -----------------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)
    
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    scores = db.relationship('Score', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

# -----------------------------------------
# Subject Model
# -----------------------------------------
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    chapters = db.relationship('Chapter', backref='subject', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Subject {self.name}>"

# -----------------------------------------
# Chapter Model
# -----------------------------------------
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    quizzes = db.relationship('Quiz', backref='chapter', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Chapter {self.name}>"

# -----------------------------------------
# Quiz Model
# -----------------------------------------
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.String(200))

    questions = db.relationship('Question', backref='quiz', cascade="all, delete-orphan", lazy=True)
    scores = db.relationship('Score', backref='quiz', lazy=True)

    def __repr__(self):
        return f"<Quiz {self.id} - Chapter {self.chapter_id}>"

# -----------------------------------------
# Question Model
# -----------------------------------------
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_title = db.Column(db.String(300), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)  # Should be 1 to 4

    def __repr__(self):
        return f"<Question {self.id}>"

# -----------------------------------------
# Score Model
# -----------------------------------------
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    total_score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Score {self.user_id} - Quiz {self.quiz_id}>"

# -----------------------------------------
# User Activity (for reminders / reports)
# -----------------------------------------
class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_login = db.Column(db.DateTime)
    last_quiz_attempt = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Activity {self.user_id}>"
