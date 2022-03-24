import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multimatching",
    version="0.1.0",
    author="Rohak Rastogi, Donald R. Sheehy and Siddharth Sheth",
    author_email="don.r.sheehy@gmail.com",
    description="A Python package for computing bottleneck distance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donsheehy/multimatching",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pdsketch',
                      'ortools'
                     ],
)
