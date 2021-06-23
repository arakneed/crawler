import setuptools

from arakneed import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arakneed",
    version=__version__,
    author="arakneed",
    author_email="arakneed@somarl.com",
    description="A common use targeted concurrent crawler for any directed graph. It's designed to be easy to use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arakneed/crawler",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=(
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ),
    setup_requires=['wheel'],
    license='MIT',
)
