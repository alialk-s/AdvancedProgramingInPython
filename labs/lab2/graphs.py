import graphviz

class Graph:

    def __init__(self, edgelist=None):
        self._adjacencylist = {}
        self._valuelist = {}
        if edgelist is not None:
            for (a, b) in edgelist:
                self.add_edge(a, b)
            self._valuelist = dict.fromkeys(self._adjacencylist, 0)

    def __len__(self):
        return len(self._adjacencylist)

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

    def add_vertex(self, vertex):
        if vertex not in self._adjacencylist:
            self._adjacencylist[vertex] = []
            self.set_vertex_value(vertex, 0)

    def add_edge(self, a, b):
        edges = self.edges()
        if (a, b) not in edges and (b, a) not in edges:
            self.add_vertex(a)
            self.add_vertex(b)
            self._adjacencylist[a].append(b)
            self._adjacencylist[b].append(a)

    def remove_vertex(self, vertex):
        if vertex in self.vertices():
            self._adjacencylist.pop(vertex)
            # remove all edges connected with this vertex as well
            for v in self._adjacencylist:
                if vertex in self._adjacencylist[v]:
                    list(self._adjacencylist[v]).remove(vertex)

    def remove_edge(self, a, b):
        list(self._adjacencylist[a]).remove(b)
        list(self._adjacencylist[b]).remove(a)

    def get_vertex_value(self, vertex):
        return self._valuelist[vertex]

    def set_vertex_value(self, vertex, value):
        self._valuelist[vertex] = value


class WeightedGraph(Graph):

    def __init__(self, start=None):
        super(WeightedGraph, self).__init__(start)
        self._weightlist = {}

    def get_weight(self, a, b):
        if (a, b) in self._weightlist:
            return self._weightlist[(a, b)]
        if (b, a) in self._weightlist:
            return self._weightlist[(b, a)]

    def set_weight(self, a, b, weight):
        if (a, b) in self._weightlist:
            self._weightlist[(a, b)] = weight
        if (b, a) in self._weightlist:
            self._weightlist[(b, a)] = weight


def dijkstra(graph, source, cost=lambda u,v: 1):
    paths = {}
    unvisited_nodes = [v for v in graph.vertices()]
    dist = {v: float('inf') for v in graph.vertices()}
    prev = {v: None for v in graph.vertices()}
    dist[source] = 0

    while unvisited_nodes:
        current_node = None
        for node in unvisited_nodes:
            if current_node == None or dist[node] < dist[current_node]:
                current_node = node

        # The code block below retrieves the current node's neighbors and updates their distances
        for neighbor in graph.neighbors(current_node):
            new_cost = dist[current_node] + cost(current_node, neighbor)
            if new_cost < dist[neighbor]:
                # update the cost of this neighbor
                dist[neighbor] = new_cost
                # update the prev dict to the current node
                prev[neighbor] = current_node
        # mark this node as visited
        unvisited_nodes.remove(current_node)

    return dist


def visualize(graph, view='dot', name='tramGraph', nodecolors=None):
    g = graphviz.Graph(name, filename=name, format='png', engine=view )

    for v in graph.vertices():
        if nodecolors != None and str(v) in nodecolors:
            g.node(str(v),style='filled', color='orange')
        else:
            g.node(str(v))

    for v in graph.edges():
        g.edge(str(v[0]),str(v[1]))
    g.render(view=True)


