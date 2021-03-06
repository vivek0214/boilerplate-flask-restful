"""Base resource classes"""

import logging

from flask import request
from flask_restful import Resource, abort, marshal

from app.generics.constants import API_ERRORS
from app.generics.controllers import BaseController
from app.generics.models import Context

LOGGER = logging.getLogger(__name__)


class BaseResource(Resource):
    method_decorators = []
    controller = None

    def __init__(self, *args, **kwargs):
        if isinstance(self.controller, BaseController):
            self.controller.set_context(self.get_context(*args, **kwargs))

    def get_context(self, *args, **kwargs):
        return Context(self, request, *args, **kwargs)

    def marshal_response(self, response_data, schema):
        try:
            return marshal(response_data, schema)
        except Exception:
            # Will log the exception automatically
            abort(API_ERRORS['InternalServerError']['status_code'],
                  **API_ERRORS['InternalServerError'])

    # def get(self, *args, **kwargs):
    #     return self.marshal_response(
    #         self.controller.get_response(),
    #         self.controller.marshal_fields), 200
    #
    # def post(self, *args, **kwargs):
    #     return self.marshal_response(
    #         self.controller.get_response(),
    #         self.controller.marshal_fields), 200
    #
    # def put(self, *args, **kwargs):
    #     return self.marshal_response(
    #         self.controller.get_response(),
    #         self.controller.marshal_fields), 200
    #
    # def delete(self, *args, **kwargs):
    #     return self.marshal_response(
    #         self.controller.get_response(),
    #         self.controller.marshal_fields), 200
