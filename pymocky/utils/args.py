from argparse import ArgumentParser

from pymocky.models.constants import Constants


class Args(object):
    @staticmethod
    def create_parser():
        parser = ArgumentParser(prog="pymocky")

        optional = parser.add_argument_group("optional arguments")
        optional.add_argument(
            "--path",
            "-p",
            help="Configuration path to read YAML files",
        )
        optional.add_argument(
            "--host",
            help="Host to bind",
            default=Constants.HOST,
        )
        optional.add_argument(
            "--port",
            help="Port to listen",
            default=Constants.PORT,
        )
        optional.add_argument(
            "--scenario",
            help="Define startup scenario",
            default=Constants.DEFAULT_SCENARIO,
        )
        optional.add_argument(
            "--update-scenario",
            help="Connect to server and update scenario",
            default="",
        )
        optional.add_argument(
            "--server-host",
            help="Server host to connect",
            default="http://localhost:{0}".format(Constants.PORT),
        )
        optional.add_argument(
            "--delay",
            help="Enable delay on each request and response",
            default=0,
        )
        optional.add_argument(
            "--reload",
            help="Connect to server and reload YAML files",
            action="store_true",
        )
        optional.add_argument(
            "--cors",
            help="Enable CORS",
            action="store_true",
        )
        optional.add_argument(
            "--watch",
            help="Enable live reload on path",
            action="store_true",
        )
        optional.add_argument(
            "--verbose",
            help="Enable verbose mode",
            action="store_true",
        )
        optional.add_argument(
            "--version",
            help="Show version",
            action="store_true",
        )

        return parser
