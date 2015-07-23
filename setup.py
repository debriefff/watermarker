import os

from distutils.core import setup

import watermarker

with open('pypi_doc.txt') as file:
    long_description = file.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-watermarker',
    version=watermarker.__version__,
    packages=['watermarker'],
    include_package_data=True,
    url='https://github.com/Skycker/watermarker',
    license='BSD License',
    author='Kirill Kostyukhin',
    description='A tool for easy working with watermarks in django projects',
    long_description=long_description,
    keywords="django, watermark, watermarks, watermarker, image",
    install_requires=['pillow'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
