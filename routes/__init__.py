from flask import jsonify, request
import jwt
from models import User
from app_core import app, db

@app.route("/")
def root():
    return jsonify({'message': 'API Root'})

@app.route("/current-user")
def api_get_current_user():
    auth_header = request.headers.get('Authorization')

    if not auth_header or 'Bearer' not in auth_header:
        return jsonify({'message': 'Bad authorization header!'}), 400

    split = auth_header.split(' ')
    
    try:
        decode_data = jwt.decode(split[1], app.config['SECRET_KEY'])
        user = User.query.filter_by(public_id=decode_data.get('user_id')).first()
        print(user)

        if not user:
            return jsonify({'message': 'Token is invalid'}), 401
        return jsonify({
            'message': 'User is authenticated',
            'user': user.as_dict()
        })
    except Exception as error:
        return jsonify({'message': 'Token is invalid'}), 401

@app.route("/login", methods=["POST"])
def api_login():
    try:
        req = request.get_json(silent=True)
        if not req or not req.get('email') or not req.get('password'):
            return jsonify({
                'message': 'No login data found'
            })
        user = User.query.filter_by(email=req.get('email')).first()

        if user and user.check_password(req.get('password')):
            token_data = {
                'user_id': user.public_id
            }

            token = jwt.encode(token_data, app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('UTF-8')})

        return jsonify({'message': 'invalid login'}), 401

    except Exception as error:
        return jsonify({'message': 'something went wrong'}), 400

@app.route("/users")
def api_get_users():

    data = User.query.all()
    users = [user.as_dict() for user in data]
    return jsonify(users)

@app.route("/users", methods=['POST'])
def api_create_users():
    req = request.get_json(silent=True)
    if not req:
        return jsonify({
            'message': 'No json data found'
        })
    try:
        user = User(**req)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message':'User with id {user.public_id} created successfully',
            'user': user.as_dict()
        })
    except Exception as error:
        return jsonify({
            'message': 'Something went wrong'
        }),400
