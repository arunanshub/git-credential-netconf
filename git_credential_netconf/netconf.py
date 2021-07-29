import configparser
import os
import subprocess
import sys

# Alternative names for some of the attributes used by `git-credential`.
# This is mostly compatible with `git-credential-netrc.perl`, except for
# `machine`/`host` parameter, which is deduced from section name.
#
# See: https://git-scm.com/docs/git-credential#IOFMT
ATTRIBUTES = {
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


def decrypt_file(
    filename: str,
    *,
    gpg_exec: str = "gpg",
    print_stderr: bool = False,
) -> str:
    """Decrypt `filename` using `gpg` and return the output as `str`.

    Args:
        filename: Name of the file to decrypt.

    Keyword Arguments:
        gpg_exec: The `gpg` program to use. Uses `gpg` by default.
        print_stderr:
            Whether to redirect `stderr` of `gpg` to `stderr`. `False` disables
            printing to `stderr`.

    Returns:
        str: Decrypted data as string.

    Raises:
        FileNotFoundError: If the file `filename` does not exist.
        SubprocessError:
            If `gpg` was unable to decrypt the file, or any error occurred.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename!r} does not exist.")

    p = subprocess.Popen(
        ["-o -", "-d", filename],  # "-o -" sends data to stdout
        executable=gpg_exec,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    retcode = p.wait()
    stdout, stderr = p.communicate()

    if retcode:
        raise subprocess.SubprocessError(
            f"Error while decrypting {filename!r}:\n{stderr.decode()}"
        )

    if print_stderr:
        # redirect `gpg`'s `stderr` output to `stderr`
        print(stderr.decode(), file=sys.stderr)

    return stdout.decode()


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
    except configparser.ParsingError as err:
        raise ValueError("Failed to parse configuration data.") from err

    try:
        section = conf[conf.sections()[0]]
    except IndexError as err:
        raise ValueError(
            "Invalid configuration data; section missing."
        ) from err

    output = {"host": section.name}  # set host value early-on

    for attr in section:
        if attr in ATTRIBUTES:
            output[ATTRIBUTES[attr]] = section[attr]

    return "\n".join((f"{k}={v}" for k, v in output.items()))
