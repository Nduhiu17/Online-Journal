from flask import Flask, jsonify, Blueprint#importing flask
from flask_cors import CORS
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig


authorization = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
CORS(app)
app.config.from_object(DevelopmentConfig)
blueprint = Blueprint('api', __name__)
blueprint_2 = Blueprint('home', __name__)
blueprint_3 = Blueprint('auth', __name__)

api_v1 = Api(blueprint, title='My Diary', version='1',
             description='An api to create a diary entry,get all entries,get a single ''entry,modify a diary entry and delete a diary entryTo test the end points here,register and login with your ''registered username and password.Hit the authorize button and then, Provide token to the ''secured endpoints.e.g `Bearer yourtoken`<br>Click on models to view samples of data input',
             authorizations=authorization, )
api_home = Api(blueprint_2,
               title='My Diary',
               version='1',
               description='An api to create a diary entry,get all entries,get a single ''entry,modify a diary entry and delete a diary entryTo test the end points here,register and login with your ''registered username and password.Hit the authorize button and then, Provide token to the ''secured endpoints.e.g `Bearer yourtoken`<br>Click on models to view samples of data input',
               authorizations=authorization,
               doc='/docv/',
               base_url="/"
               )

app.register_blueprint(blueprint)

jwt._set_error_handler_callbacks(api_v1)


@app.errorhandler(404)
def error_404(e):
    '''This method handles error 404'''
    return jsonify({"message": "Sorry!!!The page you were looking for was not found.Kindly countercheck the url"}), 404


from . import views
