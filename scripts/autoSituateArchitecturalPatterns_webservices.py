#!/usr/bin/python

import json
import requests
import jsonpickle
import argparse
from urllib import quote
import sys

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Automatically situate all architectural patterna')
  parser.add_argument('--url',dest='url',help='URL for CAIRIS server')
  parser.add_argument('--database',dest='dbName',help='Database name')
  parser.add_argument('--environment',dest='envName',help='Environment name')
  args = parser.parse_args()

  openDbResp = requests.post(args.url + '/api/settings/database/' + quote(args.dbName) + '/open?session_id=test')
  if not openDbResp.ok:
    exceptionTxt = 'Fatal error: cannot open database ' + args.dbName + ': ' + openDbResp.text
    raise Exception(exceptionTxt)


  apResp = requests.get(args.url + "/api/dimensions/table/component_view?session_id=test")
  if not apResp.ok:
    print 'Fatal error: cannot get architectural pattern names: ' + apRest.text + '.'
  else:
    for apName in apResp.json():
      sitResp = requests.post(args.url + "/api/architectural_patterns/name/" + quote(apName) + "/environment/" + args.envName + "/situate?session_id=test")
      if not sitResp.ok:
        print 'Fatal error: cannot situate architectural pattern ' + apName + ': ' + sitResp.text + '.'
  reopenDbResp = requests.post(args.url + '/api/settings/database/cairis_default/open?session_id=test')
  if not reopenDbResp.ok:
    exceptionTxt = 'Fatal error re-opening default database: ' + reopenDbResp.text
    raise Exception(exceptionTxt)
