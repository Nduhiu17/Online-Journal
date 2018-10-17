from app.models import User
from flask import request
from flask_restplus import Resource


class UserResource(Resource):

    def post(self):
        user = User.save(username=request.json['username'], email=request.json['email'],
                         password=request.json['password'])
        return {"status": "Success", "data": user}, 201
