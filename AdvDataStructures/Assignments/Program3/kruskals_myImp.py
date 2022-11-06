import sys
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

    def getVertex(self, n):
        if n in self.verList:
            return self.verList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.verList

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

    def dfs(self, s, visited = None):
        if visited is None:
            visited = set()

        if s not in visited:
            print(s, end = " ")
            visited.add(s)
            for next_node in [x.id for x in self.verList[s].connectedTo]:
                self.dfs(next_node, visited)        

    def bfs(self, s, visited = None):
        if visited is None:
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

    def kruskals(self):
        vertices_sets = set()
        edges_dict = dict()
        MST = set()

        for vert in self.getVertices():
            vertices_sets.add(frozenset({vert}))
            for nbr in self.getVertex(vert).getConnections():
                if (nbr.getId(), vert) not in edges_dict.keys():
                    edges_dict[(vert, nbr.getId())] = self.getVertex(vert).getWeight(nbr)

        edges_dict = sorted(edges_dict.items(), key = lambda x: x[1])   # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

        for edge in edges_dict:
            for item in vertices_sets:
                if edge[0][0] in list(item):
                    U = item
                if edge[0][1] in list(item):
                    V = item
            if U != V:
                MST.add((edge[0], edge[1]))
                S = U.union(V)
                vertices_sets.remove(U)
                vertices_sets.remove(V)
                vertices_sets.add(S)

        return MST

def main():
    
    # create an empty graph
    graph = Graph()

    # get graph vertices & edges from input file and add them to the graph

    file = "0 1 5\n0 5 2\n1 2 4\n2 3 9\n3 4 7\n3 5 3\n4 0 1\n5 4 8\n5 2 1\n"

    line = []
    for char in file:
        if char != "\n":
            if char != " ":
                line.append(char)
        else:
            graph.addEdge(int(line[0]), int(line[1]), int(line[2]))
            graph.addEdge(int(line[1]), int(line[0]), int(line[2]))
            line = []
    

    # file = open(sys.argv[1], "r")
    # for line in file:
    #     values = line.split()
    #     graph.addEdge(int(values[0]), int(values[1]), int(values[2]))
    #     graph.addEdge(int(values[1]), int(values[0]), int(values[2])) 

    # print adjacency list representation of the graph
    print()

    print("Graph adjacency list:")
    for vert in graph.getVertices():
        print(f"{vert} {graph.getVertex(vert)}")
    
    # create graph MST
    MST = graph.kruskals()
    # print graph MST
    print()    
    print("Graph MST:")
    print("Edge\t\tWeight")
    for edge in MST:
        print(f"{edge[0]}\t\t{edge[1]}")

main() 
    
    
