import re
from flask import request, abort
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_restplus import Resource, reqparse,fields
from datetime import datetime
from app import api_v1
from app.validators import Validate
from .models import Entry
from .models import User


api_v1.namespaces.clear()

ns1 = api_v1.namespace('api/v1/auth',
                       description='End points regarding user operations')

ns = api_v1.namespace('api/v1',
                      description='End points regarding entries operations')


resource_fields = api_v1.model('Entry', {
    'title': fields.String,
    'description': fields.String,
})


@ns.route('/entries')
class EntryResource(Resource):
    '''Get all entries resource'''

    @jwt_required
    @ns.doc(security='apiKey')
    def get(self):
        '''Method to get all entries(GET request)'''
        results = Entry.get_all_entries()
        return results

    @ns.expect(resource_fields)
    @ns.doc(security='apiKey')
    @jwt_required
    def post(self):
        '''Method to add an entry(POST request)'''
        parser = reqparse.RequestParser()
        parser.add_argument('title', help='This field cannot be blank', required=True)
        parser.add_argument('description', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        search_keys = ("title", "description")
        if all(key in data.keys() for key in search_keys):
            description = data.get("description").strip()
            does_entry_exist = Validate.is_entry_exist(description)
            if does_entry_exist:
                return {"message": "This entry is already posted"},409
            if re.match(r"^[1-9]\d*(\.\d+)?$", data['title']):
                return {'message': 'the title should be of type string'}, 400
            if len(data['title']) < 10:
                return {'message': 'The length of the title should be atleast 10 characters'}, 400
            if len(data['description']) < 20:
                return {'message': 'The length of your question content should be atleast 15 characters'},400
            entry = Entry.save(user_id=get_jwt_identity(), date_created=str(datetime.now()),
                               date_modified=str(datetime.now()), title=data['title'],
                               description=data['description'])

            return {"status": "Success", "data": entry}, 201

new_entry = api_v1.model('Entry', {
    'title': fields.String,
    'description': fields.String,
})

@ns.route('/entries/<string:id>')
class OneEntryResource(Resource):
    '''Get a single entry resource'''
    @jwt_required
    @ns.doc(security='apiKey')
    def get(self, id):
        '''Method to get an entry by id(GET request)'''
        result = Entry.get_entry(id)
        if result:
            return ({'message':'success','data':result}),200
        return ({'message':'No question found with that id'}),404




    @ns.doc(security='apiKey')
    @jwt_required
    def delete(self, id):
        '''Method to delete an entry by entry author'''
        entry_to_delete = Entry.get_entry(id)
        logged_in_user = get_jwt_identity()
        
        print('logged in user is',logged_in_user)
        
        if entry_to_delete:
            question_owner = entry_to_delete['user']['id']
            print('question owner', question_owner)
            if logged_in_user == question_owner:
                Entry.delete(id)
                return ({'message': 'successfully deleted'}), 200
            return ({'message': 'you are not authorised to delete the question since you are not the owner'}), 401
        return {"message": "No entry found with that id"}, 404



    @api_v1.expect(new_entry)
    @jwt_required
    @ns.doc(security='apiKey')
    def put(self, id):
        '''Method to modify an entry by entry author'''
        entry_to_update = Entry.get_entry(id)
        if entry_to_update:
            entry_owner = entry_to_update['user']['email']
            logged_in_user = get_jwt_identity()
            if entry_owner == logged_in_user:
                entry = Entry.update(
                    title=request.json['title'],
                    description=request.json['description'],
                    id=id)
                return {"message": "Updated", "data": entry}, 201
            return ({'message': 'you are not authorised to updater the question since you are not the owner'}), 401
        return {"message": "No entry found with that id"}, 404






new_user = api_v1.model('Register', {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
})

@ns1.route('/signup')
class UserRegistrationResource(Resource):
    '''User sign up resource'''
    @api_v1.expect(new_user)
    def post(self):
        '''Method that registers a user'''
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        parser.add_argument('email', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        if not Validate.validate_length_username(data['username']):
            return {'message': 'The length of username should be atleast 4 characters'}, 400
        if not Validate.validate_password_length(data['password']):
            return {'message': 'the length of the password should be atleast 6 characters'}, 400
        if re.match(r"^[1-9]\d*(\.\d+)?$", data['password']):
            return {'message': 'the username and password should be of type string'}, 400
        if not Validate.validate_email_format(data['email']):
            return {'message': 'Invalid email.The email should be of type "example@mail.com"'}, 400
        if User.find_by_username(data['username']):
            return {'message': 'This username is already taken,kindly try another username'}, 409
        if User.find_by_email(data['email']):
            return {'message': 'This email is already taken'}, 409
        if Validate.validate_username_format(data['username']):
            return ({'message':'Invalid username.The username should be of type "Username"'}), 400
        user = User.save(username=data['username'], email=data['email'],
                         password=User.generate_hash(data['password']),date_created=datetime.now(),date_modified=datetime.now())

        return ({'message':'you have successfully registered','data':user}),201

n_user = api_v1.model('Login', {
    'email': fields.String,
    'password': fields.String
})



@ns1.route('/login')
class UserLoginResource(Resource):
    '''User login resource'''
    @api_v1.expect(n_user)
    def post(self):
        '''Method that logs in a user'''
        parser = reqparse.RequestParser()
        parser.add_argument('password', help='This3 field cannot be blank', required=True)
        parser.add_argument('email', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        data = parser.parse_args()
        current_user = User.find_by_email(data['email'])
        if current_user == False:
            return {'message': 'User doesnt exist'}, 404

        if User.verify_hash(data['password'], current_user[3]):
            access_token = create_access_token(current_user[0])
            return dict(message='Logged in',
                        access_token=access_token), 200
        return {'message': 'Wrong credentials'}, 403
