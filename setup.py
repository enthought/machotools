import os.path as op

from setuptools import setup

VERSION = "0.1.0.dev1"

if __name__ == "__main__":
    with open(op.join("machotools", "__version.py"), "wt") as fp:
        fp.write("__version__ = '{}'".format(VERSION))

    setup(name="machotools",
          version=VERSION,
          author="David Cournapeau",
          author_email="cournape@gmail.com",
          license="BSD",
          packages=["machotools", "machotools.tests"],
          install_requires=["macholib"])
