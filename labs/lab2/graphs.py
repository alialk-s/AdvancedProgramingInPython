class Graph:

    def __init__(self, edgelist=None):
        self._adjacencylist = {}
        self._valuelist = {}
        if edgelist is not None:
            for (a, b) in edgelist:
                self.add_edge(a, b)
            self._valuelist = dict.fromkeys(self._adjacencylist, 0)


    def neighbors(self, vertex):
        return self._adjacencylist[vertex]

    def vertices(self):
        return [v for v in self._adjacencylist]

    def edges(self):
        edges = []
        for key in self._adjacencylist:
            for vertex in self._adjacencylist[key]:
                if (vertex, key) not in edges:
                    edges.append((key, vertex))
        return edges

    def __len__(self):
        return len(self._adjacencylist)

    def add_vertex(self, vertex):
        if vertex not in self._adjacencylist:
            self._adjacencylist[vertex] = []
            self._valuelist[vertex] = 0

    def add_edge(self, vertex1, vertex2):
        edges = self.edges()
        if (vertex1, vertex2) not in edges and (vertex2, vertex1) not in edges:
            if vertex1 not in self._adjacencylist:
                self._adjacencylist[vertex1] = []  # create a list (value) for this vertex (key) if not exists
            if vertex2 not in self._adjacencylist:
                self._adjacencylist[vertex2] = []  # create a list (value) for this vertex (key) if not exists
            self._adjacencylist[vertex1].append(vertex2)
            self._adjacencylist[vertex2].append(vertex1)

    def remove_vertex(self, vertex):
        if vertex in self.vertices():
            self._adjacencylist.pop(vertex)
            # remove all edges with this vertex as well
            for v in self._adjacencylist:
                if vertex in self._adjacencylist[v]:
                    list(self._adjacencylist[v]).remove(vertex)

    def remove_edge(self, vertex1, vertex2):
        if (vertex1, vertex2) in self.edges():
            list(self._adjacencylist[vertex1]).remove(vertex2)
        if (vertex2, vertex1) in self.edges():
            list(self._adjacencylist[vertex2]).remove(vertex1)

    def get_vertex_value(self, vertex):
        return self._valuelist[vertex]

    def set_vertex_value(self, vertex, value):
        self._valuelist[vertex] = value


class WeightedGraph(Graph):

    def __init__(self, start=None):
        super().__init__(start)
        self._weightlist = {}

    def get_weight(self, vertex1, vertex2):
        if (vertex1, vertex2) in self._weightlist:
            return self._weightlist[(vertex1, vertex2)]
        if (vertex2, vertex1) in self._weightlist:
            return self._weightlist[(vertex2, vertex1)]

    def set_weight(self, vertex1, vertex2, weight):
        if (vertex1, vertex2) in self._weightlist:
            self._weightlist[(vertex1, vertex2)] = weight
        if (vertex2, vertex1) in self._weightlist:
            self._weightlist[(vertex2, vertex1)] = weight
