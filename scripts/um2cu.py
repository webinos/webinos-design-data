#!/usr/bin/python

import os
from xml.sax.handler import ContentHandler
import xml.sax

class JUCMContentHandler(ContentHandler):
  def __init__(self):
    self.theComponents = []

  def startElement(self,name,attrs):
    if (name == 'components'):
      self.theComponents.append(attrs['name'])

  def components(self): return self.theComponents


if __name__ == '__main__':
  ucmDir = os.environ['UC_DIR'] + '/useCaseMaps'
  ucmFiles = os.listdir(ucmDir)
#  ucmFiles = ['DA1.jucm','DA2.jucm','DA3.jucm','DA4.jucm','DA5.jucm','DA5.jucm','DA6.jucm']
  outputDir = '/tmp'
  xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE associations PUBLIC "-//CAIRIS//DTD ASSOCIATIONS 1.0//EN" "http://www.cs.ox.ac.uk/cairis/dtd/associations.dtd">\n\n<associations>\n'
 

  for ucmFile in ucmFiles:
    parser = xml.sax.make_parser()
    handler = JUCMContentHandler()
    parser.setContentHandler(handler)

    fileName = ucmDir + '/' + ucmFile
    parser.parse(fileName)
    components = handler.components()

    ucCode,fileExt = ucmFile.split('.')
    for cName in components:
      xmlBuf += '  <manual_association from_name="' + cName + '" from_dim="component" to_name="' + ucCode + '" to_dim="usecase" />\n'

  xmlBuf += '</associations>\n'

  outputFile = outputDir + '/componentAssociations.xml'
  f = open(outputFile,'w')
  f.write(xmlBuf)
  f.close()
