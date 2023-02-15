# This is the main file of the autoexplain package.
# It is used to parse the command line arguments and call the appropriate function.

import argparse
from autoexplain.subcommands import add, set_key, generate_readme, generate_unittests
from importlib.metadata import version


def main():

    parser = argparse.ArgumentParser(prog="autoexplain")
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    
    parser.add_argument("-v", "--version", action="store_true")

    parser_add = subparsers.add_parser("add", help="Add documentation to one or more files")
    parser_add.add_argument("files", nargs="+", help="Files to add documentation to")
    parser_add.add_argument("--no_stage", action="store_true", default=False, help="Don't stage modified files")
    parser_add.add_argument("--silent", action="store_true", default=False, help="Don't ask for confirmation")

    parser_unittests = subparsers.add_parser("gen-unittests", help="Generate unittest for a code file")
    parser_unittests.add_argument("files", nargs=2, help="Files to add documentation to")
    parser_unittests.add_argument("--silent", action="store_true", default=False, help="Don't ask for confirmation")

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

    if args.command == "gen-unittests":
        generate_unittests(files=args.files, silent=args.silent)

    if args.version:
        print(version("autoexplain"))


if __name__ == "__main__":
    main()
