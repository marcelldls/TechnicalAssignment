from setuptools import setup

setup(
    py_modules=['package_statistics'],
    entry_points={
        'console_scripts': [
            'package_statistics = package_statistics:main',
        ],
    },
)
