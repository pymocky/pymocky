import os
import unittest

from pymocky.models.config import Config
from pymocky.models.mapping_request import MappingRequest
from pymocky.models.mapping_response import MappingResponse


class MappingResponseTests(unittest.TestCase):
    def setUp(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
            }
        )

    def test_title(self):
        data = {
            "body_image": "extras/sample/images/image1.png",
        }

        mapping_response = MappingResponse(None, None, data, "")

        self.assertEqual("extras/sample/images/image1.png", mapping_response.title())

    def test_clear(self):
        data = {
            "body_image": "extras/sample/images/image1.png",
            "status": 200,
        }

        mapping_response = MappingResponse(None, None, data, "")
        mapping_response.clear()

        self.assertEqual(0, mapping_response.status)

    def test_file_not_found(self):
        data = {
            "body_file": "extras/sample/files/not-found.json",
        }

        mapping_response = MappingResponse(None, None, data, "")

        self.assertEqual(404, mapping_response.status)

    def test_headers(self):
        data = {
            "headers": {"Content-Type": "application/json"},
        }

        mapping_response = MappingResponse(None, None, data, "")

        self.assertEqual({"Content-Type": "application/json"}, mapping_response.headers)

    def test_python_process_data(self):
        data = {
            "body_python": "extras/sample/files/dummy.py",
        }

        request_data = {"form_fields": {"username": "My username"}}

        mapping_request = MappingRequest("", "", request_data)

        mapping_response = MappingResponse(None, None, data, "")
        mapping_response.process_python_data({"request": mapping_request})

        self.assertEqual(200, mapping_response.status)
        self.assertIn("My username", mapping_response.body.value)


if __name__ == "__main__":
    unittest.main()
