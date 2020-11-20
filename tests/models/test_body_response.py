import unittest

from pymocky.models.body_response import BodyResponse


class BodyResponseTests(unittest.TestCase):
    def test_body_type(self):
        self.assertEqual(BodyResponse.NONE, "none")
        self.assertEqual(BodyResponse.RAW, "raw")
        self.assertEqual(BodyResponse.IMAGE, "image")
        self.assertEqual(BodyResponse.JSON, "json")

    def test_body_type_func(self):
        body = BodyResponse(None, None)

        self.assertEqual(body.body_type, BodyResponse.NONE)

    def test_body_type_raw(self):
        data = {"body_raw": "Hello World"}

        res_path = None

        body = BodyResponse(data, res_path)

        self.assertEqual(body.body_type, BodyResponse.RAW)
        self.assertEqual(body.read_value(), "Hello World")

    def test_body_type_raw_invalid(self):
        data = {"body_raw": None}

        res_path = None

        body = BodyResponse(data, res_path)

        self.assertEqual(body.body_type, BodyResponse.RAW)
        self.assertEqual(body.read_value(), "")

    def test_body_type_file(self):
        data = {"body_file": "extras/sample/files/dummy.txt"}

        res_path = None

        body = BodyResponse(data, res_path)

        self.assertEqual(body.body_type, BodyResponse.FILE)
        self.assertEqual(body.read_value().decode(), "Hello World")

    def test_body_type_file_invalid(self):
        data = {"body_file": "extras/sample/files/dummy-invalid.txt"}

        res_path = None

        body = BodyResponse(data, res_path)

        self.assertEqual(body.body_type, BodyResponse.FILE)
        self.assertEqual(body.read_value(), None)

    def test_body_type_json(self):
        data = {"body_json": '{"success": true, "message": "login-ok"}'}

        res_path = None

        body = BodyResponse(data, res_path)

        self.assertEqual(body.body_type, BodyResponse.JSON)
        self.assertIn('\\"success\\": true', body.read_value())
        self.assertIn('\\"message\\": \\"login-ok\\"', body.read_value())

    def test_body_type_json_as_object(self):
        data = {
            "body_json": {
                "success": True,
                "message": "login-ok",
            }
        }

        res_path = None

        body = BodyResponse(data, res_path)

        self.assertEqual(body.body_type, BodyResponse.JSON)
        self.assertIn('"success": true', body.read_value())
        self.assertIn('"message": "login-ok"', body.read_value())

    def test_body_type_image(self):
        data = {"body_image": "extras/sample/images/image1.png"}

        res_path = None

        body = BodyResponse(data, res_path)

        self.assertEqual(body.body_type, BodyResponse.IMAGE)
        self.assertEqual(len(body.read_value()), 9260)
