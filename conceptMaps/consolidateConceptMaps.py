##!/usr/bin/python
#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

import pydot

if __name__ == '__main__':
  subGraphs = []
  edges = []

  for fnCat in ['TMS','PS','NM','NC','LC','ID','DA','CAP']:
    fileName = fnCat + '.dot'
    dotInstance = pydot.graph_from_dot_file(fileName)
    subGraphs += dotInstance.get_subgraph_list()
    edges += dotInstance.get_edge_list()

  dotTxt = 'digraph webinosTraceability {\n  graph [rankdir=\"LR\"];\n  node [shape=rectangle,style=\"rounded,filled\",colorscheme=\"spectral3\",color=\"1\"];\n  edge [arrowhead=vee];\n\n'

  for sg in subGraphs:
    dotTxt += sg.to_string() + '\n\n'
  for e in edges: 
    dotTxt += e.to_string() + '\n'

  dotTxt += '}'
  f = open('consolidated.dot','w')
  f.write(dotTxt)
  f.close()
