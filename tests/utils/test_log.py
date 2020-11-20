import os
import unittest
from io import StringIO
from unittest.mock import patch

from colorama import Fore

from app.models.mapping_item import MappingItem
from app.models.mapping_request import MappingRequest
from app.models.mapping_response import MappingResponse
from app.utils.log import Log


class LogTests(unittest.TestCase):
    def test_error(self):
        with patch("sys.stdout", new=StringIO()) as output:
            Log.error("error message", False)
            self.assertIn("error message", output.getvalue().strip())

    def test_error_with_fatal(self):
        with patch("sys.stdout", new=StringIO()) as output:
            exited = False

            try:
                Log.error("error message", True)
            except SystemExit as e:
                if e.code == 10:
                    exited = True

            self.assertIn("error message", output.getvalue().strip())
            self.assertEqual(exited, True)

    def test_warn(self):
        with patch("sys.stdout", new=StringIO()) as output:
            Log.warn("warn message")
            self.assertIn("warn message", output.getvalue().strip())

    def test_ok(self):
        with patch("sys.stdout", new=StringIO()) as output:
            Log.ok("ok message")
            self.assertIn("ok message", output.getvalue().strip())

    def test_fail(self):
        with patch("sys.stdout", new=StringIO()) as output:
            Log.fail("fail message", False)
            self.assertIn("fail message", output.getvalue().strip())

    def test_fail_with_fatal(self):
        with patch("sys.stdout", new=StringIO()) as output:
            exited = False

            try:
                Log.fail("fail message", True)
            except SystemExit as e:
                if e.code == 10:
                    exited = True

            self.assertIn("fail message", output.getvalue().strip())
            self.assertEqual(exited, True)

    def test_failed(self):
        with patch("sys.stdout", new=StringIO()) as output:
            Log.failed("failed message")
            self.assertIn("failed message", output.getvalue().strip())

    def test_info(self):
        with patch("sys.stdout", new=StringIO()) as output:
            Log.info("info message")
            self.assertIn("info message", output.getvalue().strip())

    def test_normal(self):
        with patch("sys.stdout", new=StringIO()) as output:
            Log.normal("normal message")
            self.assertIn("normal message", output.getvalue().strip())

    def test_colored(self):
        with patch("sys.stdout", new=StringIO()) as output:
            Log.colored("colored message", Fore.YELLOW)
            self.assertIn("colored message", output.getvalue().strip())

    def test_separator(self):
        with patch("sys.stdout", new=StringIO()) as output:
            Log.separator()
            self.assertIn("-" * 80, output.getvalue().strip())

    def test_multiple_matches(self):
        with patch("sys.stdout", new=StringIO()) as output:
            data = {
                "id": "test",
                "request": {
                    "url": "",
                    "method": "get",
                },
                "response": {
                    "text": "Hello World",
                },
            }

            mapping = MappingItem(data, "dummy.yml", os.getcwd())

            Log.multiple_matches(
                [
                    mapping,
                    mapping,
                ]
            )

            self.assertIn(
                "- dummy.yml\nID: test\nScenario: default\nURL: \nMethod: GET\nQuery String: \n- dummy.yml\nID: "
                "test\nScenario: default\nURL: \nMethod: GET\nQuery String:",
                output.getvalue().strip(),
            )

    def test_url(self):
        with patch("sys.stdout", new=StringIO()) as output:
            Log.request_url("http://localhost/pymocky")
            self.assertIn(
                "Request with url: http://localhost/pymocky", output.getvalue().strip()
            )

    def test_request(self):
        with patch("sys.stdout", new=StringIO()) as output:
            data = {
                "url": "http://localhost/pymocky",
                "method": "post",
                "body": "Hello World",
            }

            request = MappingRequest("test_id", "test_scenario", data)

            Log.log_request(request, "http://localhost/pymocky")

            self.assertIn("'mock_id': 'test_id'", output.getvalue().strip())
            self.assertIn("'mock_scenario': 'test_scenario'", output.getvalue().strip())
            self.assertIn("'url': 'http://localhost/pymocky'", output.getvalue().strip())
            self.assertIn("'method': 'post'", output.getvalue().strip())
            self.assertIn("'headers': {}", output.getvalue().strip())
            self.assertIn("'body': 'Hello World'", output.getvalue().strip())
            self.assertIn("'form_fields': {}", output.getvalue().strip())
            self.assertIn("'query_string': ''", output.getvalue().strip())

    def test_response(self):
        with patch("sys.stdout", new=StringIO()) as output:
            data = {
                "url": "http://localhost/pymocky",
                "method": "post",
                "body": "Hello World",
            }

            response = MappingResponse("test_id", "test_scenario", data, os.getcwd())

            Log.log_response(response)

            self.assertIn("'mock_id': 'test_id'", output.getvalue().strip())
            self.assertIn("'mock_scenario': 'test_scenario'", output.getvalue().strip())
            self.assertIn("'method': 'post'", output.getvalue().strip())
            self.assertIn("'body': 'Hello World'", output.getvalue().strip())
            self.assertIn("'status': 200", output.getvalue().strip())
            self.assertIn("'headers': {}", output.getvalue().strip())
            self.assertIn("'headers': {}", output.getvalue().strip())
