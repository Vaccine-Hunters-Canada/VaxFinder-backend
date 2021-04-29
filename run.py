from flask import Flask
from flask_restful import Api
from vaxfinder.api import vf_resources as resources

app = Flask(__name__)
api = Api(app)

api.add_resource(resources.Location, "/location")
if __name__ == '__main__':
    app.run(debug=True)