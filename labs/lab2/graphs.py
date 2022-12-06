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
                    self._adjacencylist[v].remove(vertex)

    def remove_edge(self, a, b):
        if (a, b) in self.edges() or (b, a) in self.edges():
            self._adjacencylist[a].remove(b)
            self._adjacencylist[b].remove(a)

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
    # the returning dict
    paths = {}
    # initially, all nodes in the graph
    unvisited_nodes = [v for v in graph.vertices()]
    # every node and its shortest path previous node
    prev_nodes = {v: None for v in graph.vertices()}
    # every node and its cost to the source, initially all costs are infinity
    dist = {v: float('inf') for v in graph.vertices()}
    # however, cost from source to source is zero
    dist[source] = 0

    while unvisited_nodes:
        current_node = None
        for node in unvisited_nodes:
            if current_node == None or dist[node] < dist[current_node]:
                current_node = node

        for neighbor in graph.neighbors(current_node):
            new_cost = dist[current_node] + cost(current_node, neighbor)
            if new_cost < dist[neighbor]:
                # update the cost of this neighbor
                dist[neighbor] = new_cost
                # update the prev_nodes dict to the current node
                prev_nodes[neighbor] = current_node
        # mark this node as visited
        unvisited_nodes.remove(current_node)

    for v in graph.vertices():
        dist_node = v
        path = []
        while dist_node != source:
            # add the dest. node
            path.append(dist_node)
            # update the dest.node
            dist_node = prev_nodes[dist_node]
        # finally, add the source to the path
        path.append(source)
        # store the shortest path from source to node v in paths (we have to reverse the path first!)
        paths[v] = list(reversed(path))

    return paths


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


def view_shortest(G, source, target, cost=lambda u, v: 1):
    path = dijkstra(G, source, cost)[target]
    print(path)
    colormap = {str(v): 'orange' for v in path}
    print(colormap)
    visualize(G, view='view', nodecolors=colormap)


def demo():
    G = Graph([(1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (3, 6), (3, 7), (6, 7)])
    view_shortest(G, 2, 6)

if __name__ == '__main__':
    demo()


