import re

from pymocky.models.config import Config
from pymocky.utils.log import Log


class CherryPyUpdateScenario(object):
    def __init__(self, mapping_handler):
        self.mapping_handler = mapping_handler

    def response(self):
        string = '{"success": true, "message": "updated"}'
        return string

    @staticmethod
    def is_update_scenario(url):
        is_update_scenario_url = (
            re.match(
                r"^.*(127\.0\.0\.1|localhost|pymocky)(:\d*)?/update-scenario$", url
            )
            is not None
        )

        return is_update_scenario_url


def cherry_py_check_update_scenario(func):
    def parse_update_scenario(*args, **kwargs):
        self = args[0]

        if not hasattr(self, "update_scenario"):
            self.update_scenario = CherryPyUpdateScenario(self.mapping_handler)

        if self.update_scenario.is_update_scenario(self.cherrypy.url()):
            if Config.verbose:
                Log.info("Accessing: update scenario")

            scenario = self.cherrypy.request.params.get("scenario")

            if not scenario:
                scenario = "default"

            Config.scenario = scenario

            Log.info("Scenario changed to: {0}".format(scenario))

            return self.update_scenario.response()

        return func(self)

    return parse_update_scenario
