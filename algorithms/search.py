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
    # TODO: Add your code here
    utils.raiseNotDefined()


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
