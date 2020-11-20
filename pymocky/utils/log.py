import sys

from colorama import Fore


class Log(object):
    @staticmethod
    def error(msg, fatal=True):
        """
        Print error message and exit with error code 10
        unless 'fatal' is False.

        :param msg:     string message
        :param fatal:   exit program with error code 10 if True (default is true)
        """
        print("{0}[ERROR]{1} {2}".format(Fore.RED, Fore.RESET, msg))

        if fatal:
            sys.exit(10)

    @staticmethod
    def warn(msg):
        """
        Print a warning message

        :param msg:     string message
        """
        print("{0}[WARNING]{1} {2}".format(Fore.YELLOW, Fore.RESET, msg))

    @staticmethod
    def ok(msg=""):
        """
        Print a green 'ok' message

        :param msg:     string message
        """
        print("{0}[OK]{1} {2}".format(Fore.GREEN, Fore.RESET, msg))

    @staticmethod
    def fail(msg="", fatal=True):
        """
        Print a red 'fail' message

        :param msg:     string message
        :param fatal:   exit program with error code 10 if True (default is true)
        """
        print("{0}[FAIL]{1} {2}".format(Fore.RED, Fore.RESET, msg))

        if fatal:
            sys.exit(10)

    @staticmethod
    def failed(msg):
        """
        Print a red 'fail' message

        :param msg:     string message
        """
        print("{0}[FAILED]{1} {2}".format(Fore.RED, Fore.RESET, msg))

    @staticmethod
    def info(msg):
        """
        Print a yellow 'info' message

        :param msg:     string message
        """
        print("{0}[INFO]{1} {2}".format(Fore.YELLOW, Fore.RESET, msg))

    @staticmethod
    def normal(msg):
        """
        Print a normal log message

        :param msg:     string message
        """
        print(msg)

    @staticmethod
    def colored(msg, color):
        """
        Print a colored log message

        :param msg:     text message
        :param color:   color escape sequence (e.g. Fore.YELLOW)
        """
        print("{0}{1}{2}".format(color, msg, Fore.RESET))

    @staticmethod
    def separator():
        """
        Print separator line
        """
        Log.normal("-" * 80)

    @staticmethod
    def multiple_matches(items):
        """
        Print multiple matches

        :param items:     list of items
        """
        string = ""

        for item in items:
            string += "- " + item.file_name
            string += "\n" + str(item.request) + "\n"

        Log.normal(string)

        return string

    @staticmethod
    def request_url(url):
        """
        Print request url

        :param url:     request url
        """
        Log.info("Request with url: {0}".format(url))

    @staticmethod
    def log_request(request, url):
        """
        Print request data

        :param request:     request dict
        :param url:         request url
        """
        Log.ok("Request matched for URL: {0}".format(url))

        Log.info("Request configured:")
        Log.normal(request.__dict__)

    @staticmethod
    def log_response(response):
        """
        Print response data

        :param response:     response dict
        """
        Log.info("Response configured:")
        Log.normal(response.__dict__)
