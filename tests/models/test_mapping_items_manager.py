import os
import unittest
from os import path

from mock import Mock

from pymocky.models.config import Config
from pymocky.models.mapping_items_manager import MappingItemsManager, Constants


class MappingItemsManagerTests(unittest.TestCase):
    def test_display_name_is_correct(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
                "watch": True,
            }
        )

        mapper = MappingItemsManager()

        names = [mapping.display_name for mapping in mapper.mappings]

        self.assertIn("hello-world", names)
        self.assertIn("images", names)
        self.assertIn("files", names)
        self.assertIn("json", names)
        self.assertIn("scenario", names)

    def test_returns_all_matching_requests(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
            }
        )

        mapper = MappingItemsManager()

        # two matches
        mock_mapping_request = Mock(url="http://localhost/pymock_json_1", method="get")

        self.assertEqual(
            len(mapper.response_for_mapping_request(mock_mapping_request)), 2
        )

        # normal - get
        mock_mapping_request = Mock(
            url="http://localhost/pymock_hello_world", method="get"
        )

        self.assertEqual(
            len(mapper.response_for_mapping_request(mock_mapping_request)), 1
        )

        # normal - post
        mock_mapping_request = Mock(
            url="http://localhost/pymock_hello_world", method="post"
        )

        self.assertEqual(
            len(mapper.response_for_mapping_request(mock_mapping_request)), 0
        )

        # normal - get - with params
        mock_mapping_request = Mock(
            url="http://localhost/pymock_hello_world?name=test", method="get"
        )

        self.assertEqual(
            len(mapper.response_for_mapping_request(mock_mapping_request)), 1
        )

    def test_returns_all_matching_requests_for_method(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
            }
        )

        mapper = MappingItemsManager()

        mock_mapping_request = Mock(
            url="http://localhost/pymock_hello_world?test1", method="Get"
        )
        self.assertEqual(
            len(mapper.response_for_mapping_request(mock_mapping_request)), 1
        )

        mock_mapping_request = Mock(
            url="http://localhost/pymock_hello_world?test2", method="gEt"
        )
        self.assertEqual(
            len(mapper.response_for_mapping_request(mock_mapping_request)), 1
        )

        mock_mapping_request = Mock(
            url="http://localhost/pymock_hello_world?test3", method="post"
        )
        self.assertEqual(
            len(mapper.response_for_mapping_request(mock_mapping_request)), 0
        )

    def test_returns_all_matching_requests_for_default_scenario(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
                "scenario": Constants.DEFAULT_SCENARIO,
            }
        )

        mapper = MappingItemsManager()

        mock_mapping_request = Mock(url="http://localhost/pymock_login", method="post")

        self.assertEqual(
            len(mapper.mapping_item_for_mapping_request(mock_mapping_request)), 1
        )

    def test_returns_all_matching_requests_for_custom_scenario(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
                "scenario": "login-error",
            }
        )

        mapper = MappingItemsManager()

        mock_mapping_request = Mock(url="http://localhost/pymock_login", method="post")

        self.assertEqual(
            len(mapper.mapping_item_for_mapping_request(mock_mapping_request)), 1
        )

    def test_returns_all_matching_requests_for_wrong_scenario(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
                "scenario": "wrong",
            }
        )

        mapper = MappingItemsManager()

        mock_mapping_request = Mock(
            url="http://localhost/pymock_login_wrong", method="post"
        )

        self.assertEqual(
            len(mapper.mapping_item_for_mapping_request(mock_mapping_request)), 0
        )

    def test_returns_all_matching_requests_for_not_exists_scenario(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
                "scenario": "not-exists",
            }
        )

        mapper = MappingItemsManager()

        mock_mapping_request = Mock(url="http://localhost/pymock_login", method="post")

        self.assertEqual(
            len(mapper.mapping_item_for_mapping_request(mock_mapping_request)), 1
        )

    def test_return_body(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
            }
        )

        mapper = MappingItemsManager()

        mock_mapping_request = Mock(
            url="http://localhost:9000/pymock_hello_world?name=test", method="get"
        )

        response = mapper.response_for_mapping_request(mock_mapping_request)[0]

        print(response.body.body_type)

        self.assertIn("Hello world from pymocky!", response.body_response())

    def test_return_status_code(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
            }
        )

        mapper = MappingItemsManager()

        mock_mapping_request = Mock(
            url="http://localhost:9000/pymock_hello_world?name=test", method="get"
        )

        response = mapper.response_for_mapping_request(mock_mapping_request)[0]

        self.assertEqual(response.status, 200)

    def test_return_correct_header(self):
        Config.init_from_args_dict(
            {
                "verbose": True,
                "path": os.path.join(os.getcwd(), "extras", "sample"),
            }
        )

        mapper = MappingItemsManager()

        mock_mapping_request = Mock(
            url="http://localhost:9000/pymock_json_1", method="get"
        )

        response = mapper.response_for_mapping_request(mock_mapping_request)[0]

        self.assertEqual(response.headers["Content-Type"], "application/json")


if __name__ == "__main__":
    unittest.main()
