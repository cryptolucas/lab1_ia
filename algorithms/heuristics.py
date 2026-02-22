import math
from typing import Any, Tuple
from algorithms import utils
from algorithms.problems import MultiSurvivorProblem


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    x1,y1 = state
    x2,y2 = problem.goal
    return abs(x1-x2) + (y1-y2)


def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.
    """
    x1, y1 = state
    x2, y2 = problem.goal
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# (1) la versión inicial del código
"""    Heuristica preliminar para MultiSurvivorProblem.

    En esta primera versión combine:

        (1) Distancia al superviviente mas cercano
        +
        (2) Costo del MST

    usando el algoritmo de Kruskal, que ya conocia previamente por dalgo.

    En esta versión inicial se utilizo distancia Euclidiana porque
    inicialmente no recordaba que el agente solo puede moverse
    en 4 direcciones (arriba, abajo, izquierda, derecha) como lo indica el enunciado.

    Tampoco conocia en esta etapa la técnica de caching usando
    problem.heuristicInfo, por lo que el MST se recalculaba
    completamente en cada llamada si. Si vi que era parte de 
    las pistas pero no entendia como funcionaba y pense que era inutil.
    """

"""def survivorHeuristic(state: Tuple[Tuple, Any], problem: MultiSurvivorProblem):

    Your heuristic for the MultiSurvivorProblem.

    state: (position, survivors_grid)
    problem: MultiSurvivorProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider: distance to nearest survivor + MST of remaining survivors
    - Balance heuristic strength vs. computation time (do experiments!)
    # TODO: Add your code here
    position, survivors_grid = state
    survivors = survivors_grid.asList()

    # Caso base
    if not survivors:
        return 0

    # --------------------------------
    # 1. Distancia al superviviente mas cercano
    # --------------------------------
    closest_distances = []

    for sx, sy in survivors:
        dist = ((position[0] - sx) ** 2 + (position[1] - sy) ** 2) ** 0.5
        closest_distances.append(dist)

    closest_dist = min(closest_distances)

    # --------------------------------
    # 2. MST usando Kruskal 
    # --------------------------------

    n = len(survivors)

    if n == 1:
        mst_cost = 0
    else:
        edges = []

        for i in range(n):
            for j in range(i + 1, n):
                (x1, y1) = survivors[i]
                (x2, y2) = survivors[j]
                dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                edges.append((dist, i, j))

        edges.sort()

        # Union-Find
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            rootX = find(x)
            rootY = find(y)

            if rootX == rootY:
                return False

            if rank[rootX] < rank[rootY]:
                parent[rootX] = rootY
            elif rank[rootX] > rank[rootY]:
                parent[rootY] = rootX
            else:
                parent[rootY] = rootX
                rank[rootX] += 1

            return True

        mst_cost = 0
        edges_used = 0

        for dist, i, j in edges:
            if union(i, j):
                mst_cost += dist
                edges_used += 1
                if edges_used == n - 1:
                    break

    return closest_dist + mst_cost """
#(2) los prompts que utilizó para refinarl
"""class MultiSurvivorProblem(SearchProblem): Find a path that rescues all survivors. State: (position, survivors_grid) - position: (x, y) tuple - survivors_grid: Grid of booleans (True = survivor present) Goal: All survivors rescued (survivors_grid.count() == 0)  def __init__(self, startingMissionState: RescueState): self.start = ( startingMissionState.getRescuerPosition(), startingMissionState.getSurvivors(), ) self.walls = startingMissionState.getWalls() self.startingMissionState = startingMissionState self._expanded = 0 self.heuristicInfo = {} # For caching heuristic computations def getStartState(self): return self.start def isGoalState(self, state): return state[1].count() == 0 def getSuccessors(self, state):  Returns successor states, the actions they require, and the terrain cost of the destination cell.  successors = [] self._expanded += 1 for direction in [ Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST, ]: x, y = state[0] dx, dy = Actions.directionToVector(direction) nextx, nexty = int(x + dx), int(y + dy) if not self.walls[nextx][nexty]: nextSurvivors = state[1].copy() nextSurvivors[nextx][nexty] = False # Rescue survivor if present stepCost = self.startingMissionState.getTerrainCost(nextx, nexty) successors.append((((nextx, nexty), nextSurvivors), direction, stepCost)) return successors def getCostOfActions(self, actions):  Returns the cost of a particular sequence of actions. Uses terrain cost per cell (same as game cumulative cost).  x, y = self.getStartState()[0] cost = 0 for action in actions: dx, dy = Actions.directionToVector(action) x, y = int(x + dx), int(y + dy) if self.walls[x][y]: return 999999 cost += self.startingMissionState.getTerrainCost(x, y) return cost def survivorHeuristic(state: Tuple[Tuple, Any], problem: MultiSurvivorProblem): position, survivors_grid = state survivors = survivors_grid.asList() # Caso base if not survivors: return 0 # -------------------------------- # 1. Distancia al superviviente mas cercano # -------------------------------- closest_distances = [] for sx, sy in survivors: dist = ((position[0] - sx) ** 2 + (position[1] - sy) ** 2) ** 0.5 closest_distances.append(dist) closest_dist = min(closest_distances) # -------------------------------- # 2. MST usando Kruskal # -------------------------------- n = len(survivors) if n == 1: mst_cost = 0 else: edges = [] for i in range(n): for j in range(i + 1, n): (x1, y1) = survivors[i] (x2, y2) = survivors[j] dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 edges.append((dist, i, j)) edges.sort() # Union-Find parent = list(range(n)) rank = [0] * n def find(x): if parent[x] != x: parent[x] = find(parent[x]) return parent[x] def union(x, y): rootX = find(x) rootY = find(y) if rootX == rootY: return False if rank[rootX] < rank[rootY]: parent[rootX] = rootY elif rank[rootX] > rank[rootY]: parent[rootY] = rootX else: parent[rootY] = rootX rank[rootX] += 1 return True mst_cost = 0 edges_used = 0 for dist, i, j in edges: if union(i, j): mst_cost += dist edges_used += 1 if edges_used == n - 1: break return closest_dist + mst_cost hay algo que se pueda mejorar? o algo que me haya faltado"""
#(3) versión final del código
def survivorHeuristic(state: Tuple[Tuple, Any], problem: MultiSurvivorProblem):
    """
    Your heuristic for the MultiSurvivorProblem.

    state: (position, survivors_grid)
    problem: MultiSurvivorProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider: distance to nearest survivor + MST of remaining survivors
    - Balance heuristic strength vs. computation time (do experiments!)
    """
    # TODO: Add your code here
    position, survivors_grid = state # (x, y), Grid 
    survivors = survivors_grid.asList() #Lista de tuplas de la ubicacion de supervivientes

    #Caso base: No hay supervivientes restantes 
    if not survivors:
        return 0
    #h(n) =manhattan
    # --------------------------------
    # 1. Distancia al superviviente mas cercano
    # --------------------------------
    closest_distances = []
    #Manhatan
    for sx, sy in survivors:
        dist = abs(position[0] - sx) + abs(position[1] - sy)
        closest_distances.append(dist)
    #distance to nearest survivor
    closest_dist = min(closest_distances)
    
    #h(n) =manhattan + MST
    # --------------------------------
    # 2) MST con kruskal
    # --------------------------------

    #Sorting para mst
    survivors_key = tuple(sorted(survivors))
    #Evitar recomputar el MST como se indico
    if survivors_key in problem.heuristicInfo:
        mst_cost = problem.heuristicInfo[survivors_key]
    else:

        n = len(survivors)

        
        if n == 1:
            mst_cost = 0
        else:
            # Armar ejes con manhattan
            edges = []
            for i in range(n):
                for j in range(i + 1, n):
                    (x1, y1) = survivors[i]
                    (x2, y2) = survivors[j]
                    dist = abs(x1 - x2) + abs(y1 - y2)
                    edges.append((dist, i, j))

            edges.sort()

            # Union-Find
            parent = list(range(n))
            rank = [0] * n

            def find(x):
                if parent[x] != x:
                    parent[x] = find(parent[x])
                return parent[x]

            def union(x, y):
                rootX = find(x)
                rootY = find(y)

                if rootX == rootY:
                    return False

                if rank[rootX] < rank[rootY]:
                    parent[rootX] = rootY
                elif rank[rootX] > rank[rootY]:
                    parent[rootY] = rootX
                else:
                    parent[rootY] = rootX
                    rank[rootX] += 1

                return True

            mst_cost = 0
            edges_used = 0

            for dist, i, j in edges:
                if union(i, j):
                    mst_cost += dist
                    edges_used += 1
                    if edges_used == n - 1:
                        break

        problem.heuristicInfo[survivors_key] = mst_cost

    return closest_dist + mst_cost
    utils.raiseNotDefined()
