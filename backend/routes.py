from flask import current_app as app, jsonify, render_template, request
from flask_security import auth_required, verify_password, hash_password
from backend.models import db

datastore = app.security.datastore

@app.route('/')
def home():
    return render_template('index.html')  # Vue will take over from here

# -----------------------------------------
# Protected Test Route
# -----------------------------------------
@app.get('/protected')
@auth_required('token')
def protected():
    return '<h1>Accessible only by authenticated users</h1>'

# -----------------------------------------
# Login Route (Token Based)
# -----------------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "invalid inputs"}), 400

    user = datastore.find_user(email=email)
    if not user:
        return jsonify({"message": "invalid email"}), 404

    if verify_password(password, user.password):
        return jsonify({
            'token': user.get_auth_token(),
            'email': user.email,
            'role': user.roles[0].name,
            'id': user.id
        })

    return jsonify({'message': 'password wrong'}), 400

# -----------------------------------------
# Register Route (User Only)
# -----------------------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # default to 'user'

    if not email or not password or role not in ['admin', 'user']:
        return jsonify({"message": "invalid inputs"}), 400

    user = datastore.find_user(email=email)
    if user:
        return jsonify({"message": "user already exists"}), 409

    try:
        datastore.create_user(
            email=email,
            password=hash_password(password),
            roles=[role],
            active=True
        )
        db.session.commit()
        return jsonify({"message": "user created"}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "error creating user"}), 500
