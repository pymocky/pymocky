import unittest

from pymocky.models.header_matcher import HeaderMatcher


class HeaderMatcherTests(unittest.TestCase):
    def test_dict_headers(self):
        headers = {
            "Content-Type": "application/json",
            "Content-Length": "123",
        }

        other_headers = {
            "Content-Type": "application/json",
            "Content-Length": "123",
        }

        hm = HeaderMatcher(headers)
        matches = hm.matches(other_headers)

        self.assertEqual(matches, True)

    def test_dict_headers_not_match(self):
        headers = {
            "Content-Type": "application/json",
        }

        other_headers = {
            "Content-Length": "123",
        }

        hm = HeaderMatcher(headers)
        matches = hm.matches(other_headers)

        self.assertEqual(matches, False)

    def test_list_headers(self):
        headers = [
            "Content-Type",
            "Content-Length",
        ]

        other_headers = {
            "Content-Type": "application/json",
            "Content-Length": "123",
        }

        hm = HeaderMatcher(headers)
        matches = hm.matches(other_headers)

        self.assertEqual(matches, True)

    def test_list_headers_not_match(self):
        headers = [
            "Content-Type",
        ]

        other_headers = {
            "Content-Length": "123",
        }

        hm = HeaderMatcher(headers)
        matches = hm.matches(other_headers)

        self.assertEqual(matches, False)

    def test_string_headers(self):
        headers = "Content-Type"

        other_headers = {
            "Content-Type": "application/json",
            "Content-Length": "123",
        }

        hm = HeaderMatcher(headers)
        matches = hm.matches(other_headers)

        self.assertEqual(matches, True)

    def test_string_headers_not_match(self):
        headers = "Content-Type"

        other_headers = {
            "Content-Length": "123",
        }

        hm = HeaderMatcher(headers)
        matches = hm.matches(other_headers)

        self.assertEqual(matches, False)

    def test_header_key_not_match(self):
        headers = ["Content-Type", "application/json"]

        other_headers = {
            "Content-Length": "123",
        }

        hm = HeaderMatcher(headers)
        match = hm.header_match(headers, other_headers)

        self.assertEqual(match, False)
