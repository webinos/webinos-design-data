#!/usr/bin/python
from RedmineUseCase import RedmineUseCase
import re
import os
from stat import *

if __name__ == '__main__':

  outputDir = os.environ['TMP_DIR']

  ucDir = os.environ['UC_DIR']
  ucFiles = os.listdir(ucDir)
  envLookup = {'ID':'Identity','DA':'Discovery and Addressing','NM':'Remote Notifications and Messaging','PS':'Policy and Security','NC':'Negotiation and Compatibility','LC':'Lifecycle','CAP':'Device and Service Functional Capability','TMS':'Transfer and Management of State'}


  xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE usability PUBLIC "-//CAIRIS//DTD CAIRIS USABILITY 1.0//EN" "http://cairis.org/dtd/usability.dtd">\n\n<usability>\n\n'
  for ucFile in ucFiles:
     fileMode = os.stat(ucDir + '/' + ucFile).st_mode
     if S_ISDIR(fileMode):
       continue
     print 'Converting ',ucFile
     ruc = RedmineUseCase(ucFile)
     if (ruc.envName == ''):
       ruc.envName = envLookup[re.sub('[0-9]','',ucFile.split('.')[0])]
     xmlBuf += ruc.markupXml() + '\n'
  xmlBuf += '</usability>'
  outputFile = outputDir + '/usecases.xml'
  f = open(outputFile,'w')
  f.write(xmlBuf)
  f.close()
