#!/usr/bin/python

import cairis.core.BorgFactory
from cairis.core.Borg import Borg
from cairis.core.AssetParametersFactory import AssetParametersFactory

if __name__ == '__main__':
  cairis.core.BorgFactory.initialise()
  b = Borg()
  envName = 'Complete'

  for apName in b.dbProxy.getDimensionNames('component_view'):
    componentAssets = b.dbProxy.componentAssets(apName)
    acDict = {}
    assetParametersList = []
    for assetName,componentName in componentAssets:
      assetParametersList.append(AssetParametersFactory.buildFromTemplate(assetName,[envName]))
      if assetName not in acDict:
        acDict[assetName] = []
      acDict[assetName].append(componentName)
    print 'situating ',apName
    b.dbProxy.situateComponentView(apName,'Complete',acDict,assetParametersList,[],[]) 
  b.dbProxy.conn.commit()
