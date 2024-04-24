from setuptools import setup, find_packages

setup(
    name="mergecraft",
    version="0.0.4",
    description="A command-line tool to merge files into a temporary file and open in VS Code.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="José Nery",
    author_email="josenerydev@gmail.com",
    url="https://github.com/josenerydev/mergecraft",
    packages=find_packages(),
    install_requires=["pathspec"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "mergecraft=mergecraft.mergecraft:main",
        ],
    },
)
