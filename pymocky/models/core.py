import requests

from pymocky import __version__
from pymocky.models.constants import Constants
from pymocky.server.cherrypy_server import CherryPyServer
from pymocky.utils.log import Log


class Core(object):
    class __Core:
        pass

    instance = None

    def __init__(self, arg):
        if not Core.instance:
            Core.instance = Core.__OnlyOne(arg)
        else:
            Core.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)

    @staticmethod
    def run(args):
        if args.update_scenario:
            scenario = args.update_scenario

            if not scenario:
                scenario = Constants.DEFAULT_SCENARIO

            Log.info("Changing to scenario {0}...".format(scenario))

            try:
                r = requests.get(
                    "{0}/pymocky/update-scenario?scenario={1}".format(
                        args.server_host,
                        scenario,
                    )
                )

                if r.status_code == 200:
                    Log.ok("Scenario updated")
                else:
                    Log.failed("Scenario not updated: {0:d}".format(r.status_code))
            except requests.exceptions.RequestException as e:
                Log.error("Scenario update error: {0}".format(e))
        elif args.reload:
            Log.info("Reloading...")

            try:
                r = requests.get("{0}/pymocky/reload".format(args.server_host))

                if r.status_code == 200:
                    Log.ok("Reloaded")
                else:
                    Log.failed("Reload failed: {0:d}".format(r.status_code))
            except requests.exceptions.RequestException as e:
                Log.error("Reload error: {0}".format(e))
        elif args.version:
            Log.normal("Version: {0}".format(__version__.__version__))
        else:
            if not args.path:
                Log.error("Path argument is required (--path or -p)")

            CherryPyServer.start()
