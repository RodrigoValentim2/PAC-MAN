# ghostAgents.py
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


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util


class GhostAgent(Agent):
    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()


class RandomGhost(GhostAgent):
    "A ghost that chooses a legal action uniformly at random."

    def getDistribution(self, state):
        dist = util.Counter()
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist


class DirectionalGhost(GhostAgent):
    "A ghost that prefers to rush Pacman, or flee when scared."

    def __init__(self, index, prob_attack=0.8, prob_scaredFlee=0.8):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee
        self.master = 1

    def comunicacao(self, GhostAgent, state):
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        pos = state.getGhostPosition(self.index)
        isScared = ghostState.scaredTimer > 0

        print("Aguardando ordens do Agente 1")
        speed = 1

        if isScared:
            speed = 0.5

        actionVectors = [Actions.directionToVector(
            a, speed) for a in legalActions]
        newPositions = [(pos[0]+a[0], pos[1]+a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()
        isScared = ghostState.scaredTimer > 0
        if isScared:
            speed = 0.5

        # Select best actions given the state
        distancesToPacman = [manhattanDistance(
            pos, pacmanPosition) for pos in newPositions]
        if isScared:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_scaredFlee
        else:

            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip(
            legalActions, distancesToPacman) if distance == bestScore]
        print("# Construct distribution")
        # Construct distribution
        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += (1-bestProb) / len(legalActions)
        dist.normalize()
        return dist

    def getDistribution(self, state):
        # Read variables from state
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        isScared = ghostState.scaredTimer > 0
        speed = 1

        print(self.index)

        actionVectors = [Actions.directionToVector(
            a, speed) for a in legalActions]
        print(actionVectors)
        pos = state.getGhostPosition(self.index)
        print(pos)
        newPositions = [(pos[0]+a[0], pos[1]+a[1]) for a in actionVectors]

        pacmanPosition = state.getPacmanPosition()
        distancesToPacman = [manhattanDistance(
            pos, pacmanPosition) for pos in newPositions]
        if isScared:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack

        bestActions = [action for action, distance in zip(
            legalActions, distancesToPacman) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += (1-bestProb) / len(legalActions)
        dist.normalize()
        return dist


class MinimaxGhosts(GhostAgent):
    "A ghost that prefers to rush Pacman, or flee when scared."
    # message codes:
    # 1 - Danger zone

    def __init__(self, index, prob_attack=0.8, prob_scaredFlee=0.99):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee
        self.master = 1
        self.depth = 2
        self.mesage_board = []

    def minimax(self, depth, agent, state):
        print('Agent:', agent)
        print('State:', state.getLegalActions())

        speed = 1
        legal_actions = state.getLegalActions()
        actionVectors = [Actions.directionToVector(
            a, speed) for a in legal_actions]

        pos = state.getGhostPosition(self.index)

        newPositions = [(pos[0]+a[0], pos[1]+a[1]) for a in actionVectors]

        if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
        if agent != 0:
            depth += 1
            # maximize for GHOST
            return max(self.minimax(0, depth, state.generateSuccessor(agent, newState)) for newState in state.getLegalActions(agent))

    def evaluationFunction(self, state):

        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        isScared = ghostState.scaredTimer > 0
        speed = 1

        actionVectors = [Actions.directionToVector(
            a, speed) for a in legalActions]

        pos = state.getGhostPosition(self.index)

        newPositions = [(pos[0]+a[0], pos[1]+a[1]) for a in actionVectors]

        pacmanPosition = state.getPacmanPosition()
        distancesToPacman = [manhattanDistance(
            pos, pacmanPosition) for pos in newPositions]

        if (isScared or (any(message == 1 for message in self.mesage_board))):
            print('Message list:', self.mesage_board)
            raw_input()
            bestScore = max(distancesToPacman)
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack

        bestActions = [action for action, distance in zip(
            legalActions, distancesToPacman) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += (1-bestProb) / len(legalActions)
        dist.normalize()
        print('Dist>', dist)
        return dist

    def comunicacao(self, GhostAgent, state):

        pacmanPosition = state.getPacmanPosition()
        danger_zones = state.getCapsules()

        distancesToPoints = [manhattanDistance(
            pos, pacmanPosition) for pos in danger_zones]

        if(any(distance <= 1 for distance in distancesToPoints)):
            self.mesage_board.append(1)
        else:
            if(len(self.mesage_board) > 0):
                aux = list(set(self.mesage_board))
                aux.remove(1)
                self.mesage_board = aux

    def getDistribution(self, state):
        # Read variables from state
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        isScared = ghostState.scaredTimer > 0
        speed = 1
        print('Agent', )
        actionVectors = [Actions.directionToVector(
            a, speed) for a in legalActions]
        print(actionVectors)
        pos = state.getGhostPosition(self.index)
        print(pos)
        newPositions = [(pos[0]+a[0], pos[1]+a[1]) for a in actionVectors]

        print('Index:', self.index)

        print('State:', state)

        print('Minimax value', self.minimax(2, self.index, state))

        self.comunicacao(self.index, state)

        return self.minimax(2, self.index, state)
