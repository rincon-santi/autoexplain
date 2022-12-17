from setuptools import setup

setup(
    name='autoexplain',
    version='1.0.0',
    description='Use OpenAI capabilities to smooth your document generation',
    author='Santiago Rincon Martinez',
    author_email='rincon.santi@gmail.com',
    packages=['src'],
    install_requires=['openai','configparser','argparse'],
    entry_points={
        'console_scripts': [
            'autoexplain=src.autoexplain:main'
        ]
    }
)