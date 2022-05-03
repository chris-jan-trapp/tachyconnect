import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tachyconnect",
    version="0.3.1",
    author="Christian Trapp",
    author_email="trapp@gbv.de",
    description="Leica total stations and Qt via python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gbv/tachyconnect",
    project_urls={
        "Bug Tracker": "https://github.com/gbv/tachyconnect/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=["pyqt5"]
)
