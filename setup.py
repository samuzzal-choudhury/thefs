from setuptools import setup, find_packages

setup(
    name='thefs',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'flask'
    ],
    entry_points={
        'console_scripts': [
            'thefs=thefs.main:main'
        ],
    },
)

