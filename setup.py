from setuptools import setup

setup(
    name = 'package_statistics',
    py_modules=['package_statistics'],
    python_requires='>=3.8',
    extras_require={
        'dev': [
            'black',
            'tox',
        ],
    },
    entry_points={
        'console_scripts': [
            'package_statistics = package_statistics:main',
        ],
    },
)
