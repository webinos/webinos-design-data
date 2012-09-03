#!/usr/bin/python

# Convert a Redmine marked-up use case file into a CAIRIS usability model

import os

class RedmineUseCase:
  def __init__(self,inFile):
    self.inDescription = 0
    self.inPostconditions = 0
    self.inPreconditions = 0
    self.inFlow = 0
    self.inUseCaseMap = 0
    self.inRelatedArtifacts = 0
    self.ucCode = inFile.split('.')[0]
    self.origUcCode = ''
    self.ucName = ''
    self.ucAuthors = ''
    self.ucRoles = []
    self.envName = ''
    self.ucDesc = ''
    self.ucPre = ''
    self.ucPost = ''
    self.ucSteps = []
    self.theInputFile = inFile
    self.theInputDir = os.environ['UC_DIR']
    self.process()

  def resetSectionMarkers(self):
    self.inDescription = 0
    self.inPostconditions = 0
    self.inPreconditions = 0
    self.inFlow = 0
    self.inUseCaseMap = 0
    self.inRelatedArtifacts = 0

  def processHeading(self,lineElements):
    if lineElements[0] == 'h1':
      ucNameElements = lineElements[1].split(':')
      self.origUcCode = ucNameElements[0].strip()
      self.ucName = ucNameElements[1].strip()
    else:
      heading = lineElements[1].strip()
      if heading == 'Description':
        self.resetSectionMarkers()
        self.inDescription = 1  
      elif heading == 'Preconditions':
        self.resetSectionMarkers()
        self.inPreconditions = 1  
      elif heading == 'Postconditions':
        self.resetSectionMarkers()
        self.inPostconditions = 1  
      elif heading == 'Flow':
        self.resetSectionMarkers()
        self.inFlow = 1  
      elif heading == 'Use case map' or  heading == 'Use Case Map':
        self.resetSectionMarkers()
        self.inUseCaseMap = 1  
      elif heading == 'Related artifacts':
        self.resetSectionMarkers()
        self.inRelatedArtifacts = 1  

  def processAttribute(self,lineElements):
    attName = lineElements[0].strip()
    if attName == 'Author' or attName == 'Authors':
      self.ucAuthors = lineElements[1].strip()
    if attName == 'Actor' or attName == 'Actors':
      self.ucActors = lineElements[1]
      roleList = self.ucActors.split(',')
      for role in roleList:
        self.ucRoles.append(role.strip())
    if attName == 'Category':
      self.envName = lineElements[1].strip()

  def processBody(self,line):
    if line == '':
      return

    if self.inDescription == 1:
      self.ucDesc += line 
    if self.inPreconditions == 1:
      self.ucPre += line 
    if self.inPostconditions == 1:
      self.ucPost += line 
    if self.inFlow == 1:
      self.ucSteps.append( line.split('#')[1].strip() )

  def markupXml(self):
    originatorPostfix = 'Based on D2.1 use case ' + self.origUcCode + '.'
    if len(self.ucDesc) == 0:
      self.ucDesc = originatorPostfix
    else:
      self.ucDesc += '  ' + originatorPostfix

    xmlBuf = '<usecase name=\"' + self.ucName + '\" author=\"' + self.ucAuthors + '\" code=\"' + self.ucCode + '\">\n  <description>' + self.ucDesc + '</description>\n'
    for r in self.ucRoles:
      xmlBuf += '  <actor name=\"' + r + '\" />\n'

    xmlBuf += '  <usecase_environment name=\"' + self.envName + '\">\n    <preconditions>' + self.ucPre + '</preconditions>\n    <flow>\n'
    stepIdx = 1
    for s in self.ucSteps:
      xmlBuf += '      <step number=\"' + str(stepIdx) + '\" description=\"' + s + '\" />\n'
      stepIdx += 1
    xmlBuf += '    </flow>\n    <postconditions>' + self.ucPost + '</postconditions>\n  </usecase_environment>\n'

    xmlBuf += '  <usecase_environment name=\"Complete\">\n    <preconditions>' + self.ucPre + '</preconditions>\n    <flow>\n'
    stepIdx = 1
    for s in self.ucSteps:
      xmlBuf += '      <step number=\"' + str(stepIdx) + '\" description=\"' + s + '\" />\n'
      stepIdx += 1
    xmlBuf += '    </flow>\n    <postconditions>' + self.ucPost + '</postconditions>\n  </usecase_environment>\n</usecase>\n\n'

    return xmlBuf

  def process(self):
    rf = open(self.theInputDir + '/' + self.theInputFile)
    for l in rf.readlines():
      line = l.strip()
      if line == '' or line[1] == '!' or line[1] == '|':
        continue 
      lineElements = line.split('.')
      if len(lineElements) == 2 and lineElements[0][0] == 'h':
        self.processHeading(lineElements)
      else:
        lineElements = line.split(':')
        if len(lineElements) == 2:
          self.processAttribute(lineElements)
        else:
          self.processBody(line)
