from time import sleep
from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic


def tinyHouseSearch(problem: SearchProblem):
    """
    Returns a sequence of moves that solves tinyHouse. For any other building, the
    sequence of moves will be incorrect, so only use this for tinyHouse.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):     #   PUNTO 1
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    origin = problem.getStartState()
    print(origin)
    stack = utils.Stack()
    visited = set()
    stack.push((origin, []))
    actions = []
   
    while stack.isEmpty() == False:
        element, actions = stack.pop()
        
        if problem.isGoalState(element):
            return actions
        
        if element not in visited:
            visited.add(element)
            
            for succesor, action, cost in problem.getSuccessors(element):
                stack.push((succesor, actions + [action]))
                
            
    
    #utils.raiseNotDefined()


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    origin = problem.getStartState()
    queue = utils.Queue()
    visited = set()
    queue.push((origin, []))
    actions = []
   
    while queue.isEmpty() == False:
        element, actions = queue.pop()
        
        if problem.isGoalState(element):
            return actions
        
        if element not in visited:
            visited.add(element)
            
            for succesor, action, cost in problem.getSuccessors(element):
                queue.push((succesor, actions + [action]))
   
   
    
    #utils.raiseNotDefined()


def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """

    # TODO: Add your code here
    utils.raiseNotDefined()


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    frontera = utils.PriorityQueue()
    visitados = set()
    estado_inicial = problem.getStartState()
    # Item = (posicion_actual, lista_de_acciones, costo_g_acumulado)
    item_inicial = (estado_inicial, [], 0)
    # Prioridad: g + h
    prioridad_inicial = 0 + heuristic(estado_inicial, problem)
    frontera.push(item_inicial, prioridad_inicial)
    #ciclo while
    while not frontera.isEmpty():
        actual_estado, acciones, costo_g = frontera.pop()
        #si ya ha llegado a la meta
        if problem.isGoalState(actual_estado):
            return acciones
        if actual_estado not in visitados:
            visitados.add(actual_estado)
        #si no ha llegado a la meta
        for sucesor, accion, costoPaso in problem.getSuccessors(actual_estado):
            # 1. costo g de haber llegado ahi
            nuevo_costo_g = costo_g + costoPaso 
            # 2. prioridad (g+h)
            prioridad_f = nuevo_costo_g + heuristic(sucesor, problem)
            # 3. actualizar frontera
            frontera.push((sucesor, acciones + [accion], nuevo_costo_g), prioridad_f)



# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
