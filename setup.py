import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setuptools.setup(
    name='nfl-play-gen-api',
    version="0.0.1",
    author="Brent Satterwhite",
    author_email="bsatterwhite@gmail.com",
    description="REST API for generating or sampling NFL plays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsatterwhite3/nfl-play-gen-api",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.7',
)
