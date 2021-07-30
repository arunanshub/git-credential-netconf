# git-credential-netconf

Git credentials management made easy.

# Installation

Use `pip` or `pip3` to install `git-credential-netconf`

```bash
pip install git-credential-netconf
```

or

```bash
pip3 install git-credential-netconf
```

# Introduction

- TODO:  <30-07-21> -

# Usage Overview

- TODO:  <30-07-21> -

# Usage Details

```none
usage: git-credential-netconf [-h] [-g GPG] [-d] [-f FILE] [-q]
                              {get,store,erase} ...

positional arguments:
  {get,store,erase}     The credential operation to use.

optional arguments:
  -h, --help            show this help message and exit
  -g GPG, --gpg GPG     The `gpg` program to use.
  -d, --debug           Show output of `gpg` (it prints into `stderr`).
  -f FILE, --file FILE  The `.netconf.gpg` file to use.
  -q, --quit-on-failure
                        Do not let Git consult any more helpers if an error
                        is encountered while decryption.

git-credential-netconf is licensed under MIT license. Visit
<https://github.com/arunanshub/git-credential-netconf> for more info.
```

# Why another tool?

- TODO:  <30-07-21> -

# License

[MIT](https://choosealicense.com/licenses/mit/)
