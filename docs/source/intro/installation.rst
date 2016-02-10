Installation / Setup
=====================

Nautilus is availible using pip:

>>> pip install nautilus

Necessary Background Processes
-------------------------------

In order to run a nautilus cloud, you must have both consul and rabbitmq
installed and running on localhost.

Linux
^^^^^^^^
If you are developing on a linux machine, this is easily accomplished using
docker. For docker installation instructions please visit here. Once you have
successfully installed docker, the two process can be started with two separate
commands in your console:

>>> docker run -d -p "5672:5672" rabbitmq
>>> docker run -d -p "8500:8500" progrium/consul -server -bootstrap

For more information using docker, please read the documentation here.


Apple / OSX
^^^^^^^^^^^^^
Because of some complications with docker on OSX, we cannot bind our containers
to ports on localhost. This leaves us with two options: point nautilus to
another location (we'll have to do this for every service), or run the two
processes by hand. Since we do not  yet support the first option, OSX users
need to install these two packages by hand using MacPorts or homebrew.

Once consul and rabbitmq are installed, they can be run in background processes
with the following command in the terminal

>>> consul -server -bootstrap &
>>> rabbitmq-server &


Notes
-----------
    * I know this is tedious to ensure when developping, I will eventually start these processes for you if they are not present when running a service.
