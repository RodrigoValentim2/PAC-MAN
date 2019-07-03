# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
            
        print("Scores all", scores)    
        bestScore = max(scores)
        print("max scores", bestScore)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

      

        newFoodList = newFood.asList()
              
        print("Foods",  newFoodList)
        min_food_distance = -1
        for food in newFoodList:
            distance = util.manhattanDistance(newPos, food)
            if min_food_distance >= distance or min_food_distance == -1:
                min_food_distance = distance


        distances_to_ghosts = 1
        proximity_to_ghosts = 0
        for ghost_state in successorGameState.getGhostPositions():
            distance = util.manhattanDistance(ghost_state, newPos)
            distances_to_ghosts += distance
            if distance > 1:
                proximity_to_ghosts -= 1
                
                
        print("Sucessor", (successorGameState.getScore() + (1 / float(min_food_distance))))
        print("Dist min food",  (1 / float(min_food_distance)))
        print("Dist Ghost", (1 / float(distances_to_ghosts)) - proximity_to_ghosts)        
        print("Score", successorGameState.getScore() + (1 / float(min_food_distance)) - (1 / float(distances_to_ghosts)) - proximity_to_ghosts)
        print("Score combinado", successorGameState.getScore() + (1 / float(min_food_distance)) - (1 / float(distances_to_ghosts)) - proximity_to_ghosts)
        return successorGameState.getScore() + (1 / float(min_food_distance)) - (1 / float(distances_to_ghosts)) - proximity_to_ghosts

        # return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        def minimax(agent, depth, gameState):
       
           
            
            print("Se")
            
            """print(depth)
            
            gost1 = gameState.getGhostPositions()            
            print(gost1)
            newPos = gameState.getPacmanPosition()
            distance = util.manhattanDistance(gost1[0],  newPos)
            
            min_pac= -1
            if min_pac >= distance or min_pac == -1:
                min_pac = distance
            self.moveGhost(gameState , 2 , depth)""" 
                
            
            
            if gameState.isLose() or gameState.isWin() or depth == self.depth:  # return the utility in case the defined depth is reached or the game is won/lost.
                return self.evaluationFunction(gameState)
            if agent != 0: 
                depth += 1
                # maximize for GHOST
                return max(minimax(0, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
        

        """Performing maximize action for the root node i.e. pacman"""
        agent = 1       
        if agent != 0:
            maximum = float("-inf")
            action = Directions.WEST
            for agentState in gameState.getLegalActions(1):
                utility = minimax(0, agent, gameState.generateSuccessor(agent, agentState))
                if utility > maximum or maximum == float("-inf"):
                    maximum = utility
                    action = agentState
                    print(action)

        return random.choice(gameState.getLegalActions(0))
        # if gameState.isWin() or gameState.isLose():
        #   return Directions.STOP

        # nextMoves = gameState.getLegalPacmanActions()
        # num = gameState.getNumAgents() - 1
        # value = -BIGNUM
        # chosenMove = Directions.STOP
        
        # for move in nextMoves:
        #     nextState = gameState.generatePacmanSuccessor(move)
        #     if nextState.isWin():
        #         return move  # win the game immediately if it can 
        #     score = self.moveGhost(nextState, num, 1)
        #     if score > value:
        #         value = score
        #         chosenMove = move
        # return chosenMove
  
    def moveAgent(self, gameState , depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        nextMoves = gameState.getLegalPacmanActions()
        nextStates = [gameState.generatePacmanSuccessor(action) for action in nextMoves]
        num = gameState.getNumAgents() - 1
        scores = [self.moveGhost(nextState , num , depth + 1)  for nextState in nextStates]
        return max(scores)
      
    def moveGhost(self , gameState , ghostNum , depth):
      if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      nextMoves = gameState.getLegalActions(ghostNum)
      if len(nextMoves) == 0:
          return self.evaluationFunction(gameState)
      nextStates = [gameState.generateSuccessor(ghostNum, action)  for action in nextMoves]
      num = ghostNum - 1
      if num == 0:  # all ghosts has been moved 
          if depth == self.depth:  # has already explored enough depth 
              scores = [self.evaluationFunction(nextState) for nextState in nextStates]
          else:  # explore deeper, make pacman move the next 
              scores = [self.moveAgent(nextState , depth) for nextState in nextStates]
      else:  # move the next ghost in the list
          scores = [self.moveGhost(nextState, num , depth) for nextState in nextStates]
      return min(scores)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maximizer(agent, depth, game_state, a, b):  # maximizer function
            v = float("-inf")
            for newState in game_state.getLegalActions(agent):
                v = max(v, alphabetaprune(1, depth, game_state.generateSuccessor(agent, newState), a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v

        def minimizer(agent, depth, game_state, a, b):  # minimizer function
            v = float("inf")

            next_agent = agent + 1  # calculate the next agent and increase depth accordingly.
            if game_state.getNumAgents() == next_agent:
                next_agent = 0
            if next_agent == 0:
                depth += 1

            for newState in game_state.getLegalActions(agent):
                v = min(v, alphabetaprune(next_agent, depth, game_state.generateSuccessor(agent, newState), a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v

        def alphabetaprune(agent, depth, game_state, a, b):
            if game_state.isLose() or game_state.isWin() or depth == self.depth:  # return the utility in case the defined depth is reached or the game is won/lost.
                return self.evaluationFunction(game_state)

            if agent == 0:  # maximize for pacman
                return maximizer(agent, depth, game_state, a, b)
            else:  # minimize for ghosts
                return minimizer(agent, depth, game_state, a, b)

        """Performing maximizer function to the root node i.e. pacman using alpha-beta pruning."""
        utility = float("-inf")
        action = Directions.WEST
        alpha = float("-inf")
        beta = float("inf")
        for agentState in gameState.getLegalActions(0):
            ghostValue = alphabetaprune(1, 0, gameState.generateSuccessor(0, agentState), alpha, beta)
            if ghostValue > utility:
                utility = ghostValue
                action = agentState
            if utility > beta:
                return utility
            alpha = max(alpha, utility)

        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
