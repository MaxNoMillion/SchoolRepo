from queue import Queue


class Graph:

  def __init__(self):
    self.verList = {}
    self.numVertices = 0

  class __Vertex:
    def __init__(self, key):
      self.id = key
      self.connectedTo = {}

    def getId(self):
      return self.id
    
    def getConnections(self):
      return self.connectedTo.keys()

    def getWeight(self, nbr):
      return self.connectedTo[nbr]

    def addNeighbor(self, nbr, weight = 0):
      self.connectedTo[nbr] = weight

    def __str__(self):
      return f"connected to: {str([x.id for x in self.connectedTo])}"


  def addVertex(self, key):
    self.numVertices += 1
    newVertex = Graph.__Vertex(key)
    self.verList[key] = newVertex
    return newVertex

  def getVertex(self, key):
    if key in self.verList:
      return self.verList[key]
    else:
      return None

  def __contains__(self, key):
    return key in self.verList

  def addEdge(self, source, destination, weight = 0):
    if source not in self.verList:
      newVertex = self.addVertex(source)
    if destination not in self.verList:
      newVertex = self.addVertex(destination)
    self.verList[source].addNeighbor(self.verList[destination], weight)

  def getVertices(self):
    return self.verList.keys()

  def __iter__(self):
    return iter(self.verList.values())

  # DFS algorythm
  def dfs(self, s, visited = None):
    if visited is None: # checks if none type
      visited = set()

    if s not in visited:
      print(s, end = " ")
      visited.add(s)
      for next_node in [x.id for x in self.verList[s].connectedTo]:
        self.dfs(next_node, visited)

  # BFS algorythm
  def bfs(self, s, visited = None):
    if visited is None: # checks if none type
      visited = set()

    q = Queue()
    q.put(s)
    visited.add(s)

    while not q.empty():
      current_node = q.get()
      print(current_node, end = " ")

      for next_node in [x.id for x in self.verList[current_node].connectedTo]:
        if next_node not in visited:
          q.put(next_node)
          visited.add(next_node)        


def main():

  graph = Graph()

  for i in range(6):
    graph.addVertex(i)

  graph.addEdge(0, 1, 5)
  graph.addEdge(0, 5, 2)
  graph.addEdge(1, 2, 4)
  graph.addEdge(2, 3, 9)
  graph.addEdge(3, 4, 7)
  graph.addEdge(3, 5, 3)
  graph.addEdge(4, 0, 1)
  graph.addEdge(5, 4, 8)
  graph.addEdge(5, 2, 1)

  # for vertex in graph:
  #   for adjacent in vertex.getConnections():
  #     print(f"({vertex.getId()}, {adjacent.getId()})")
  
  print()

  for k, v in graph.verList.items():
    print(k,v)

  print()
  graph.dfs(5)

  print()
  graph = Graph()

  for i in range(5):
    graph.addVertex(i)

  graph.addEdge(0, 1, 0)
  graph.addEdge(1, 0, 0)

  graph.addEdge(0, 2, 0)
  graph.addEdge(2, 0, 0)

  graph.addEdge(2, 3, 0)
  graph.addEdge(3, 2, 0)

  graph.addEdge(3, 4, 0)
  graph.addEdge(4, 3, 0)

  graph.addEdge(3, 1, 0)
  graph.addEdge(1, 3, 0)

  # for vertex in graph:
  #   for adjacent in vertex.getConnections():
  #     print(f"({vertex.getId()}, {adjacent.getId()})")

  print()

  for k, v in graph.verList.items():
    print(k,v)

  print()

  graph.dfs(3)

  print()

  graph = Graph()

  for i in range(6):
    graph.addVertex(i)

  graph.addEdge(0, 1, 0)
  graph.addEdge(1, 0, 0)
  graph.addEdge(0, 2, 0)
  graph.addEdge(2, 0, 0)
  graph.addEdge(0, 3, 0)
  graph.addEdge(3, 0, 0)
  graph.addEdge(0, 4, 0)
  graph.addEdge(4, 0, 0)
  graph.addEdge(1, 2, 0)
  graph.addEdge(2, 1, 0)
  graph.addEdge(2, 3, 0)
  graph.addEdge(3, 2, 0)
  graph.addEdge(2, 5, 0)
  graph.addEdge(5, 2, 0)
  graph.addEdge(3, 4, 0)
  graph.addEdge(4, 3, 0)
  graph.addEdge(3, 5, 0)
  graph.addEdge(5, 3, 0)
  graph.addEdge(4, 5, 0)
  graph.addEdge(5, 4, 0)

  print()

  for k, v in graph.verList.items():
    print(k,v)

  print()

  graph.bfs(3)


main()
  


