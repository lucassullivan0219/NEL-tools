
# Updated setup.py
from setuptools import setup, find_packages

setup(
    name="mat_tools",                # Change this to match your folder name
    version="0.1.0",
    packages=find_packages(),        # This will find the 'mat_tools' directory
    install_requires=[
        "numpy",
        "scipy",
        "h5py"
    ],
    python_requires='>=3.6',
)
