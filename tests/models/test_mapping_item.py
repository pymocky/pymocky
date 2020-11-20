import os
import unittest
from os import path

from mock import Mock

from pymocky.models.mapping_item import MappingItem

res_path = os.path.dirname(path.abspath(__file__)) + "/res"


class MappingItemTests(unittest.TestCase):
    def test_handles_mapping_request(self):
        data = {
            "id": "mock1",
            "name": "test1",
            "request": {"method": "GET", "url": ".*1/2.*"},
            "response": {"status": 1234},
        }

        mock_mapping_request = Mock()
        mock_mapping_request.__eq__ = Mock(return_value=True)

        mapping_item = MappingItem(data, "", res_path)
        mapping_item.request = mock_mapping_request

        mapping_item.handles_mapping_request(mock_mapping_request)
        self.assertTrue(mapping_item.request.__eq__.called)

    def test_properties(self):
        data = {
            "id": "mock1",
            "scenario": "scenario1",
            "name": "test1",
            "request": {},
            "response": {},
        }

        mapping_item = MappingItem(data, "dummy.yml", res_path)

        self.assertEqual(mapping_item.mock_id, "mock1")
        self.assertEqual(mapping_item.display_name, "test1")
        self.assertEqual(mapping_item.file_name, "dummy.yml")
        self.assertEqual(mapping_item.mock_scenario, "scenario1")

    def test_uuid_on_mock_id(self):
        data = {
            "request": {},
            "response": {},
        }

        mapping_item = MappingItem(data, "", res_path)

        self.assertIn("-", str(mapping_item.mock_id))
