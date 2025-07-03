from setuptools import setup, find_packages

# Function to read the contents of requirements.txt and return as a list
def read_requirements():
    with open('requirements.txt') as file:
        return file.read().splitlines()

setup(
    name='subtitle_generator',
    version='0.0.2',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'stt=subtitle_generator.cli_main:cli'
        ],
    },
    author='Eric Ho',
    author_email='wingsum.developer@gmail.com',
    description='A subtitle generation package using Whisper model. It also suport text translation using m2m100 facebook model',
    license='MIT',
    url='https://github.com/wingsum93/openai-transcribe-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]

)
