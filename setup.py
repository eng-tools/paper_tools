from setuptools import setup, find_packages

about = {}
with open("pypaper/__about__.py") as fp:
    exec(fp.read(), about)

setup(name='pypaper',
      version=about['__version__'],
      description='A command line tool to aid the writing of research papers',
      url='https://github.com/eng-tools/pypaper',  # The URL to the github repo
      author='Maxim Millen',
      author_email='mmi46@uclive.ac.nz',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[
          "bibtexparser",
      ],
      include_package_data=True,  # need to include files listed in MANIFEST.in
      keywords="research latex",
      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[dev,test]
      extras_require={
          'test': ['pytest'],
      },
      python_requires='>=3',
      package_data={
          'models': ['models_data.dat'],
      },
      zip_safe=False)


# From python packaging guides
# versioning is a 3-part MAJOR.MINOR.MAINTENANCE numbering scheme,
# where the project author increments:

# MAJOR version when they make incompatible API changes,
# MINOR version when they add functionality in a backwards-compatible manner, and
# MAINTENANCE version when they make backwards-compatible bug fixes.


# run:
# python setup.py sdist
# twine upload dist/*