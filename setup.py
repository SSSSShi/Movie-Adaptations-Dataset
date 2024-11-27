from setuptools import setup, find_packages

setup(
    name="goodreads-analysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scipy'
    ],
)
