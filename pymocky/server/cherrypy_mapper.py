from time import sleep

from pymocky.models.config import Config
from pymocky.utils.log import Log
from pymocky.server.cherrypy_reload import cherry_py_check_reload
from pymocky.server.cherrypy_status import cherry_py_check_status
from pymocky.server.cherrypy_update_scenario import cherry_py_check_update_scenario


class CherryPyMapper(object):
    def __init__(self, mapping_handler=None, cherrypy=None):
        self.mapping_handler = mapping_handler
        self.cherrypy = cherrypy

    @cherry_py_check_status
    @cherry_py_check_update_scenario
    @cherry_py_check_reload
    def handle_request(self):
        request = self.cherrypy.to_mapper_request()

        if Config.verbose:
            Log.info("Request data:")
            Log.normal(request)
        else:
            Log.request_url(self.cherrypy.url())

        items = self.mapping_handler.mapping_item_for_mapping_request(request)

        if len(items) == 0:
            self.cherrypy.response.status = 500
            Log.failed("No response found for request: {0}".format(self.cherrypy.url()))
            return "No response found for request"

        if len(items) > 1:
            Log.warn("Matched {0:d} items, choosing the first one".format(len(items)))

            if Config.verbose:
                Log.multiple_matches(items)

        matched_item = items[0]
        response = matched_item.response

        if Config.verbose:
            Log.log_request(matched_item.request, self.cherrypy.url())

        delay = Config.delay

        if delay > 0:
            delay = delay / 1000

            if Config.verbose:
                Log.info("Delay: {0:.3f}ms".format(delay))

            sleep(delay)

        self.cherrypy.response.status = response.status
        self.fill_headers(response.headers)

        if Config.verbose:
            Log.log_response(response)

        return response.body_response()

    def check_status(func):
        def parse_status(*args, **kwargs):
            print(args)
            return ""

        return parse_status

    def fill_headers(self, headers):
        if type({}) is not type(headers):
            return

        for key in headers.keys():
            self.cherrypy.response.headers[key] = headers[key]
