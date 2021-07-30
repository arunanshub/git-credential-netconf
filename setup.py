from setuptools import find_packages, setup

setup(
    name="git-credential-netconf",
    version="0.2.0",
    author="Arunanshu Biswas",
    author_email="mydellpc07@gmail.com",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    entry_points=dict(
        console_scripts=[
            "git-credential-netconf=git_credential_netconf.__main__:main"
        ],
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    install_requires=["python-gnupg"],
    url="https://github.com/arunanshub/git-credential-netconf",
)
