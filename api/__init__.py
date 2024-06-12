from flask_restx import Api

# from .countries_api import api as countries_api

api = Api(
    title="HBnB API",
    version="1.0",
    description="HBnB Evolution API: Part 1.",
)

# api.add_namespace(countries_api)