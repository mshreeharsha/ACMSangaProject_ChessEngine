
import random
import math

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 1
        self.visits = 1
        
    def expand(self):
        print(f'expansion \n{self.state}')
        legal_moves = self.state.findValidMoves()
        for move in legal_moves:
            self.state.makeMove(move)
            new_state = self.state
            self.state.undoMove()
            self.children.append(Node(new_state, self))

        
    def select_child(self, exploration_factor=1.4):
        best_child = None
        best_score = float("-inf")
        for child in self.children:
            score = child.wins / child.visits + exploration_factor * math.sqrt(math.log(self.visits) / child.visits)
            if score > best_score:
                best_child = child
                best_score = score
        print(f'best_child = \n{best_child}')
        return best_child
        
    def update(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.update(result)
        
class MCTS:
    def __init__(self, state):
        self.root = Node(state)
        
    def select_move(self, iterations=100):
        node = self.root
        for i in range(iterations):  
            if node.visits == 1:
                node.expand()
            else:
                node = node.select_child()
            
            result = self.simulate(node.state)
            node.update(result)
        best_move = None
        most_visits = -1
        for child in self.root.children:
            if child.visits > most_visits:
                best_move = child.state.moveLog[-1]
                most_visits = child.visits
        print(f'best_move \n{best_move}')
        return best_move
    
    def simulate(self, state):
        game_over = False
        while not game_over:
            legal_moves = state.findValidMoves()
            if not legal_moves:
                if state.checkmate:
                    if state.whiteToPlay:
                        return -1
                    else:
                        return 1
                else:
                    return 0
            move = random.choice(legal_moves)
            state.makeMove(move)
            game_over = state.checkmate or state.stalemate
        if (state.checkmate or state.stalemate) and not state.whiteToPlay :
            return 1
        else:
            return -1