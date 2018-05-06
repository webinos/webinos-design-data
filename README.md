The *webinos* design data repository
==

This repository contains the design data used as part of the development of the *[webinos](https://github.com/webinos/Webinos-Platform "webinos")* project.   *webinos* is a "Secure Web Operating System Application Delivery Environment" designed to run web applications across multiple devices.

The data in this repository includes use cases, scenarios, personas, requirements, architectural models and security and privacy analysis for the platform.  Most of this information is either in XML or text format.

CAIRIS
--

The content of this repository is was created to work with [cairis](https://github.com/failys/cairis "CAIRIS").  CAIRIS is a platform for specifying secure and usable systems.


Getting started
--

* Install CAIRIS.  You can find instructions on how to install it at https://cairis.org
* Download the contents of this repository
* Modify the beginning of the file 'scripts/regenerate.sh' :

<pre>
export CAIRIS_ROOT=/home/cairisuser/cairis # the top-level directory 
export CAIRIS_SRC=$CAIRIS_ROOT/cairis # the location of the CAIRIS source code and other configuration data
export PYTHONPATH=$CAIRIS_ROOT 
export CAIRIS_SQL=$CAIRIS_SRC/sql
export CAIRIS_CFG=/home/cairisuser/cairis.cnf # Your personalised version of the cairis.cnf template in $CAIRIS_SRC/config
export GIT_DIR=/home/cairisuser/webinos-design-data # This is the directory of this repository
export DBHOST=localhost # Your database host 
export DBUSER=test # Your database user name
export DBPASSWORD=  # Your database password; this will typically be blank
export DBNAME=test_default # The database name.  Each account with have a default database, i.e. test_default for test
</pre>

* Run the regenerate script.  This will import all of the data into the target CAIRIS database.
* start CAIRIS
