import os.path

from setuptools import setup


VERSION = "1.0.0.dev1"


if __name__ == "__main__":
    with open(os.path.join("machotools", "__version.py"), "wt") as fp:
        fp.write("__version__ = '{0}'".format(VERSION))

    with open("README.rst", "rt") as fp:
        long_description = fp.read()

    setup(name="machotools",
          version=VERSION,
          author="David Cournapeau",
          author_email="cournape@gmail.com",
          description="A small library + CLI tool to manipulate Mach-0 binaries",
          long_description=long_description,
          license="BSD",
          packages=["machotools", "machotools.tests"],
          install_requires=["macholib"],
          classifiers=[
              "Programming Language :: Python :: 2.7",
              "Programming Language :: Python :: 3.5",
              "Programming Language :: Python :: 3.6",
          ])
