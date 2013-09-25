from setuptools import setup

if __name__ == "__main__":
    setup(name="machotools",
          version="0.0.3.dev",
          author="David Cournapeau",
          author_email="cournape@gmail.com",
          license="BSD",
          packages=["machotools", "machotools.tests"],
          install_requires=["macholib"])
