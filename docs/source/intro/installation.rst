Installation / Setup
=====================

On versions of Ubuntu greater than 16.0, you need to install a few system
packages first:

.. code-block:: bash

    $ sudo apt-get install libffi-dev libssl-dev


Nautilus is availible using pip:

.. code-block:: bash

    $ pip install nautilus

Necessary Background Processes
-------------------------------

In order to run a nautilus cloud, you must have kafka running on your local machine. For more information on
kafka including how to run it locally, go [here](http://www.bogotobogo.com/Hadoop/BigData_hadoop_Zookeeper_Kafka_single_node_single_broker_cluster.php).
