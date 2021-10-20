================================
Open Inertia Modelling (OpInMod)
================================

**A model generator for unit commitment and economic inertia dispatch modelling**


.. contents::
    :depth: 1
    :local:
    :backlinks: top


Introduction
============

Open Inertia Modelling (OpInMod) is a modelling framework desigened to create unit commitment 
and economic inertia dispatch optimisation problems. Present energy system modelling generators 
do not consider power system inertia in unit commitment and economic dispatch modelling to assess 
future energy system pathways. However, maintaining sufficient power system inertia in power 
systems is the foundation for power frequency controllability.
OpInMod closes this gap. Synchronous inertia from synchronously connected rotating masses
as well as synthetic inertia from wind turbines and battery storage units are considered to 
contribute to the overall power system inertia. 

OpInMod inherits the logic and philosophy of the `Open energy modelling framework (oemof) <https://github.com/oemof/oemof>`_.

Everybody is welcome to use and/or develop OpInMod!

Contribution and questions are welcome via opening a pull-request or an issue on GitHub. 

.. _installation_label:

Installation
============

If you have a working Python3 environment, you need to get the repository and install. Do:

::

    pip install git+https://github.com/hnnngt/opinmod.git#egg=opinmod


OpInMod does not work as a stand alone. The following dependencies are needed and have to be 
installed separately: 

* Pyomo = 5.7.2
* pandas = 1.3.2
* scipy = 1.7.1
* oemof.solph = 0.4.4

OpInMod is tested with the above listed versions of libraries and Python version 3.8.10. 

To run optimisation models, at least one solver has to be installed. Please check the well 
documented solver installation section in the `oemof-documentation <https://oemof-solph.readthedocs.io/en/latest/readme.html#installing-a-solver>`_

Contributing
============

A warm welcome to all who want to join developing and contribute to OpInMod.
Contribution and questions are welcome via opening a pull-request or an issue. 


Citing
======




.. _solph_examples_label:

Examples & Documentation
========================

You can find four examples in `OpInMod's example repository <https://github.com/hnnngt/OpInMod_Examples>`_ on github to download or clone. 
The four examples are based on oemof's `simple dispatch example <https://github.com/oemof/oemof-examples/tree/master/oemof_examples/oemof.solph/v0.4.x/simple_dispatch>`_
Further comments and elaborations on how to use OpInMod are provided in the example repository.

Acknowledgement
===============
Since OpInMod inherits the Open Energy Modelling Framework - `oemof <https://github.com/oemof/oemof>`_, 
the constant work and efforts of the oemof developer group is acknowledged. 


License
=======

Copyright (c) 2021 Henning Thiesen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


