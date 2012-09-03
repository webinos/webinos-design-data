#!/usr/bin/python

# Converts XLS sheets to .csv using pyodtcoverter

import os
from DocumentConverter import *
import csv

csvFiles = ['TMS.csv','PS.csv','NM.csv','NC.csv','LC.csv','ID.csv','DA.csv','CAP.csv']

def removeTempFiles():
  for fileName in csvFiles:
    try:
      os.unlink(fileName)
    except OSError:
      pass
  print 'temp files removed'

if __name__ == "__main__":
 
  outputDir = os.environ['TMP_DIR']
  reqDir = os.environ['REQ_DIR']

  removeTempFiles()
  try: 
    converter = DocumentConverter()
    print 'converting spreadsheets to CSV' 
    for fileName in ['TMS.xls','PS.xlsx','NM.xlsx','NC.xlsx','LC.xlsx','ID.xlsx','DA.xls','CAP.xlsx']:
      tmpFile = fileName.split('.')[0] + '.csv'
      converter.convert(reqDir + '/' + fileName,outputDir + '/' + tmpFile)
      print 'Created ' + tmpFile

    xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE goals PUBLIC "-//University of Oxford//DTD GOALS USABILITY 1.0//EN" "http://www.cs.ox.ac.uk/cairis/dtd/goals.dtd">\n\n<goals>\n\n'

    priorityLookup = {}
    priorityLookup['Low'] = '3'
    priorityLookup['Medium'] = '2'
    priorityLookup['High'] = '1'

    for csvFile in csvFiles:
      print 'Converting ' + csvFile
      r = csv.reader(open(outputDir + '/' + csvFile,'rU'))
      r.next() # skip the headers
      reqLabel = 1
      for cells in r:
        reqName = cells[0]
        originator = cells[1]
        envName = cells[2]
        reqPri = priorityLookup[cells[3]]
        reqDesc = cells[4]
        reqFC = cells[5]
        reqComments = cells[6]  
        xmlBuf += '<requirement name=\"' + reqName + '\" reference=\"' + envName + '\" reference_type=\"environment\" label=\"' + str(reqLabel) + '\" type=\"Functional\" priority=\"' + reqPri + '\">\n  <description>' + reqDesc + '</description>\n  <rationale>' + reqComments + '</rationale>\n  <fit_criterion>' + reqFC + '</fit_criterion>\n  <originator>' + originator + '</originator>\n</requirement>\n'
        reqLabel += 1
    xmlBuf += '</goals>'

    outputFile = outputDir + '/requirements.xml'
    f = open(outputFile,'w')
    f.write(xmlBuf)
    f.close() 

    print 'Exported requirements to XML'
  except DocumentConversionException, e:
    print 'Error: ' + str(e)
    exit(-1)
  except ErrorCodeIOException, e:
    print 'ErrorCodeIOException: ' + str(exception.ErrCode)
    exit(-1)
