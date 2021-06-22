import setuptools

from arakneed import __version__


def read_file(p):
    with open(p, "r") as f:
        return f.read()


setuptools.setup(
    name="arakneed",
    version=__version__,
    author="arakneed",
    author_email="arakneed@somarl.com",
    description="A common use targeted concurrent crawler for any directed graph. It's designed to be easy to use.",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/arakneed/crawler",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=(
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.3",
        "License :: OSI Approved :: MIT License",
    ),
    setup_requires=['wheel'],
    license=read_file('LICENSE'),
)
