# Router class, used for abstracting the routing functions.
# Acts as an API to convert md5hashes to ipv4-addresses
class Router:

    # Constructor for the Router class
    # @param: src string (md5hash)
    # @param: neighbors list of tuples (string (md5hash), string (ipv4-address))
    def __init__(self, src, neighbors):
        self.neighbors = neighbors
        self.graph = Graph(src, [(src, i[0], 1) for i in neighbors], [i[0] for i in neighbors])
        bf = self.graph.bellman_ford()
        self.table = bf[0]
        self.prev_hops = bf[1]

    # Is called to update the routing table
    # @param: sender tuple (sting (md5hash), string(ipv4-address))
    # @param: table list of tuples (string (md5hash), string (ipv4-address), boolean (withdraw), int (distance))
    # @return: None (only if the update would break the routing table)
    def update(self, sender, table):
        if sender not in self.neighbors:
            self.neighbors.append(sender)
            self.graph.insert_edge((self.graph.src, sender[0], 1))

        if sender[0] not in self.graph.vertices:
            self.graph.insert_vertice(sender[0])

        for i in table:
            if i[2]:
                self.graph.remove_vertice(i[0])
            else:
                self.graph.insert_edge((sender[0], i[0], i[3] + 1))
                if i[0] not in self.graph.vertices:
                    self.graph.insert_vertice(i[0])

        bf = self.graph.bellman_ford()

        # Check if update would break the graph
        if bf != 0:
            self.table = bf[0]
            self.prev_hops = bf[1]
        else:
            return None

    # Takes the md5 hash of the destination
    # @param: dest_md5 string
    # @return: None (only if dest_md5 is not in the routing table)
    # @return: tuple (string (md5hash), string (ipv4-address))
    def get_next_hop(self, dest_md5):
        if dest_md5 not in self.prev_hops:
            return None

        # Traverses the prev_hops from bellman_ford backwards from dest to src, returns ipv4 from self.neighbors
        prev_step = dest_md5
        while True:
            next_step = self.prev_hops[prev_step]
            if next_step == self.graph.src:
                # Next hop should be a neighbor
                for row in self.neighbors:
                    if row[0] == prev_step:
                        return row
            prev_step = next_step


# Graph class which represents the acyclic graph used to calculate bellman-ford
class Graph:
    def __init__(self, src, edges=[], vertices=[]):
        self.src = src
        self.edges = edges
        self.vertices = vertices

    # Adds a md5 hash identifier to the list of vertices in the graph
    # @param: vertice string (md5_hash)
    def insert_vertice(self, vertice):
        self.vertices.append(vertice)

    # Adds a connection between two vertices to the list of edges in the graph
    # @param: edge tuple (string (src_md5), string (dest_md5), int (weight))
    def insert_edge(self, edge):
        # Updates weight if edge exists, if not then appends the edge to edges
        if edge not in self.edges:
            for e in self.edges:
                if e[0] == edge[0] and e[1] == edge[1]:
                    e[2] = edge[2]
                    return
            self.edges.append(edge)

    # Removes a vertice from the list of vertices in the graph
    # @param: vertice string (src_md5)
    def remove_vertice(self, vertice):
        if vertice in self.vertices:
            self.vertices.remove(vertice)
        # Remove all edges connected to the deleted vertex
        for edge in self.edges:
            if edge[0] == vertice or edge[1] == vertice:
                self.remove_edge(edge)

    # Removes a connection between two vertices from the list of edges in the graph
    # @param: edge tuple (string (src_md5), string (dest_md5), int (weight))
    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    # Calculates the distances and gives the path to all vertices
    # @return: hops dict (string (md5_hash): int (hop-count))
    # @return: prev_hop dict (string (to_md5): string (from_md5))
    def bellman_ford(self):
        hops = {}
        prev_hop = {}

        for i in self.vertices:
            hops[i] = float("Inf")
            prev_hop[i] = None

        hops[self.src] = 0

        for i in range(0, len(self.vertices) - 1):
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


def testCase():
    # Test
    rt = Router("myhash", [("n1", "1.1.1.1"), ("n2", "2.2.2.2")])

    # update from neighbor
    rt.update(("n1", "1.1.1.1"), [("n3", "3.3.3.3", False, 1), ("n4", "4.4.4.4", False, 2)])
    # update from non-neighbor
    rt.update(("n5", "5.5.5.5"), [("n6", "6.6.6.6", False, 1)])

    # test nexthops for neighbors
    assert rt.get_next_hop("n5") == ("n5", "5.5.5.5")
    assert rt.get_next_hop("n1") == ("n1", "1.1.1.1")

    # test nexthop for non-neighbors
    assert rt.get_next_hop("n3") == ("n1", "1.1.1.1")

# testCase()
