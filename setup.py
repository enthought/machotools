from setuptools import setup

import machotools

if __name__ == "__main__":
    setup(name="machotools",
          version=machotools.__version__,
          author="David Cournapeau",
          author_email="cournape@gmail.com",
          license="BSD",
          packages=["machotools", "machotools.tests"],
          install_requires=["macholib"])
