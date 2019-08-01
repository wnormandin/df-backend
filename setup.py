from setuptools import setup, find_packages
from df_backend import __version__

setup(
    name="df_backend",
    version=__version__,
    install_requires=[
        'django',
        'django-rest-framework',
        'django-waitress'
        ],
    author='William Normandin',
    author_email='bill@pokeybill.us',
    packages=find_packages(),
    license='MIT',
    description='Backend API for the DunderFunk game client'
    )
