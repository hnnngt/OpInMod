
"""Setup information of OpInMod.
"""

from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='opinmod',
      version='0.1',
      author='Henning Thiesen',
      license='MIT',
      author_email='henning.thiesen@hs-flensburg.de',
      description='A model generator for unit commitment and economic inertia dispatch modelling',
      long_description=read('README.rst'),
      long_description_content_type='text/x-rst',
      packages=find_packages(),
      install_requires=['oemof.solph == 0.4.4',
                        'pandas == 1.3.2',
                        'scipy == 1.7.1',
                        'pyomo == 5.7.2']
      )
