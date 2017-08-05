#!/bin/bash -x

# You'll want to change the below values based on your own local installation 
export CAIRIS_ROOT=/home/cairisuser/cairis
export CAIRIS_SRC=$CAIRIS_ROOT/cairis
export GIT_DIR=/home/cairisuser/webinos-design-data
export URL=http://localhost:7071
export DBNAME=webinos
export TMP_DIR=/tmp

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

echo '*** Building scenarios ***'
$WP2_SCRIPT_DIR/rs2ct.py 

echo '*** Building use cases ***'
$WP2_SCRIPT_DIR/ru2cu.py 

echo '*** Building requirements ***'
$WP2_SCRIPT_DIR/xr2cr.py 

echo '*** Building traceability model ***'
$WP2_SCRIPT_DIR/d2ra.py

echo '*** Build pattern mitigation data ***'
$WP2_SCRIPT_DIR/xm2ga.py

echo '*** Importing threat and vulnerability types and template threats and vulnerabilities from OWASP, CWE, and CAPEC***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --create  --overwrite --type tvtypes $MODELS_DIR/OWASPTypes.xml 
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type tvtypes $CAIRIS_ROOT/examples/threat_vulnerability_types/cwecapec_tv_types.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --overwrite --type directory $CAIRIS_ROOT/examples/directories/owasp_directory.xml 
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type directory $CAIRIS_ROOT/examples/directories/cwecapec_directory.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type directory $MODELS_DIR/D28TV.xml 

echo '*** Importing environments ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type project $MODELS_DIR/environments.xml

echo '*** Importing actors ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type riskanalysis $MODELS_DIR/actors.xml

echo '*** Importing known assets based on D2.8 ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type assets $MODELS_DIR/externalAssets.xml 

echo '*** Importing backlog lists ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $MODELS_DIR/coreBacklog.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $MODELS_DIR/platformImplementation.xml

echo '*** Importing miscallaneous CSP event data ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type processes $MODELS_DIR/installCodes.xml

echo '*** Importing personas ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/alice.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/anna.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/carlos.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/clara.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/david.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/eric.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/ethan.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/frankie.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/gary.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/georg.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/gloria.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/harold.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/helen.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type processes $PERSONA_DIR/helen_impliedCharacteristics.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/irwin.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/jessica.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/jimmy.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type processes $PERSONA_DIR/jimmy_impliedCharacteristics.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/justin.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/peter.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $PERSONA_DIR/richard.xml

echo '*** Importing persona images ***'
$WP2_SCRIPT_DIR/importObjectImages.py --url $URL --database $DBNAME --image_dir $PERSONA_DIR --type persona

echo '*** Importing scenarios ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $TMP_DIR/scenarios.xml

echo '*** Importing use cases ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type usability $TMP_DIR/usecases.xml

echo '*** Importing requirements ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type requirements $TMP_DIR/requirements.xml

echo '*** Importing traceability data ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type associations $TMP_DIR/assocs.xml
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type associations $TMP_DIR/scenarioTraceability.xml

echo '*** Importing architectural patterns ***'
$WP2_SCRIPT_DIR/autoSituateArchitecturalPatterns_webservices.py --url $URL --database $DBNAME --environment Complete

for CCVIEW in $(ls $VIEWS_DIR/*.xml)
do
  $CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type architecturalpattern $CCVIEW
done

echo '*** Importing attack patterns ***'
for APATTERN in $(ls $AP_DIR/*.xml)
do
  $CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type attackpattern $APATTERN
done

echo '*** Importing persona images ***'
$WP2_SCRIPT_DIR/importObjectImages.py --url $URL --database $DBNAME --image_dir $PERSONA_DIR --type attacker

echo '*** Import misusability cases ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type all $MODELS_DIR/misusability.xml

echo '*** Import persona synopses ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type synopses $MODELS_DIR/persona_synopses.xml 

echo '*** Importing component traceability ***'
$WP2_SCRIPT_DIR/um2cu.py
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type associations $TMP_DIR/componentAssociations.xml

echo '*** Automatically situate architectural patterns ***'
$WP2_SCRIPT_DIR/autoSituateArchitecturalPatterns_webservices.py --url $URL --database $DBNAME --environment Complete

echo '*** Mitigate attack patterns where possible ***'
$CAIRIS_SRC/bin/web_cimport.py --url $URL --database $DBNAME --type all $TMP_DIR/pattern_mitigation.xml 
