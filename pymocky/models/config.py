from pymocky.models.constants import Constants


class Config(object):
    verbose = False

    host = ""
    port = 0
    path = ""
    scenario = Constants.DEFAULT_SCENARIO

    delay = 0

    watch = False
    cors = False

    @classmethod
    def init_from_args(cls, args):
        cls.verbose = args.verbose
        cls.host = args.host
        cls.port = int(args.port)
        cls.path = args.path
        cls.delay = int(args.delay)
        cls.scenario = args.scenario
        cls.watch = args.watch
        cls.cors = args.cors

    @classmethod
    def init_from_args_dict(cls, args):
        cls.verbose = args["verbose"] if "verbose" in args else False
        cls.host = args["host"] if "host" in args else Constants.HOST
        cls.port = int(args["port"]) if "port" in args else Constants.PORT
        cls.path = args["path"] if "path" in args else ""
        cls.delay = int(args["delay"]) if "delay" in args else 0
        cls.scenario = args["scenario"] if "scenario" in args else ""
        cls.watch = args["watch"] if "watch" in args else False
        cls.cors = args["cors"] if "cors" in args else False

    @classmethod
    def empty_dict(cls):
        args = {
            "verbose": False,
            "host": "",
            "port": 0,
            "path": "",
            "delay": 0,
            "scenario": "",
            "watch": False,
            "cors": False,
        }

        return args
