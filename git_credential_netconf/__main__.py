import argparse
import os
import sys

from . import netconf

APP_NAME = "git-credential-netconf"

APP_DESC = """\
"""

CLI_APP_EPILOG = """\
git-credential-netconf is licensed under MIT license.

Visit <https://github.com/arunanshub/git-credential-netconf> for more info.
"""


def main():
    ps = argparse.ArgumentParser(
        prog=APP_NAME,
        description=APP_DESC,
        epilog=CLI_APP_EPILOG,
    )
    ps.add_argument(
        "-g",
        "--gpg",
        help="The `gpg` program to use.",
        default="gpg",
    )
    sub = ps.add_subparsers(
        help="The credential command to use.",
        dest="command",
        required=True,
    )
    parse_get = sub.add_parser("get")

    # unsupported by this manager
    sub.add_parser("store")
    sub.add_parser("erase")

    ps.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Show output of `gpg` (it prints into `stderr`).",
    )
    parse_get.add_argument(
        "-f",
        "--file",
        default=os.path.expanduser("~/.netconf.gpg"),
        help="The `.netconf.gpg` file to use.",
    )

    args = ps.parse_args()

    # we only support "get"
    if args.command == "get":
        try:
            # send data to stdout
            sys.stdout.write(
                netconf.parse_config(
                    netconf.decrypt_file(
                        args.file,
                        gpg_exec=args.gpg,
                        print_stderr=args.debug,
                    )
                )
                + "\n"
            )
            sys.stdout.flush()

        except (Exception, KeyboardInterrupt) as err:
            raise SystemExit(f"ERROR: {err}")
