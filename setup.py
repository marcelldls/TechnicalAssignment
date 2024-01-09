from setuptools import setup

setup(
    py_modules=['package_statistics'],
    extras_require={
        'dev': [
            'tox',
        ],
    },
    entry_points={
        'console_scripts': [
            'package_statistics = package_statistics:main',
        ],
    },
)
