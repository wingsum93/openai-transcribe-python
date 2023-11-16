from setuptools import setup, find_packages

setup(
    name='subtitle_generator',
    version='0.0.1',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[...],  # Dependencies listed in requirements.txt
    entry_points={
        'console_scripts': [
            'generate-subtitles=subtitle_generator.cli:main',
        ],
    },
    # Other metadata like author, description, etc.
)
