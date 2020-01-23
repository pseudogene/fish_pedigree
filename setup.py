#!/usr/bin/env python
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='fish_pedigree',
    version='1.0',
    description='Pedigree Chromosome Drawer.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Michaël Bekaert',
    author_email='michael.bekaert@stir.ac.uk',
    license='GPL',
    url='https://github.com/pseudogene/fish_pedigree',
    keywords='pedigree chromosome ancestry inference',
    scripts=[
        'scripts/vcf2map.py',
        'scripts/map_chr.py',
        'scripts/make_karyotype.py',
        'scripts/R_colours.py'
    ],
    install_requires=['seaborn','biopython'],
)
