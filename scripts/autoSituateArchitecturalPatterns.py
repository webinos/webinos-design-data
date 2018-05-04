#!/usr/bin/python

import cairis.core.BorgFactory
from cairis.core.Borg import Borg
import cairis.core.AssetParametersFactory
import sys

if __name__ == '__main__':
  cairis.core.BorgFactory.initialise(sys.argv[1],sys.argv[2])
  b = Borg()
  envName = 'Complete'

  for apName in b.dbProxy.getDimensionNames('component_view'):
    componentAssets = b.dbProxy.componentAssets(apName)
    acDict = {}
    assetParametersList = []
    for assetName,componentName in componentAssets:
      assetParametersList.append(cairis.core.AssetParametersFactory.buildFromTemplate(assetName,[envName]))
      if assetName not in acDict:
        acDict[assetName] = []
      acDict[assetName].append(componentName)
    print 'situating ',apName
    b.dbProxy.situateComponentView(apName,'Complete',acDict,assetParametersList,[],[]) 
  b.dbProxy.conn.commit()
