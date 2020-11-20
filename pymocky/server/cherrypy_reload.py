import re

from pymocky.models.config import Config
from pymocky.utils.log import Log


class CherryPyReload(object):
    def __init__(self, mapping_handler):
        self.mapping_handler = mapping_handler

    def response(self):
        string = '{"success": true, "message": "reloaded"}'
        return string

    @staticmethod
    def is_reload(url):
        is_reload_url = (
            re.match(r"^.*(127\.0\.0\.1|localhost|pymocky)(:\d*)?/reload$", url)
            is not None
        )

        return is_reload_url


def cherry_py_check_reload(func):
    def parse_reload(*args, **kwargs):
        self = args[0]

        if not hasattr(self, "reload"):
            self.reload = CherryPyReload(self.mapping_handler)

        if self.reload.is_reload(self.cherrypy.url()):
            if Config.verbose:
                Log.info("Accessing: reload")

            self.mapping_handler.parse_yaml_files()

            Log.ok("Mapping settings rebuilt successfully")

            return self.reload.response()

        return func(self)

    return parse_reload
