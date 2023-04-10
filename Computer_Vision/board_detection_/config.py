from time import time
global NC_LAYER, NC_IMAGE, NC_CLOCK, NC_DEBUG, NC_CONFIG
NC_LAYER = 0
NC_IMAGE = object
NC_CLOCK = time()
# NC_DEBUG = False # True
NC_DEBUG = True
NC_CONFIG = {'layers': 3}
print(NC_CONFIG)
# NC_CONFIG = {'layers': 1}
# NC_CONFIG = {'layers': 2}
