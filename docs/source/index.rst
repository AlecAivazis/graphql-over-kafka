.. nautilus documentation master file, created by
   sphinx-quickstart on Tue Feb  9 00:14:56 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
    :hidden:

    intro/index
    services/index
    handlers/index
    api/index
    utilities/index
    internals/index

Welcome to Nautilus!
=====================

While microservices  have been all the rage for some time now, there
has been very little released that provides an "out of the box" solution
for those developers looking to quickly produce distributed/cloud-based
applications without having to think about how all the moving parts fit
together.


Nautilus is a framework for flux based microservices that looks to provide
extendible implementations of common aspects of a cloud so that you can focus
on what you do best: building massively scalable web applications. Some of these
features include:

    * Service registration
    * Distributed authentication
    * Message passing
    * Data retrieval and API gateway construction
    * Distributed/remote database administration


At the moment, there is only a python implementation of the nautilus spec, but
there are plans for more languages - stay tuned!
