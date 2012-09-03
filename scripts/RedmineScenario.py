#!/usr/bin/python

# Convert a Redmine marked-up scenario file into a CAIRIS usability model

import os

class RedmineScenario:
  def __init__(self,inFile):
    self.inOverview = 0
    self.inDescription = 0
    self.inIssues = 0
    self.inBenefits = 0
    self.inFlow = 0
    self.inUsabilityBreakdown = 0
    self.inRequiredUseCases = 0
    self.envName = ''
    self.scCode = ''
    self.scName = ''
    self.scOverview = ''
    self.scAuthors = ''
    self.scDescription = ''
    self.scIssues = ''
    self.scBenefits = ''
    self.usBreakdown = ''
    self.theCurrentPersona = ''
    self.theCurrentDuration = ''
    self.theCurrentFrequency = ''
    self.theCurrentDemands = ''
    self.scUcs = []
    self.breakdownList = []
    self.theInputFile = inFile
    self.theInputDir = os.environ['SC_DIR']
    self.process()

  def resetSectionMarkers(self):
    self.inOverview = 0
    self.inDescription = 0
    self.inIssues = 0
    self.inBenefits = 0
    self.inFlow = 0
    self.inUsabilityBreakdown = 0
    self.inRequiredUseCases = 0

  def processBreakdownTableLine(self,line):
    lineElements = line.split('|')
    attributeName = lineElements[1].strip()
    attributeValue = lineElements[2].strip()
    if (attributeName == 'Persona'):
      self.theCurrentPersona = attributeValue
    elif (attributeName == 'Duration'):
      self.theCurrentDuration = attributeValue.replace(' ','_')
    elif (attributeName == 'Frequency'):
      self.theCurrentFrequency = attributeValue.replace(' ','_')
    elif (attributeName == 'Demands'):
      self.theCurrentDemands = attributeValue
    elif (attributeName == 'Goal Conflict'):
      self.breakdownList.append((self.theCurrentPersona,self.theCurrentDuration,self.theCurrentFrequency,self.theCurrentDemands,attributeValue))
      self.theCurrentPersona = self.theCurrentDuration = self.theCurrentFrequency = self.theCurrentDemands = ''

  def processHeading(self,lineElements):
    if lineElements[0] == 'h1':
      scNameElements = lineElements[1].split(':')
      self.scCode = scNameElements[0].strip()
      self.scName = scNameElements[1].strip()
    else:
      heading = lineElements[1].strip()
      if heading == 'Overview':
        self.resetSectionMarkers()
        self.inOverview = 1  
      elif heading == 'Description':
        self.resetSectionMarkers()
        self.inDescription = 1  
      elif heading == 'Issues':
        self.resetSectionMarkers()
        self.inIssues = 1  
      elif heading == 'Benefits':
        self.resetSectionMarkers()
        self.inBenefits = 1  
      elif heading == 'Usability breakdown':
        self.resetSectionMarkers()
        self.inUsabilityBreakdown = 1  
      elif heading == 'Required Use Cases':
        self.resetSectionMarkers()
        self.inRequiredUseCases = 1  

  def processAttribute(self,lineElements):
    attName = lineElements[0].strip()
    if attName == 'Author' or attName == 'Authors':
      self.scAuthors = lineElements[1].strip()

  def processBody(self,line):
    if (self.inDescription == 1 or self.inIssues == 1 or self.inBenefits == 1) and len(line) > 0 and (line[len(line) -1] == '\n'):
      line += '\n'
    if self.inOverview == 1:
      self.scOverview += line 
    elif self.inDescription == 1:
      self.scDescription += line 
    elif self.inIssues == 1:
      self.scIssues += line 
    elif self.inBenefits == 1:
      self.scBenefits += line 
    elif self.inUsabilityBreakdown == 1:
      self.processBreakdownTableLine(line)
    elif self.inRequiredUseCases == 1:
      self.scUcs.append( line.split('*')[1].strip() )

      

  def markupXml(self):
    xmlBuf = '<task name=\"' + self.scName + '\" author=\"' + self.scAuthors + '\" code=\"' + self.scCode + '\" assumption_task=\"FALSE\">\n  <objective>' + self.scOverview + '</objective>\n'

    xmlBuf += '  <task_environment name=\"' + self.envName + '\">\n    <dependencies>None</dependencies>\n'
    for ub in self.breakdownList:
      xmlBuf += '    <task_persona persona=\"' + ub[0] + '\" duration=\"' + ub[1] + '\" frequency=\"' + ub[2] + '\" demands=\"' + ub[3] + '\" goal_conflict=\"' + ub[4] + '\" />\n'
    xmlBuf += '    <narrative>' + self.scDescription + '</narrative>\n    <consequences>' + self.scIssues + '</consequences>\n    <benefits>' + self.scBenefits + '</benefits>\n  </task_environment>\n'

    xmlBuf += '  <task_environment name=\"Complete\">\n    <dependencies>None</dependencies>\n'
    for ub in self.breakdownList:
      xmlBuf += '    <task_persona persona=\"' + ub[0] + '\" duration=\"' + ub[1] + '\" frequency=\"' + ub[2] + '\" demands=\"' + ub[3] + '\" goal_conflict=\"' + ub[4] + '\" />\n'
    xmlBuf += '    <narrative>' + self.scDescription + '</narrative>\n    <consequences>' + self.scIssues + '</consequences>\n    <benefits>' + self.scBenefits + '</benefits>\n  </task_environment>\n</task>\n'

    return xmlBuf

  def markupTraceability(self):
    xmlBuf = ''
    for ucName in self.scUcs:
      xmlBuf += '<manual_association from_name=\"' + ucName + '\" from_dim=\"usecase\" to_name=\"' + self.scName + '\" to_dim=\"task\" />\n'
    return xmlBuf


  def process(self):
    rf = open(self.theInputDir + '/' + self.theInputFile)
    for l in rf.readlines():
      if len(l) > 0 and l[len(l) -1] != '\n':
        l.rstrip()
      line = l.lstrip()
      if line == '':
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
