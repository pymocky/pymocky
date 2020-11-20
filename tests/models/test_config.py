import unittest

from pymocky.models.config import Config
from pymocky.models.constants import Constants
from pymocky.utils.args import Args


class ConfigTests(unittest.TestCase):
    def test_default_values(self):
        self.assertEqual(Config.verbose, False)
        self.assertEqual(Config.host, "")
        self.assertEqual(Config.port, 0)
        self.assertEqual(Config.path, "")
        self.assertEqual(Config.scenario, Constants.DEFAULT_SCENARIO)
        self.assertEqual(Config.delay, 0)
        self.assertEqual(Config.watch, False)
        self.assertEqual(Config.cors, False)

    def test_init_from_args(self):
        cmd_line = (
            "--verbose --host=127.0.0.1 --port=9000 --path=/my-path --delay=1 --scenario=my-scenario --watch "
            "--cors"
        )

        parser = Args.create_parser()
        argv = cmd_line.split()
        args = parser.parse_args(argv)

        Config.init_from_args(args)

        self.assertEqual(len(argv), 8)
        self.assertEqual(Config.host, "127.0.0.1")
        self.assertEqual(Config.port, Constants.PORT)
        self.assertEqual(Config.path, "/my-path")
        self.assertEqual(Config.delay, 1)
        self.assertEqual(Config.scenario, "my-scenario")
        self.assertEqual(Config.watch, True)
        self.assertEqual(Config.cors, True)

    def test_init_from_args_dict(self):
        cmd_line = {
            "verbose": True,
            "host": "127.0.0.1",
            "port": 9000,
            "path": "/my-path",
            "delay": 1,
            "scenario": "my-scenario",
            "watch": True,
            "cors": True,
        }

        Config.init_from_args_dict(cmd_line)

        self.assertEqual(len(cmd_line), 8)
        self.assertEqual(Config.host, "127.0.0.1")
        self.assertEqual(Config.port, Constants.PORT)
        self.assertEqual(Config.path, "/my-path")
        self.assertEqual(Config.delay, 1)
        self.assertEqual(Config.scenario, "my-scenario")
        self.assertEqual(Config.watch, True)
        self.assertEqual(Config.cors, True)

    def test_empty_dict(self):
        cmd_line = Config.empty_dict()

        self.assertEqual(len(cmd_line), 8)
        self.assertEqual(Config.host, "")
        self.assertEqual(Config.port, 0)
        self.assertEqual(Config.path, "")
        self.assertEqual(Config.delay, 0)
        self.assertEqual(Config.scenario, Constants.DEFAULT_SCENARIO)
        self.assertEqual(Config.watch, False)
        self.assertEqual(Config.cors, False)
