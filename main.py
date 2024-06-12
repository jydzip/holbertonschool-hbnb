from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from api.countries import api as countries_API
from api.cities import api as cities_API
from api.places import api as places_API

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


api = Api(
    title="HBnB API",
    version="1.0",
    description="HBnB Evolution API: Part 1.",
)
api.add_namespace(countries_API)
api.add_namespace(cities_API)
api.add_namespace(places_API)

api.init_app(app)

app.run(debug=True)