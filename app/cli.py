import mimetypes
from argparse import ArgumentParser

import colorama

from app.models.config import Config
from app.models.core import Core
from app.utils.args import Args


def main():
    # initialize
    colorama.init()
    mimetypes.init()

    # command line params
    parser = Args.create_parser()
    args = parser.parse_args()

    # apply config
    Config.init_from_args(args)
    Core.run(args)


if __name__ == "__main__":
    main()
