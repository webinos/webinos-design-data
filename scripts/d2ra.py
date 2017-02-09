#!/usr/bin/python

# Convert graphviz dot files into CAIRIS associations

import pydot
import os

if __name__ == '__main__':
  
  outputDir = os.environ['TMP_DIR']
  cmDir = os.environ['CM_DIR']
  xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE associations PUBLIC "-//CAIRIS//DTD CAIRIS ASSOCIATIONS 1.0//EN" "http://cairis.org/dtd/associations.dtd">\n\n<associations>\n\n'


  assocSet = set([])
  for fnCat in ['TMS','PS','NM','NC','LC','ID','DA','CAP']:
    dotFile = cmDir + '/' + fnCat + '.dot'
    dotInstance = (pydot.graph_from_dot_file(dotFile))[0]
  
    for e in dotInstance.get_edge_list():
      fromName = e.get_source()
      toName = e.get_destination()
      assocRationale = e.obj_dict['attributes']['label']
      assocSet.add('<manual_association from_name=' + fromName + ' from_dim="requirement" to_name=' + toName + ' to_dim="requirement" label=' + assocRationale + ' />\n')
 
    for subGraph in dotInstance.get_subgraph_list():
      nodeList = subGraph.get_node_list()
      for n in nodeList:
        reqName = n.get_name()
        try:
          ucs = n.obj_dict['attributes']['usecases']
          ucNames = ucs.split(',')
          if ucNames[0] != '""':
            for ucLabel in ucNames:
              ucName = ucLabel.strip().replace('"','')
              assocSet.add('<manual_association from_name=' + reqName + ' from_dim="requirement" to_name="' + ucName + '" to_dim="usecase" />\n')
        except KeyError:
          continue
        try:
          scs = n.obj_dict['attributes']['scenarios']
          scNames = scs.split(',')
          if scNames[0] != '""':
            for scLabel in scNames:
              scName = scLabel.strip().replace('"','')
              assocSet.add('<manual_association from_name=' + reqName + ' from_dim="requirement" to_name="' + scName + '" to_dim="task" />\n')
        except KeyError:
          continue
        try:
          bList = n.obj_dict['attributes']['backlog']
          bNames = bList.split(',')
          if bNames[0] != '""':
            for bLabel in bNames:
              bName = bLabel.strip().replace('"','')
              assocSet.add('<manual_association from_name=' + reqName + ' from_dim="requirement" to_name="' + bName + '" to_dim="document_reference" />\n')
        except KeyError:
          continue
  for xa in assocSet:
    xmlBuf += xa
  xmlBuf += '</associations>'

  outputFileName = outputDir + '/assocs.xml'
  outFile = open(outputFileName,'w')
  outFile.write(xmlBuf)
  outFile.close()
