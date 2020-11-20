import os
import unittest

from pymocky.models.config import Config
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

        self.assertEqual(mapping_response.title(), "extras/sample/images/image1.png")

    def test_clear(self):
        data = {
            "body_image": "extras/sample/images/image1.png",
            "status": 200,
        }

        mapping_response = MappingResponse(None, None, data, "")
        mapping_response.clear()

        self.assertEqual(mapping_response.status, 0)

    def test_file_not_found(self):
        data = {
            "body_file": "extras/sample/files/not-found.json",
        }

        mapping_response = MappingResponse(None, None, data, "")

        self.assertEqual(mapping_response.status, 404)

    def test_headers(self):
        data = {
            "headers": {"Content-Type": "application/json"},
        }

        mapping_response = MappingResponse(None, None, data, "")

        self.assertEqual(mapping_response.headers, {"Content-Type": "application/json"})


if __name__ == "__main__":
    unittest.main()
