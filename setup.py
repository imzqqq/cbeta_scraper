#!/usr/bin/python3

from distutils.core import setup
import io
import os

# Long description
here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='CBETA_scraper',
    packages=['CBTA-Scraper'],
    version='0.1.0',
    description='Tool for scraping CBETA',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['CBETA', 'scraper', 'python', "crawl"],
    install_requires=[
        'selenium', 'pandas', 'chromedriver-autoinstaller', 'urllib3'
    ],
    classifiers=[
        'Development Status :: 5 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
