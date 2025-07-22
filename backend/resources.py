from flask import jsonify, request
from flask_restful import Api, Resource, fields, marshal_with
from flask_security import auth_required, current_user
from backend.models import Quiz, db

api = Api(prefix='/api')

quiz_fields = {
    'id': fields.Integer,
    'chapter_id': fields.Integer,
    'date_of_quiz': fields.DateTime,
    'duration_minutes': fields.Integer,
    'remarks': fields.String
}

class QuizAPI(Resource):

    @marshal_with(quiz_fields)
    @auth_required('token')
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)

        if not quiz:
            return {"message": "not found"}, 404
        return quiz

    @auth_required('token')
    def delete(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)

        if not quiz:
            return {"message": "not found"}, 404

        # Admin check
        if 'admin' in [role.name for role in current_user.roles]:
            db.session.delete(quiz)
            db.session.commit()
            return {"message": "quiz deleted"}
        else:
            return {"message": "not authorized"}, 403

class QuizListAPI(Resource):

    @marshal_with(quiz_fields)
    @auth_required('token')
    def get(self):
        quizzes = Quiz.query.all()
        return quizzes

    @auth_required('token')
    def post(self):
        data = request.get_json()
        chapter_id = data.get('chapter_id')
        date_of_quiz = data.get('date_of_quiz')  # must be ISO string
        duration_minutes = data.get('duration_minutes')
        remarks = data.get('remarks')

        # Admin only can create quiz
        if 'admin' in [role.name for role in current_user.roles]:
            quiz = Quiz(
                chapter_id=chapter_id,
                date_of_quiz=date_of_quiz,
                duration_minutes=duration_minutes,
                remarks=remarks
            )
            db.session.add(quiz)
            db.session.commit()
            return jsonify({'message': 'quiz created'})
        else:
            return {"message": "not authorized"}, 403

# Register Resources
api.add_resource(QuizAPI, '/quizzes/<int:quiz_id>')
api.add_resource(QuizListAPI, '/quizzes')
