from setuptools import setup, find_packages

setup(
    name="took",
    version="0.0.12",
    packages=find_packages(),
     package_data={
        'took': ['resources/hooks/*.sh'],
    },
    entry_points={
        "console_scripts": [
            "took=took.took:main",
            "tk=took.took:main",
        ],
    },
    install_requires=[
        "rich>=13.0.0",
    ],
    author="loaojuz",
    author_email="",
    description="CLI tool to track time spent on tasks.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/joaohenriqueluz/took",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
