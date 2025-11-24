from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qrng-api",
    version="1.0.0",
    author="QRNG API",
    author_email="support@qrngapi.com",
    description="Official Python SDK for QRNG API - Quantum Random Number Generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qrng-api/python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "websocket-client>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "mypy>=0.990",
        ],
    },
    keywords="quantum random number generator entropy cryptography",
    project_urls={
        "Documentation": "https://qrngapi.com/docs",
        "Source": "https://github.com/qrng-api/python-sdk",
        "Tracker": "https://github.com/qrng-api/python-sdk/issues",
    },
)
