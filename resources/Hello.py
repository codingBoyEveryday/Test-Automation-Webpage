from flask_restful import Resource


class Hello(Resource):
    def get(self):
        return {"message": "Hello, World get!"}

    # def post(self):
    #     return {"message": "Hello, World post!"}