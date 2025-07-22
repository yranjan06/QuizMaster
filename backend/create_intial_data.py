from backend.models import db, User, UserRole, Subject, Chapter, Quiz, Question, Score, Role
from datetime import datetime

def initialize_database(app):
    with app.app_context():
        db.create_all()

        # Create roles first (Flask-Security requirement)
        if not Role.query.filter_by(name='admin').first():
            admin_role = Role(name='admin', description='Administrator')
            user_role = Role(name='user', description='Regular User')
            db.session.add(admin_role)
            db.session.add(user_role)
            db.session.commit()

        # Create Admin user if not exists
        if not User.query.filter_by(username='admin@quizmaster.com').first():
            admin = User(
                username='admin@quizmaster.com',
                email='admin@quizmaster.com',
                full_name='Admin User',
                role=UserRole.ADMIN,
                date_of_birth=datetime.strptime('1985-01-01', '%Y-%m-%d').date(),
                active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)

        # Create Regular User if not exists
        if not User.query.filter_by(username='student@quizmaster.com').first():
            student = User(
                username='student@quizmaster.com',
                email='student@quizmaster.com',
                full_name='Test Student',
                role=UserRole.USER,
                qualification='10th Grade',
                date_of_birth=datetime.strptime('2005-08-15', '%Y-%m-%d').date(),
                active=True
            )
            student.set_password('student123')
            db.session.add(student)

        db.session.commit()

        # Add Sample Subject if not exists
        if not Subject.query.count():
            subject = Subject(
                name='Mathematics',
                description='Basic Mathematics Topics',
                created_by=1,
                is_active=True
            )
            db.session.add(subject)
            db.session.commit()

            # Add Chapter
            chapter = Chapter(
                name='Algebra',
                description='Basic Algebra Concepts',
                subject_id=subject.id,
                order_index=1,
                is_active=True
            )
            db.session.add(chapter)
            db.session.commit()

            # Add Quiz
            quiz = Quiz(
                title='Algebra Basics Quiz',
                description='Covers fundamentals of algebra',
                chapter_id=chapter.id,
                date_of_quiz=datetime.strptime('2024-11-01', '%Y-%m-%d').date(),
                time_duration=10,
                total_marks=5,
                passing_marks=3,
                created_by=1,
                is_active=True
            )
            db.session.add(quiz)
            db.session.commit()

            # Add Questions
            questions = [
                Question(
                    quiz_id=quiz.id,
                    question_statement='What is the value of x in: 2x + 3 = 7?',
                    option1='2',
                    option2='1',
                    option3='3',
                    option4='5',
                    correct_option=1,
                    marks=1,
                    order_index=1,
                    is_active=True
                ),
                Question(
                    quiz_id=quiz.id,
                    question_statement='What is (a + b)^2?',
                    option1='a^2 + b^2',
                    option2='a^2 + 2ab + b^2',
                    option3='2a + 2b',
                    option4='a + b',
                    correct_option=2,
                    marks=1,
                    order_index=2,
                    is_active=True
                )
            ]
            db.session.bulk_save_objects(questions)
            db.session.commit()
