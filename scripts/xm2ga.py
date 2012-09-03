#!/usr/bin/python

# Converts XLS  obstacle mitigation sheets to a cairis model of domain properties and goal associations

import os
from DocumentConverter import *
import csv

csvFiles = ['attackPatternMitigation.csv']

def removeTempFiles():
  for fileName in csvFiles:
    try:
      os.unlink(fileName)
    except OSError:
      pass
  print 'temp files removed'

if __name__ == "__main__":
 
  outputDir = os.environ['TMP_DIR']
  archDir = os.environ['ARCHITECTURE_DIR']

  removeTempFiles()
  try: 
    converter = DocumentConverter()
    apMitFile = 'attackPatternMitigations.xls'
    csvFile = apMitFile.split('.')[0] + '.csv'
    converter.convert(archDir + '/' + apMitFile,outputDir + '/' + csvFile)

    xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE cairis_model PUBLIC "-//University of Oxford//DTD MODEL 1.0//EN" "http://www.cs.ox.ac.uk/cairis/dtd/cairis_model.dtd">\n\n<cairis_model>\n\n'

    dpBuf = ''
    gaBuf = ''
    aaBuf = '|_.Obstacle|_.Mitigating Requirement Name|_.Mitigating Requirement Definition|_.Affected Components|_.Satisfied (Y/N)|_.Rationale|\n'

    print 'Converting ' + csvFile
    r = csv.reader(open(outputDir + '/' + csvFile,'rU'))
    r.next() # skip the headers
    reqLabel = 1
    for cells in r:
      obsNames = cells[0]
      gdpName = cells[1]
      gdpDef = cells[2]
      cNames = cells[3]
      isSatisfied = cells[4]
      dpDef = cells[5]
  

      if isSatisfied == 'N':
        dpBuf += '<domainproperty name=\"' + gdpName + '\" type="Invariant" originator="WP 3 workshop - August 2012">\n  <definition>' + dpDef + '</definition>\n</domainproperty>\n'

      for obsName in obsNames.split('#'):
        gaBuf += '<goal_association environment="Complete" goal_name=\"' + obsName + '\" goal_dim="obstacle" ref_type="resolve" subgoal_name=\"' + gdpName + '\" subgoal_dim=\"'
        if isSatisfied == 'Y':
          gaBuf += 'goal'
        else:
          gaBuf += 'domainproperty'
        gaBuf += '\" alternative_id="0">\n  <rationale>' + dpDef + '</rationale>\n</goal_association>\n'
        aaBuf += '| ' + obsName + ' | ' + gdpName + ' | ' + gdpDef + ' | ' + cNames + ' | ' + isSatisfied + ' | ' + dpDef + ' |\n'


    if len(dpBuf) > 0:
      xmlBuf += '<goals>\n' + dpBuf + '</goals>\n\n'
    if len(gaBuf) > 0:
      xmlBuf += '<associations>\n' + gaBuf + '</associations>\n\n'
    xmlBuf += '</cairis_model>'

    outputFile = outputDir + '/pattern_mitigation.xml'
    f = open(outputFile,'w')
    f.write(xmlBuf)
    f.close() 

    aaFile = outputDir + '/ambiguityAnalysis.txt'
    f = open(aaFile,'w')
    f.write(aaBuf)
    f.close() 

    print 'Exported pattern mitigation details to XML'
  except DocumentConversionException, e:
    print 'Error: ' + str(e)
    exit(-1)
  except ErrorCodeIOException, e:
    print 'ErrorCodeIOException: ' + str(exception.ErrCode)
    exit(-1)
