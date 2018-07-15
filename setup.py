import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mechapy",
    version="0.1.0.dev1",
    author="Brian White",
    author_email="briannwhite@gmail.com",
    description="An object-oriented, pythonic toolbox for mechanical engineering computations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/briannwhite/mechapy",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Development Status :: 2 - Pre-Alpha"
    ),
    install_requires=['numpy', 'matplotlib', 'pandas', 'pint']
)