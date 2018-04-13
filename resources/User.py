from flask import request
from flask_restful import Resource
from Model import db, User, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users).data
        return {'status': 'success', 'data': users}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return {'message': 'User already exists'}, 400
        user = User(
            username=json_data['username'],
            user_id=json_data['user_id'],
            email=json_data['email'],
            group=json_data['group'],
            password_hash=json_data['password_hash']
        )

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data

        return {"status": 'success', 'data': result}, 201