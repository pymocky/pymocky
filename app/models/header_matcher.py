import re


class HeaderMatcher(object):
    def __init__(self, headers):
        self.headers = headers

    def matches(self, other_headers):
        if isinstance(self.headers, dict):
            return self.dict_header_matches(other_headers)
        elif isinstance(self.headers, list):
            return self.list_header_matches(other_headers)
        elif isinstance(self.headers, str):
            return self.string_header_matches(other_headers)

    def keys_matching_other_headers_keys(self, other_headers):
        ret = []

        for key in self.headers.keys():
            matched_key = self.key_matching_headers_key(other_headers, key)

            if matched_key:
                ret.append((key, matched_key))

        return ret

    def key_matching_headers_key(self, other_headers, key):
        arr = [a_key for a_key in other_headers.keys() if re.match(key, a_key)]
        return arr[0] if arr else None

    def header_match(self, key_tuple, other_header):
        this_key = key_tuple[0]
        other_key = key_tuple[1]

        has_value = other_key in other_header

        if not has_value:
            return False

        this_value = self.headers[this_key]
        other_value = other_header[other_key]

        return re.match(this_value, other_value)

    def dict_header_matches(self, headers):
        matching_keys = self.keys_matching_other_headers_keys(headers)

        if len(matching_keys) != len(self.headers.keys()):
            return False

        return all(
            [self.header_match(key_tuple, headers) for key_tuple in matching_keys]
        )

    def string_header_matches(self, other_headers, this_header=""):
        this_header = this_header if this_header else self.headers
        other_header_strings = [k + v for (k, v) in other_headers.items()]

        return any(re.match(this_header, value) for value in other_header_strings)

    def list_header_matches(self, other_headers):
        return all(
            self.string_header_matches(other_headers, a_header)
            for a_header in self.headers
        )
