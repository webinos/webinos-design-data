#!/bin/bash -x

# You'll want to change the below values based on your own local installation 
export CAIRIS_SRC=/home/irisuser/CAIRIS/cairis/cairis
export PYTHONPATH=$CAIRIS_SRC
export CAIRIS_SQL=$CAIRIS_SRC/sql
export GIT_DIR=/home/irisuser/webinos/wp2
export DBHOST=localhost
export DBUSER=irisuser
export DBPASSWORD=""
export DBNAME=arm
export TMP_DIR=/tmp
export OUTPUT_DIR=/tmp/deliverable #This is where files for the D2.4 and D2.5 deliverable go
export SOFFICE_STARTUP_SLEEP=15  #How long to wait before soffice starts up in headless model 

export MODELS_DIR=$GIT_DIR/cairisModels
export CM_DIR=$GIT_DIR/conceptMaps
export REQ_DIR=$GIT_DIR/requirements
export SC_DIR=$GIT_DIR/scenarios
export UC_DIR=$GIT_DIR/usecases
export PERSONA_DIR=$GIT_DIR/personas
export ARCHITECTURE_DIR=$GIT_DIR/architecture
export VIEWS_DIR=$ARCHITECTURE_DIR/architecturalpatterns
export AP_DIR=$ARCHITECTURE_DIR/attackpatterns
export WP2_SCRIPT_DIR=$GIT_DIR/scripts

echo '*** Creating output directory ***'
if [ -d $OUTPUT_DIR ]
then
  rm -rf $OUTPUT_DIR
fi
mkdir $OUTPUT_DIR

echo '*** Building scenarios ***'
$WP2_SCRIPT_DIR/rs2ct.py 

echo '*** Building use cases ***'
$WP2_SCRIPT_DIR/ru2cu.py 

echo '*** Building requirements ***'
soffice -headless -accept="socket,host=127.0.0.1,port=2002;urp;" -nofirststartwizard &
sleep $SOFFICE_STARTUP_SLEEP
$WP2_SCRIPT_DIR/xr2cr.py 

echo '*** Building traceability model ***'
$WP2_SCRIPT_DIR/d2ra.py

echo '*** Build pattern mitigation data ***'
$WP2_SCRIPT_DIR/xm2ga.py

echo '*** Creating CAIRIS database ***'
/usr/bin/mysql -h $DBHOST -u $DBUSER --password=$DBPASSWORD --database $DBNAME < $CAIRIS_SQL/init.sql
/usr/bin/mysql -h $DBHOST -u $DBUSER --password=$DBPASSWORD --database $DBNAME < $CAIRIS_SQL/procs.sql

echo '*** Importing threat and vulnerability types and template threats and vulnerabilities from OWASP, CWE, and CAPEC***'
$CAIRIS_SRC/cimport.py --type tvtypes $MODELS_DIR/OWASPTypes.xml
$CAIRIS_SRC/cimport.py --type tvtypes $CAIRIS_SQL/cwecapec_tv_types.xml --overwrite 0
$CAIRIS_SRC/cimport.py --type directory $CAIRIS_SQL/owasp_directory.xml
$CAIRIS_SRC/cimport.py --type directory $CAIRIS_SQL/cwecapec_directory.xml --overwrite 0
$CAIRIS_SRC/cimport.py --type directory $MODELS_DIR/D28TV.xml --overwrite 0

echo '*** Importing environments ***'
$CAIRIS_SRC/cimport.py --type project $MODELS_DIR/environments.xml

echo '*** Importing actors ***'
$CAIRIS_SRC/cimport.py --type riskanalysis $MODELS_DIR/actors.xml

echo '*** Importing known assets based on D2.8 ***'
$CAIRIS_SRC/cimport.py --type assets $MODELS_DIR/externalAssets.xml 

echo '*** Importing backlog lists ***'
$CAIRIS_SRC/cimport.py --type usability $MODELS_DIR/coreBacklog.xml
$CAIRIS_SRC/cimport.py --type usability $MODELS_DIR/platformImplementation.xml

echo '*** Importing personas ***'
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/alice.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/anna.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/carlos.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/clara.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/david.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/eric.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/ethan.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/frankie.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/gary.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/georg.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/gloria.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/harold.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/helen.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/irwin.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/jessica.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/jimmy.xml
$CAIRIS_SRC/cimport.py --type processes $PERSONA_DIR/jimmy_impliedCharacteristics.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/justin.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/peter.xml
$CAIRIS_SRC/cimport.py --type usability $PERSONA_DIR/richard.xml

echo '*** Importing scenarios ***'
$CAIRIS_SRC/cimport.py --type usability $TMP_DIR/scenarios.xml

echo '*** Importing use cases ***'
$CAIRIS_SRC/cimport.py --type usability $TMP_DIR/usecases.xml

echo '*** Importing requirements ***'
$CAIRIS_SRC/cimport.py --type requirements $TMP_DIR/requirements.xml

echo '*** Importing traceability data ***'
$CAIRIS_SRC/cimport.py --type associations $TMP_DIR/assocs.xml
$CAIRIS_SRC/cimport.py --type associations $TMP_DIR/scenarioTraceability.xml

echo '*** Importing architectural patterns ***'

for CCVIEW in $(ls $VIEWS_DIR/*.xml)
do
  $CAIRIS_SRC/cimport.py --type architecturalpattern $CCVIEW
done

echo '*** Importing attack patterns ***'
for APATTERN in $(ls $AP_DIR/*.xml)
do
  $CAIRIS_SRC/cimport.py --type attackpattern $APATTERN
done

echo '*** Import misusability cases ***'
$CAIRIS_SRC/cimport.py --type all $MODELS_DIR/misusability.xml --overwrite 0

echo '*** Import persona synopses ***'
$CAIRIS_SRC/cimport.py --type synopses $MODELS_DIR/persona_synopses.xml 

echo '*** Importing component traceability ***'
$WP2_SCRIPT_DIR/um2cu.py
$CAIRIS_SRC/cimport.py --type associations $TMP_DIR/componentAssociations.xml


echo '*** Automatically situate architectural patterns ***'
$WP2_SCRIPT_DIR/autoSituateArchitecturalPatterns.py

echo '*** Mitigate attack patterns where possible ***'
$CAIRIS_SRC/cimport.py --type all $TMP_DIR/pattern_mitigation.xml --overwrite 0

echo echo '*** Exporting scenarios with traceability data ***'
$CAIRIS_SRC/cexport.py --type scenarios $OUTPUT_DIR/scenarios.txt

echo echo '*** Exporting use cases ***'
$CAIRIS_SRC/cexport.py --type usecases $OUTPUT_DIR/usecases.txt

echo echo '*** Exporting requirements ***'
$CAIRIS_SRC/cexport.py --type requirements $OUTPUT_DIR/requirements.txt

echo '*** Export architectural patterns ***'
$CAIRIS_SRC/cexport.py --type architecture $OUTPUT_DIR/D036_ArchitecturalPatterns.txt

echo '*** Export attack patterns ***'
$CAIRIS_SRC/cexport.py --type attackpatterns $OUTPUT_DIR/D036_AttackPatterns.txt
