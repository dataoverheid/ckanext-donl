from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(
    name='ckanext-donl',
    version=version,
    description="CKAN data.overheid.nl extensions",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Bram Rombouts, Jesse Klaasse',
    author_email='bram.rombouts@indicia.nl, jesse.klaasse@indicia.nl',
    url='http://data.overheid.nl/',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.donl'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        donl_theme=ckanext.donl.plugin:ThemePlugin
        donl_ipm=ckanext.donl.model.ipm_plugin:IpmPlugin
    ''',
)
