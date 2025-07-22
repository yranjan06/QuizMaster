from flask import request
from flask_restful import Api, Resource, fields, marshal_with
from flask_security import auth_required, current_user
from backend.models import db, User, Subject, Chapter, Quiz, Question, Score

api = Api(prefix='/api')

# Marshaling fields
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'full_name': fields.String,
    'role': fields.String,
    'qualification': fields.String,
}

subject_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
}

chapter_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'subject_id': fields.Integer,
}

quiz_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'chapter_id': fields.Integer,
    'time_duration': fields.Integer,
    'total_marks': fields.Integer,
    'passing_marks': fields.Integer,
}

question_fields = {
    'id': fields.Integer,
    'quiz_id': fields.Integer,
    'question_statement': fields.String,
    'option1': fields.String,
    'option2': fields.String,
    'option3': fields.String,
    'option4': fields.String,
    'correct_option': fields.Integer,
}

score_fields = {
    'id': fields.Integer,
    'quiz_id': fields.Integer,
    'user_id': fields.Integer,
    'total_scored': fields.Integer,
    'percentage': fields.Float,
    'correct_answers': fields.Integer,
    'time_taken': fields.Integer,
    'is_passed': fields.Boolean,
    'timestamp_of_attempt': fields.DateTime,
}


# User API
class UserAPI(Resource):
    @marshal_with(user_fields)
    @auth_required('token')
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user


# Subject API
class SubjectAPI(Resource):
    @marshal_with(subject_fields)
    def get(self, subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404
        return subject


# Chapter API
class ChapterAPI(Resource):
    @marshal_with(chapter_fields)
    def get(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404
        return chapter


# Quiz API
class QuizAPI(Resource):
    @marshal_with(quiz_fields)
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404
        return quiz


# Question API
class QuestionAPI(Resource):
    @marshal_with(question_fields)
    def get(self, question_id):
        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404
        return question


# Score API (quiz attempt history)
class ScoreAPI(Resource):
    @marshal_with(score_fields)
    @auth_required('token')
    def get(self, score_id):
        score = Score.query.get(score_id)
        if not score:
            return {"message": "Score not found"}, 404
        return score

    @auth_required('token')
    def post(self):
        data = request.get_json()
        score = Score(
            quiz_id=data.get('quiz_id'),
            user_id=current_user.id,
            total_scored=data.get('total_scored'),
            total_questions=data.get('total_questions'),
            correct_answers=data.get('correct_answers'),
            time_taken=data.get('time_taken'),
            is_passed=data.get('is_passed'),
            percentage=data.get('percentage'),
            user_answers=data.get('user_answers')
        )
        db.session.add(score)
        db.session.commit()
        return {"message": "Score recorded"}, 201


# Register API endpoints
api.add_resource(UserAPI, '/users/<int:user_id>')
api.add_resource(SubjectAPI, '/subjects/<int:subject_id>')
api.add_resource(ChapterAPI, '/chapters/<int:chapter_id>')
api.add_resource(QuizAPI, '/quizzes/<int:quiz_id>')
api.add_resource(QuestionAPI, '/questions/<int:question_id>')
api.add_resource(ScoreAPI, '/scores', '/scores/<int:score_id>')
