import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rtneat-python",
    version="0.0.1",
    author="Ciro García",
    author_email="kolterdev@gmail.com",
    description="A real-time NEAT implementation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kolterdyx/RT_NEAT_Python",
    project_urls={
        "Bug Tracker": "https://github.com/Kolterdyx/RT_NEAT_Python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
