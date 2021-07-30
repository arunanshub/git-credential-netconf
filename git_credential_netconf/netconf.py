import configparser
import os
import sys
from typing import Iterable, Optional

import gnupg

# Alternative names for some of the attributes used by `git-credential`.
# This is mostly compatible with `git-credential-netrc.perl`, except for
# `machine`/`host` parameter, which is deduced from section name.
#
# See: https://git-scm.com/docs/git-credential#IOFMT
ATTRIBUTES = {
    # `host`
    "machine": "host",
    "host": "host",
    # `path`
    "path": "path",
    # `password`
    "password": "password",
    # `protocol`
    "port": "protocol",
    "protocol": "protocol",
    # `username`
    "login": "username",
    "user": "username",
    "username": "username",
}

# potential candidates for configuration files for git.
CONFIGS = (
    os.path.normpath(os.path.expanduser("~/.gitconfig")),
    os.path.normpath("./.git/config"),
)


class _GitConfig:
    """Git's configuration file reader class."""

    def __init__(self, gitconfigs: Iterable[str] = CONFIGS):
        self._conf = configparser.ConfigParser(interpolation=None)
        self._conf.read(gitconfigs)

    @property
    def gpg_exec(self) -> str:
        """The GPG executable configured for Git."""
        return self._conf.get("gpg", "program", fallback="gpg")


def decrypt_file(
    filename: str,
    *,
    gpg_exec: Optional[str] = None,
    print_stderr: bool = False,
) -> str:
    """Decrypt `filename` using `gpg` and return the output as `str`.

    Args:
        filename: Name of the file to decrypt.

    Keyword Arguments:
        gpg_exec: The `gpg` program to use. Uses `gpg` by default.
        print_stderr:
            Whether to print the output of `gpg` to `stderr`. `True` enables
            printing.

    Returns:
        str: Decrypted data as string.

    Raises:
        FileNotFoundError: If the file `filename` does not exist.
        ValueError:
            If `gpg` was unable to decrypt the file, or any other error
            occurred.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename!r} does not exist.")

    gconf = _GitConfig()

    gpg = gnupg.GPG(gpg_exec or gconf.gpg_exec)
    with open(filename, "rb") as f:
        res = gpg.decrypt_file(f)

    if print_stderr:
        for line in res.stderr.splitlines():
            # avoid the overly verbose [GNUPG:] messages
            if not line.startswith("[GNUPG:]"):
                print(line, file=sys.stderr, flush=True)

    if not res.ok:
        raise ValueError(f"GnuPG failed to decrypt: {res.status!r}")

    return str(res)


def parse_config(data: str) -> str:
    """
    Parse the configuration data `data` and return a `git-credential`
    compatible string.

    Only the first section name is used; subsequent sections are ignored.

    Args:
        data: The configuration data to parse.

    Returns:
        str: A `git-credential` compatible data.

    Raises:
        ValueError: If the `data` cannot be parsed.
    """
    conf = configparser.ConfigParser(interpolation=None)

    try:
        conf.read_string(data)
    except configparser.Error as err:
        raise ValueError(f"Failed to parse configuration data: {err}") from err

    try:
        section = conf[conf.sections()[0]]
    except IndexError as err:
        raise ValueError(
            "Invalid configuration data; section missing."
        ) from err

    output = {}
    port_set = False

    for attr in sorted(section.keys() & ATTRIBUTES.keys()):
        if ATTRIBUTES[attr] == "host":
            output["host"] = section[attr]  # set `host` early-on
            try:
                # set `port` to `host` if it is an `int`
                output["host"] += f':{int(section["port"])}'
                port_set = True
            except (ValueError, KeyError):
                pass
        else:
            if port_set and attr == "port":
                # don't set a `numeric` value for `protocol` if `port` is set
                # in `host`
                continue
            output[ATTRIBUTES[attr]] = section[attr]

    return "\n".join((f"{k}={v}" for k, v in output.items()))
