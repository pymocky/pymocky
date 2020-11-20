import re

from pymocky.models.config import Config
from pymocky.utils.log import Log


class CherryPyStatus(object):
    def __init__(self, mapping_handler):
        self.mapping_handler = mapping_handler

    def response(self):
        string = "<html>"
        string += "<body>"

        string += "Server running correctly<br/><br/>"
        string += "Parsed interceptors:<br/>"
        string += "_" * 80
        string += "<br/>"

        for item in self.mapping_handler.mappings:
            string += " - " + item.file_name + "<br/>"

            request = str(item.request).replace("\n", "<br/>")
            string += "<br/>"
            string += "Request:<br/>" + request + "<br/>"
            string += "<br/>"

            response = item.response.title()
            string += "Response:<br/>" + response + "<br/>"
            string += "_" * 80
            string += "<br/>"

        string += "</body>"
        string += "</html>"
        return string

    @staticmethod
    def is_status(url):
        is_status_url = (
            re.match(r"^.*(127\.0\.0\.1|localhost|pymocky)(:\d*)?/status$", url)
            is not None
        )

        return is_status_url


def cherry_py_check_status(func):
    def parse_status(*args, **kwargs):
        self = args[0]

        if not hasattr(self, "status"):
            self.status = CherryPyStatus(self.mapping_handler)

        if self.status.is_status(self.cherrypy.url()):
            if Config.verbose:
                Log.info("Accessing: status")

            return self.status.response()

        return func(self)

    return parse_status
