"""
Setup script for the QuizMaster package.
"""

from setuptools import setup, find_packages

setup(
    name="quizmaster",
    version="0.1.0",
    description="A Python-based quiz application",
    author="QuizMaster Team",
    author_email="example@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        # Add dependencies here
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)