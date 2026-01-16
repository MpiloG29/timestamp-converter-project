from setuptools import setup, find_packages

setup(
    name="timestamp-converter",
    version="0.1.0",
    description="A timestamp converter utility",
    author="MpiloG29",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
