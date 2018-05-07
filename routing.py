# Router class, used for abstracting the routing functions.
# Acts as an API to convert md5hashes to ipv4-addresses
class Router:

    # Constructor for the Router class
    # src is a md5hash
    # neighbors is a list of tuple (md5hash, ipv4-address) 
    def __init__(self, src, neighbors):
        self.neighbors = neighbors
        self.graph = Graph(src, [(src, i[0], 1) for i in neighbors], [i[0] for i in neighbors])        
        self.table = self.graph.bellman_ford()[0]
        
    # Is called to update the routing table
    # table: list of tuple(md5hash, ipv4-address, withdraw, distance)
    # returns None 
    def update(sender, table):
        for i in table:
            if i[2]:
                self.graph.remove_vertice(i[0])
            else:
                self.graph.insert_edge(sender, i[0], i[3])
        self.table = self.graph.bellman_ford()[0]

    # Returns the md5hash of the next hop
    def get_next_hop(md5hash):
        if md5hash in neighbors:
            return md5hash
        else:
            
            return None


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
        # TODO check if weight changed
        if edge not in self.edges:
            self.edges.append(edge)

    def remove_vertice(self, vertice):
        if vertice in self.vertices:
            self.vertices.remove(vertice)
        # TODO remove all edges from this vertice 

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
    
    # TODO if cycle or negative
    def bellman_ford(self):
        hops = {}
        prev_hop = {}

        for i in self.vertices:
            hops[i] = float("Inf")
            prev_hop[i] = None

        hops[self.src] = 0
        
        for i in range (1, len(self.vertices)-1):
            for u, v, w in self.edges:
                if hops[u] + w < hops[v]:
                    hops[v] = hops[u] + w
                    prev_hop[v] = u
        
        for u, v, w in self.edges:
            if hops[u] + w <  hops[v]:
                return 0
        
        return hops, prev_hop

r = Router("test", [("w",0),("e",2),("q",1)])

print (r.graph.bellman_ford(), r.neighbors)
