import unittest

from mock import Mock

from app.utils.log import Log
from app.server.cherrypy_mapper import CherryPyMapper


class CherryPyMapperTests(unittest.TestCase):
    def test_return_correct_body_for_multiple_response(self):
        item1 = Mock(file_name="file1")
        item1.request = "request1"

        item2 = Mock(file_name="file2")
        item2.request = "request2"

        # Config = Mock(verbose=True)

        mapper = CherryPyMapper()
        mapper.cherrypy = Mock()
        mapper.cherrypy.url = Mock(return_value="some url")

        body = Log.multiple_matches([item1, item2])

        self.assertEqual(
            body,
            "- file1\nrequest1\n- file2\nrequest2\n",
        )

    def test_can_set_headers(self):
        mock_mapper = Mock()
        item1 = Mock()
        item1.response = Mock(status=1, headers={"header_key": "header_value"})
        mock_mapper.mapping_item_for_mapping_request = Mock(return_value=[item1])

        mock_cherry = Mock()
        mock_cherry.response = Mock(status=1, headers={})
        mock_cherry.url = Mock(return_value="ss")

        self.assertEqual(mock_cherry.response.headers, {})

        cherry_mapper = CherryPyMapper(
            mapping_handler=mock_mapper, cherrypy=mock_cherry
        )
        cherry_mapper.handle_request()

        self.assertEqual(
            mock_cherry.response.headers,
            {
                "header_key": "header_value",
            },
        )
