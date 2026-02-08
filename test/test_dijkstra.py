import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.dijkstra import dijkstra

dijkstra(sys.argv[1], sys.argv[2])
