import unittest

from app.models.mapping_request import MappingRequest


class MappingRequestTests(unittest.TestCase):
    def test_equal_to_url(self):
        request_1 = MappingRequest(None, None, {"url": ".*1/2.*"})
        request_2 = MappingRequest(None, None, {"url": ".*1/2.*"})
        self.assertEqual(request_1, request_2)

        request_2 = MappingRequest(None, None, {"url": ".*1/2/3.*"})
        self.assertEqual(request_1, request_2)

        request_1 = MappingRequest(None, None, {"url": ".*1/2/3.*"})
        request_2 = MappingRequest(None, None, {"url": ".*1/2.*"})
        self.assertNotEqual(request_1, request_2)

    def test_check_method_is_equal(self):
        request_1 = MappingRequest(None, None, {"url": ".*1/2.*", "method": "get"})
        request_2 = MappingRequest(None, None, {"url": ".*1/2.*", "method": "gEt"})
        self.assertEqual(request_1, request_2)

        request_1 = MappingRequest(None, None, {"url": ".*1/2.*", "method": "get"})
        request_2 = MappingRequest(None, None, {"url": ".*1/2.*"})
        self.assertNotEqual(request_1, request_2)

        request_1 = MappingRequest(None, None, {"url": ".*1/2.*"})
        request_2 = MappingRequest(None, None, {"url": ".*1/2.*", "method": "get"})
        self.assertEqual(request_1, request_2)

        request_1 = MappingRequest(None, None, {"url": ".*1/2.*", "method": "post"})
        request_2 = MappingRequest(None, None, {"url": ".*1/2.*", "method": "get"})
        self.assertNotEqual(request_1, request_2)

        request_1 = MappingRequest(None, None, {"url": ".*1/2.*", "method": "get"})
        request_2 = MappingRequest(None, None, {"url": ".*1/2.*", "method": "gEt"})
        self.assertEqual(request_1, request_2)

    def test_check_matches_body(self):
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "body": ".*TheKey.*Value.*"}
        )
        request_2 = MappingRequest(
            None, None, {"url": ".*1/2.*", "body": "TheKeyEqual=ATestValueIs"}
        )
        self.assertEqual(request_1, request_2)

        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "body": ".*TheKey.*XTheValue.*"}
        )
        request_2 = MappingRequest(
            None, None, {"url": ".*1/2.*", "body": "TheKeyEqual=TestTheValueIs"}
        )
        self.assertNotEqual(request_1, request_2)

    def test_check_matches_headers(self):
        dic_headers = {"key1": "value1", "key2": "value2"}
        request_2 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": dic_headers}
        )

        # with self.subTest("no headers"):
        request_1 = MappingRequest(None, None, {"url": ".*1/2.*"})
        self.assertEqual(request_1, request_2)

        # with self.subTest("does not have equal headers"):
        dic_headers = {"keyx": "valuex"}
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": dic_headers}
        )
        self.assertNotEqual(request_1, request_2)

        # with self.subTest("has exact headers"):
        dic_headers = {"key1": "value1"}
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": dic_headers}
        )
        self.assertEqual(request_1, request_2)

        # with self.subTest("has pattern value headers"):
        dic_headers = {"key1": "va.*1"}
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": dic_headers}
        )
        self.assertEqual(request_1, request_2)

        # with self.subTest("has pattern key headers"):
        dic_headers = {"k.*1": "value1"}
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": dic_headers}
        )
        self.assertEqual(request_1, request_2)

        # with self.subTest("all headers must match"):
        dic_headers = {"k.*1": "value1", "key2": "value2"}
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": dic_headers}
        )
        self.assertEqual(request_1, request_2)

        dic_headers = {"k.*1": "value1", "k.*2": "v.*2"}
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": dic_headers}
        )
        self.assertEqual(request_1, request_2)

        # with self.subTest("only some match returns false"):
        dic_headers = {"k.*1": "value1", "key3": "value2"}
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": dic_headers}
        )
        self.assertNotEqual(request_1, request_2)

    def test_matches_headers_also_as_string(self):
        dic_headers = {"key1": "value1", "key2": "value2"}
        request_2 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": dic_headers}
        )

        # with self.subTest("matches"):
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": "ke.*val.*"}
        )
        self.assertEqual(request_1, request_2)

        # with self.subTest("does not matches"):
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": "kex.*val.*"}
        )
        self.assertNotEqual(request_1, request_2)

    def test_matches_headers_also_as_array(self):
        dic_headers = {"key1": "value1", "key2": "value2"}
        request_2 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": dic_headers}
        )

        # with self.subTest("all matches"):
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": ["k.*1.*v.*1", "k.*2.*v.*2"]}
        )
        self.assertEqual(request_1, request_2)

        # with self.subTest("some dont match"):
        request_1 = MappingRequest(
            None, None, {"url": ".*1/2.*", "headers": ["k.*1.*v.*1", "k.*3.*v.*2"]}
        )
        self.assertNotEqual(request_1, request_2)

    def test_invalid_body(self):
        request = MappingRequest(None, None, {"body": [".*TheKey.*Value.*"]})

        matches = request.body_matches(request.body)

        self.assertFalse(matches)

    def test_form_fields(self):
        request = MappingRequest(
            None,
            None,
            {
                "form_fields": {
                    "username": "demo",
                    "password": "1234",
                }
            },
        )

        form_fields = {
            "username": "demo",
            "password": "1234",
        }

        matches = request.form_fields_matches(form_fields)

        self.assertTrue(matches)

    def test_invalid_form_fields(self):
        request = MappingRequest(
            None,
            None,
            {
                "form_fields": {
                    "username": "demo",
                }
            },
        )

        form_fields = {
            "password": "1234",
        }

        matches = request.form_fields_matches(form_fields)

        self.assertFalse(matches)

    def test_to_string(self):
        request = MappingRequest(
            None,
            None,
            {
                "url": "login",
                "headers": {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                },
                "form_fields": {
                    "username": "demo",
                },
                "method": "post",
                "body": "Hello World!",
            },
        )

        request_str = request.__str__()

        self.assertIn("ID:", request_str)
        self.assertIn("Scenario:", request_str)
        self.assertIn("URL:", request_str)
        self.assertIn("Method:", request_str)
        self.assertIn("Header:", request_str)
        self.assertIn("Body:", request_str)
        self.assertIn("Form Fields:", request_str)
        self.assertIn("Query String:", request_str)
