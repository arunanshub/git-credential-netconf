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
    ps.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Show output of `gpg` (it prints into `stderr`).",
    )
    ps.add_argument(
        "-f",
        "--file",
        default=os.path.expanduser("~/.netconf.gpg"),
        help="The `.netconf.gpg` file to use.",
    )
    ps.add_argument(
        "-q",
        "--quit-on-failure",
        dest="quit",
        action="store_true",
        help="Do not let Git consult any more helpers"
        " if an error is encountered while decryption.",
    )

    # "operation" argument
    sub = ps.add_subparsers(
        help="The credential operation to use.",
        dest="operation",
        required=True,
    )
    sub.add_parser("get")
    # unsupported by this helper
    sub.add_parser("store")
    sub.add_parser("erase")

    args = ps.parse_args()

    # we only support "get"
    if args.operation == "get":
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

        except Exception as err:
            if args.quit:
                print("quit=1")
            raise SystemExit(f"ERROR: {err}")
        except KeyboardInterrupt:
            raise SystemExit("ERROR: Caught keyboard interrupt!")
