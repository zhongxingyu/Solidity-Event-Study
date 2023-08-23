import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="gas_reducer",
    version="0.0.1",
    author="solEventStudy",
    author_email="lJSBDFLJWEBHdljkB@outlook.com",
    description="A tool for analyzing solidity events",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SolEventStudy/Solidity-Event-Study",
    include_package_data=True,
    package_data={},
    packages=setuptools.find_packages(),
)