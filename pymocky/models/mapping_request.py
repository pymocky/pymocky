import re

from pymocky.models.config import Config
from pymocky.models.header_matcher import HeaderMatcher
from pymocky.utils.log import Log


class MappingRequest(object):
    def __init__(self, mock_id, mock_scenario, data):
        self.mock_id = mock_id
        self.mock_scenario = mock_scenario

        self.url = data.get("url", "")
        self.method = data.get("method", "")
        self.headers = data.get("headers", {})
        self.body = data.get("body", "")
        self.form_fields = data.get("form_fields", {})
        self.query_string = data.get("query_string", "")

    def __eq__(self, other):
        matches_method = self.method_matches(other.method)
        matches_url = self.url_matches(other.url)
        matches_body = self.body_matches(other.body)
        matches_headers = HeaderMatcher(self.headers).matches(other.headers)
        matches_form_fields = self.form_fields_matches(other.form_fields)
        matches_query_string = self.query_string_matches(other.query_string)

        if Config.verbose:
            Log.info("Mock tested:")
            Log.normal("Mock ID: {0}".format(self.mock_id))
            Log.normal("Mock Scenario: {0}".format(self.mock_scenario))
            Log.normal("Request URL: {0}".format(other.url))
            Log.normal("Mock URL: {0}".format(self.url))
            Log.normal(
                "Matches Method: {0}".format(("Yes" if matches_method else "No"))
            )
            Log.normal("Matches URL: {0}".format(("Yes" if matches_url else "No")))
            Log.normal("Matches Body: {0}".format(("Yes" if matches_body else "No")))
            Log.normal(
                "Matches Headers: {0}".format(("Yes" if matches_headers else "No"))
            )
            Log.normal(
                "Matches Form Fields: {0}".format(
                    ("Yes" if matches_form_fields else "No")
                )
            )
            Log.normal(
                "Matches Query String: {0}".format(
                    ("Yes" if matches_query_string else "No")
                )
            )

        return (
            matches_method
            and matches_url
            and matches_body
            and matches_headers
            and matches_form_fields
            and matches_query_string
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def method_matches(self, method):
        return method.lower() == self.method.lower() if self.method else True

    def url_matches(self, url):
        return re.match(self.url, url) is not None

    def body_matches(self, body):
        has_body = self.body != ""

        if has_body:
            if isinstance(body, str):
                return re.match(self.body, body) if has_body else True
            else:
                return False
        else:
            return True

    def form_fields_matches(self, form_fields):
        has_form_fields = self.form_fields != {}

        if has_form_fields:
            for key in self.form_fields.keys():
                if isinstance(form_fields, dict):
                    if key not in form_fields:
                        return False

                    try:
                        if not re.match(self.form_fields[key], form_fields[key]):
                            return False
                    except TypeError:
                        Log.failed("Invalid regex: {0}".format(self.form_fields[key]))
                        return False
                else:
                    return False

        return True

    def query_string_matches(self, query_string):
        has_query_string = self.query_string != ""

        if has_query_string:
            if isinstance(query_string, str):
                return (
                    re.match(self.query_string, query_string)
                    if has_query_string
                    else True
                )
            else:
                return False
        else:
            return True

    def __str__(self):
        result = ""
        result += "ID: {0}".format(self.mock_id)
        result += "\nScenario: {0}".format(self.mock_scenario)
        result += "\nURL: {0}".format(self.url)

        if self.method != "":
            result += "\nMethod: {0}".format(self.method.upper())
        if self.headers != {}:
            result += "\nHeader: {0}".format(self.headers)
        if len(self.body) > 0:
            result += "\nBody: {0}".format(self.body)
        if self.form_fields != {}:
            result += "\nForm Fields: {0}".format(self.form_fields)
        if self.query_string != {}:
            result += "\nQuery String: {0}".format(self.query_string)

        return result
