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

Credential management in Git should not be difficult to use or configure, but
(unfortunately) looking at the existing tools, it is difficult to think about
it, let alone configure them without errors.

**NOT. ANY. MORE!**

Presenting `git-credential-netconf`, and easy yet powerful way to manage your
Git credentials by harnessing the power of **GnuPG!**

# Usage Overview

The following guide assumes you have a GPG key and you have installed `git-credential-netconf`.

1. Create a `.netconf` file in your home directory.

   ```bash
   touch ~/.netconf
   ```

2. Start by filling in your username and password:

   ```conf
   [conf]
   login = yourname
   password = very-secret-password
   ```

   **The `.netconf` file uses configuration file format.**

   [Read more about `.netconf` file.](#about-netconf-file)

3. Encrypt your `.netconf` file with `gpg`

   ```bash
   gpg --recipient yourname@example.com --output ~/.netconf.gpg --encrypt \
       --sign ~/.netconf
   ```

   1. And remove your original `.netconf` for security:

        ```bash
        shred -u ~/.netconf
        ```

4. Now use git without hassle!

   ```bash
   git push
   ```

   This will prompt `git-credential-netconf` to decrypt the `~/.netconf` file
   using `GPG` and fetch the `username` and `password`, among other values.

   You'll be asked for the password to `GPG` private key when decrypting.

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

# About `.netconf` file

- TODO:  <30-07-21> -

# Why another tool?

- TODO:  <30-07-21> -

# License

[MIT](https://choosealicense.com/licenses/mit/)
