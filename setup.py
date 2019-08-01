from setuptools import setup, find_packages
from df_backend import __version__

setup(
    name="df_backend",
    version=__version__,
    install_requires=[
        'click',
        'django',
        'django-rest-framework',
        'requests',
        'waitress'
        ],
    author='William Normandin',
    author_email='bill@pokeybill.us',
    packages=find_packages(),
    license='MIT',
    description='Backend API for the DunderFunk game client',
    entry_points={'console_scripts': ['df-api=df_backend.cli:cli']},
    include_package_data=True
    )
