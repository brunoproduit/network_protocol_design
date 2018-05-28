from utils import *

print('Reading in neighbors from ', NEIGHBORSFILE)
neighbors = Utils.read_neighbors_from_neighborfile()
print(neighbors)
print('Finished reading neighbors')

global router
router = Router(source_address, neighbors)
