import signal
import socket

import cherrypy
import cherrypy_cors

from pymocky.models.config import Config
from pymocky.utils.log import Log
from pymocky.models.mapping_items_manager import MappingItemsManager
from pymocky.server.cherrypy_mapper import CherryPyMapper


class CherryPyServer(object):
    exposed = True

    def __init__(self):
        self.handler = MappingItemsManager()

        Log.ok(
            "Server started successfully at {0}:{1}".format(
                "http://" + socket.gethostbyname(socket.gethostname()),
                cherrypy.config["server.socket_port"],
            )
        )

    @cherrypy.expose
    def default(self, *args, **kwargs):
        mapper = CherryPyMapper(
            mapping_handler=self.handler,
            cherrypy=cherrypy,
        )

        return mapper.handle_request()

    @staticmethod
    def start():
        Log.info("Initializing server...")

        # update config
        cherrypy.config.update(
            {
                "server.socket_port": Config.port,
                "server.socket_host": Config.host,
                "environment": "embedded",
                "tools.encode.text_only": False,
                "cors.expose.on": Config.cors,
            }
        )

        # update config for verbose mode
        if Config.verbose:
            cherrypy.config.update(
                {
                    "log.screen": True,
                }
            )

        # cors
        if Config.cors:
            cherrypy_cors.install()
            Log.info("CORS enabled")

        # listen for signal
        def signal_handler(signal, frame):
            Log.info("Shutting down server...")
            cherrypy.engine.exit()
            Log.ok("Server shutdown successfully")

        signal.signal(signal.SIGINT, signal_handler)

        # start server
        cherrypy.quickstart(CherryPyServer())
