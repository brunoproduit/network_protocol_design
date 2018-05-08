# Router class, used for abstracting the routing functions.
# Acts as an API to convert md5hashes to ipv4-addresses
class Router:

    # Constructor for the Router class
    # src is a md5hash
    # neighbors is a list of tuple (md5hash, ipv4-address)
    def __init__(self, src, neighbors):
        self.neighbors = neighbors
        self.graph = Graph(src, [(src, i[0], 1) for i in neighbors], [i[0] for i in neighbors])
        bf = self.graph.bellman_ford()
        self.table = bf[0]
        self.prev_hops = bf[1]


    # Is called to update the routing table
    # table: list of tuple(md5hash, ipv4-address, withdraw, distance)
    # returns None
    def update(self, sender, table):
        for i in table:
            if i[2]:
                self.graph.remove_vertice(i[0])
            else:
                self.graph.insert_edge(sender, i[0], i[3])

        self.table = self.graph.bellman_ford()[0]

    # Returns ipv4 of the next node in the route to dest
    # returns None if dest is not in the list of vertices
    def get_next_hop(self, dest_md5):
        if dest_md5 not in self.prev_hops:
            return None

        # Traverses the prev_hops from bellman_ford backwards from dest to src, returns ipv4 from self.table
        prev_step = dest_md5
        while True:
            next_step = self.prev_hops[prev_step]
            if next_step == self.graph.src:
                for row in self.table:
                    if row[0] == prev_step:
                        return row[1]
            prev_step = next_step



# Graph class which represents the acyclic graph used to calculate bellman-ford
class Graph:
    def __init__(self, src, edges=[], vertices=[]):
        self.src = src
        self.edges = edges
        self.vertices = vertices

    def insert_vertice(self, vertice):
        self.vertices.append(vertice)

    # tuple (src, dst, weight)
    def insert_edge(self, edge):
        # Updates weight if edge exists, if not then appends the edge to edges
        if edge not in self.edges:
            for e in self.edges:
                if e[0] == edge[0] and e[1] == edge[1]:
                    e[2] = edge[2]
                    return
            self.edges.append(edge)

    def remove_vertice(self, vertex):
        if vertex in self.vertices:
            self.vertices.remove(vertex)
        # Remove all edges connected to the deleted vertex
        for edge in self.edges:
            if edge[0] == vertex or edge[1] == vertex:
                self.remove_edge(edge)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def bellman_ford(self):
        hops = {}
        prev_hop = {}

        for i in self.vertices:
            hops[i] = float("Inf")
            prev_hop[i] = None

        hops[self.src] = 0

        for i in range(1, len(self.vertices)-1):
            for u, v, w in self.edges:
                if hops[u] + w < hops[v]:
                    hops[v] = hops[u] + w
                    prev_hop[v] = u


        # Returns 0 if Graph contains a negative-weight cycle
        # (Shouldn't happen as the weights are hop-counts -- always positive)
        for u, v, w in self.edges:
            if hops[u] + w < hops[v]:
                return 0

        return hops, prev_hop

r = Router("test", [("w",0),("e",2),("q",1)])

print (r.table, r.neighbors, r.graph)
