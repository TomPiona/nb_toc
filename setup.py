from setuptools import setup

version = '0.1.2'

setup(
    name='nb_toc',
    version=version,
    description='Creates a table of contents for Jupyter Notebooks',
    url='https://github.com/tompiona/nb_toc',
    download_url = 'https://github.com/tompiona/nb_toc/archive/{}.tar.gz'.format(version),
    author='Ronald Walker',
    install_requires=[
          'decorator',
          'ipython-genutils',
          'jsonschema',
          'jupyter-core',
          'nbformat',
          'six',
          'traitlets'
      ],
    author_email='ronald.walker@berkeley.edu',
    keywords='juypter notebook table of contents internal links hyperlinks',
    py_modules=["nb_toc"],
)
