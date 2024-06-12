from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from api.countries import api as countriesApi
from api.cities import api as citiesAPI

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


api = Api(
    title="HBnB API",
    version="1.0",
    description="HBnB Evolution API: Part 1.",
)
api.add_namespace(countriesApi)

api.add_namespace(citiesAPI)

api.init_app(app)

app.run(debug=True)