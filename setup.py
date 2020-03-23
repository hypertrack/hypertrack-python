import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hypertrack",
    version="3.0.3",
    author="HyperTrack",
    author_email="help@hypertrack.com",
    description="HyperTrack API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.hypertrack.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["requests==2.22.0"]
)
