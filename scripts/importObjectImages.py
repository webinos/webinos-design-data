#!/usr/bin/python

import json
import requests
import jsonpickle
import argparse
from urllib import quote
import sys
import glob
import imghdr


def updateObjectImage(url,dimName,imgDir,objt):
  objtName = objt['theName']
  objtGlob = glob.glob(imgDir + '/' + objtName + '.*')
  if len(objtGlob) == 0:
    return
  elif len(objtGlob) > 1:
    raise Exception('Error uploading image for ' + objtName + ': expecting just 1 file for ' + objtName + ', but found ' + str(objtGlob) + '.')
  imgFile = objtGlob[0]
  if (imghdr.what(imgFile) == None):
    raise Exception('Error uploading ' + imgFile + ': invalid image file.')
  imgResp = requests.post(url + '/api/upload/image?session_id=test',files=dict(file=open(imgFile,'rb')))
  if not imgResp.ok:
    raise Exception('Error uploading ' + imgFile + ' :' + imgResp.text + '.')
  else:
    objt['theImage'] = imgResp.json()['filename']
    objt_json = {'session_id' : 'test','object' : objt}
    hdrs = {'Content-type': 'application/json'}
    objtUpdResp = requests.put(url + '/api/' + dimName + 's/name/' + objtName,data=json.dumps(objt_json),headers=hdrs);
    if not objtUpdResp.ok:
      raise Exception('Error updating ' + objtName + ': ' + objtUpdResp.text + '.')


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Import object images')
  parser.add_argument('--url',dest='url',help='URL for CAIRIS server')
  parser.add_argument('--database',dest='dbName',help='Database name')
  parser.add_argument('--image_dir',dest='imageDir',help='Directory for model images')
  parser.add_argument('--type',dest='dimName',help='Object type (persona or attacker)')
  args = parser.parse_args()

  try:
    if ((args.dimName != 'attacker') and (args.dimName != 'persona')):
      raise Exception('Object type ' + args.dimName + ' not supported.')

    openDbResp = requests.post(args.url + '/api/settings/database/' + quote(args.dbName) + '/open?session_id=test')
    if not openDbResp.ok:
      raise Exception('Fatal error: cannot open database ' + args.dbName + ': ' + openDbResp.text)

    objtResp = requests.get(args.url + "/api/" + args.dimName + "s?session_id=test")
    if not objtResp.ok:
      raise Exception('Fatal error: cannot get ' + args.dimName + 's: ' + objtResp.text + '.')
    else:
      objts = objtResp.json()
      for objtName in objts.keys():
        updateObjectImage(args.url,args.dimName,args.imageDir,objts[objtName])

    reopenDbResp = requests.post(args.url + '/api/settings/database/cairis_default/open?session_id=test')
    if not reopenDbResp.ok:
      raise Exception('Fatal error re-opening default database: ' + reopenDbResp.text)

  except Exception, e:
    print 'Fatal error: ' + str(e)
    sys.exit(-1)
