
import math
import random

class Node:
    def __init__(self, state, moveplayed,parent = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.moveplayed=moveplayed
    
    def ucb_score(self):
        if self.visits == 0:
            return float('inf')
        
        return (self.wins / self.visits) + 1.4 * math.sqrt(2 * math.log(self.visits) / self.visits)

    def expand(self):
        legal_moves = self.state.findValidMoves()
        for move in legal_moves:
            self.state.makeMove(move)
            print(self.state.board)
            print("\n")
            new_state = self.state
            self.state.undoMove()
            self.children.append(Node(new_state, move,self))

    def select_child(self):
        best_child = None
        best_score = float('-inf')
        for child in self.children:
            score = self.ucb_score()
            if score > best_score:
                best_child = child
                best_score = score
        return best_child
    
    def update(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.update(result)

class MCTS:
    def __init__(self,gs):
        self.root = Node(gs,None)

    def select_move(self,iterations = 1):
        node = self.root
        for i in range(iterations):
            if node.visits == 0 or node.visits == 1:
                node.expand()
                for child in node.children:
                    result = self.simulate(node)
                    child.update(result)

            else:
                node = node.select_child()

        best_move = self.root.select_child()
        return best_move.moveplayed
    
    def simulate(self,node):
        game_over = False
        s=len(node.state.moveLog)
        while not game_over:
            legal_moves = node.state.findValidMoves()
            if not legal_moves:
                if node.state.checkmate:
                    if node.state.whiteToPlay:
                        return 1
                    else:
                        return 0
                else:
                    return 0.5
            move = random.choice(legal_moves)
            node.state.makeMove(move)
            game_over = node.state.stalemate or node.state.checkmate
        L=node.state.moveLog
        while(len(L)>s):
            undoMove()

        if node.state.whiteToPlay and game_over:
            return 1
        else:
            return 0
