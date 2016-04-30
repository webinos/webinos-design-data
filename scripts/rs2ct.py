#!/usr/bin/python
from RedmineScenario import RedmineScenario
import re
import os
from stat import *

if __name__ == '__main__':

  outputDir = os.environ['TMP_DIR']

  scDir = os.environ['SC_DIR']
  scFiles = os.listdir(scDir)

  envLookup = {'ID':'Identity','DA':'Discovery and Addressing','NM':'Remote Notifications and Messaging','PS':'Policy and Security','NC':'Negotiation and Compatibility','LC':'Lifecycle','CAP':'Device and Service Functional Capability','TMS':'Transfer and Management of State'}


  xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE usability PUBLIC "-//CAIRIS//DTD CAIRIS USABILITY 1.0//EN" "http://cairis.org/dtd/usability.dtd">\n\n<usability>\n\n'
  assocBuf = '<?xml version="1.0"?>\n<!DOCTYPE associations PUBLIC "-//CAIRIS//DTD CAIRIS ASSOCIATIONS 1.0//EN" "http://cairis.org/dtd/associations.dtd">\n\n<associations>\n\n'
  for scFile in scFiles:
     
     fileMode = os.stat(scDir + '/' + scFile).st_mode
     if S_ISDIR(fileMode):
       continue

     print 'Converting ',scFile
     rs = RedmineScenario(scFile)
     if (rs.envName == ''):
       rs.envName = envLookup[re.sub('[0-9]','',scFile.split('-')[1].split('.')[0])]
     xmlBuf += rs.markupXml() + '\n'
     assocBuf += rs.markupTraceability() + '\n'
  xmlBuf += '</usability>'
  assocBuf += '</associations>'
  outputFile = outputDir + '/scenarios.xml'
  assocFile = outputDir + '/scenarioTraceability.xml'
  f = open(outputFile,'w')
  f2 = open(assocFile,'w')
  f.write(xmlBuf)
  f2.write(assocBuf)
  f.close()
  f2.close()
