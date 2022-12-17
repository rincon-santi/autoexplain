"""
This code is used to add documentation to one or more files. The code uses the OpenAI API to generate a summary of the code.

The code uses the following classes and functions:

    - main: This function is used to parse the command line arguments and call the appropriate function.

    - add: This function is used to add documentation to one or more files.

    - set_key: This function is used to set the OpenAI key.
"""

import argparse
import sys
sys.path.insert(1,'.')
from src.subcommands import add, set_key, generate_readme

def main():
    """
    This function is used to parse the command line arguments and call the appropriate function.
    """

    parser = argparse.ArgumentParser(prog="autoexplain")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    parser_add = subparsers.add_parser("add", help="Add documentation to one or more files")
    parser_add.add_argument("files", nargs="+", help="Files to add documentation to")


    parser_set_key = subparsers.add_parser("set-key", help="Set OpenAI key")
    parser_set_key.add_argument("key", nargs=1, help="OpenAI key")

    subparsers.add_parser("gen-readme", help="Generate README.md for this folder contents")

    args = parser.parse_args()

    if args.command == "add":
        add(args)

    if args.command == "set-key":
        set_key(args)

    if args.command == "gen-readme":
        generate_readme()


if __name__ == "__main__":
    main()
