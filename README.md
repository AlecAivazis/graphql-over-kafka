# nautilus

[![Build Status](https://travis-ci.org/nautilus/nautilus.svg?branch=master)](https://travis-ci.org/nautilus/nautilus)
[![Coverage Status](https://coveralls.io/repos/github/nautilus/nautilus/badge.svg?branch=master)](https://coveralls.io/github/nautilus/python?branch=master)

Nautilus is a framework for event-driven microservices. It attempts to provide extendible 
answers to common questions when building a moden web application so that you can focus
on what you do best: building awesome, scalable services. Some of these features include:

* Distributed authentication
* Message passing
* Couple-free service joins
* Service API versioning (coming soon!)
* A flexible GraphQL API that adapts as services come online 
* Distributed/remote database administration (coming soon!)

Full documentation is hosted [here](http://nautilus.github.io/python/).

***NOTE***: At the moment, this project should be considered an experiment using kafka to perform service joins across 
            very fine grain services. If you are interested in helping, please get in touch!

## Requirements
* >= Python 3.5
* Kafka
