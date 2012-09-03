The *webinos* design data repository
==

This repository contains the design data used as part of the development of the *[webinos](https://github.com/webinos/Webinos-Platform "webinos")* project.   *webinos* is a "Secure Web Operating System Application Delivery Environment" designed to run web applications across multiple devices.

The data in this repository includes use cases, scenarios, personas, requirements, architectural models and security and privacy analysis for the platform.  Most of this information is either in XML or text format.

CAIRIS
--

The content of this repository is was created to work with [cairis](https://github.com/failys/CAIRIS "CAIRIS").  CAIRIS is a Requirements Management tool for specifying secure and usable systems.


Getting started
--

* Download the CAIRIS tool from https://github.com/failys/CAIRIS and install it as per the instructions
* Download the contents of this repository
* Modify the beginning of the file 'scripts/regenerate.sh' :
<pre>
export CAIRIS_SRC= ... # This should be the caris directory, ending in "/CAIRIS/cairis/cairis"
export PYTHONPATH=$CAIRIS_SRC
export CAIRIS_SQL=$CAIRIS_SRC/sql
export GIT_DIR=  ...# This is the directory of this repository
export DBHOST= ... # Your database host 
export DBUSER= ... # Your database user name
export DBPASSWORD= ... # Your database password
export DBNAME= ... # The database name, usually set to 'arm'
</pre>
* run the regenerate script.  This will import all of the data into the CAIRIS database
* start CAIRIS









