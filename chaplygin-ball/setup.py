from setuptools import setup, find_packages

setup(
    name="chaplygin",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Educational simulation of the Chaplygin ball — rolling without slipping, with numerical RK45 and visualization support.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chaplygin-ball",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20",
        "scipy>=1.8",
        "matplotlib>=3.5",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Education",
    ],
    include_package_data=True,
)
