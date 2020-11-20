import re


def is_valid_re(value):
    try:
        re.compile(value)
        return True
    except re.error:
        return False
