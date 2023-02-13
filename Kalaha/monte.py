import numpy as np
import random

class state_monte:
  def __init__(self, array, player, games_won, games_played, parent):
    self.array = array
    self.player = player
    self.games_won = games_won
    self.games_played = games_played
    self.parent = parent
    self.children = set() 
    
  # Returns children reached from current state_monte
  # If the children have not yet been generated, generate them.

  def state_monte_children(self):
    if ( len(self.children)==0 ):
      self.children = self.accessible()
    return self.children


  # Upper Confidence Bound definition following Lecture 6 slides 18 to 22

  def ucb(self):
    first_term = self.games_won/self.games_played
    second_term = np.sqrt(2*np.log(self.parent.games_played)/self.games_played)
    return first_term + second_term

  # Overload comparison operators in order to be able to use min and max functions on state_monte objects
  # A state is considered smaller than another if its ucb fuction is smaller 
  # A state is considered larger than another if its ucb fuction is larger
  # If the games played for the state is zero, it is considered to be smaller.

  def __lt__(self,other_state_monte):
    if(other_state_monte.games_played!=0 and self.games_played!=0):
      return (self.ucb() < other_state_monte.ucb())
    elif (other_state_monte.games_played!=0):
      return False
    else:
      return True
  def __gt__(self,other_state_monte):
    if(other_state_monte.games_played!=0 and self.games_played!=0):    
      return (self.ucb() > other_state_monte.ucb()) 
    elif (other_state_monte.games_played!=0):
      return True
    else:
      return False

  def __ge__(self,other_state_monte):
    if(other_state_monte.games_played!=0 and self.games_played!=0):    
      return (self.ucb() >= other_state_monte.ucb()) 
    elif (other_state_monte.games_played!=0):
      return True
    else:
      return False

  def __le__(self,other_state_monte):
    if(other_state_monte.games_played!=0 and self.games_played!=0):
      return (self.ucb() <= other_state_monte.ucb())
    elif (other_state_monte.games_played!=0):
      return False
    else:
      return True 

  def __eq__(self,other_state_monte):
    return (self.games_won == other_state_monte.games_won and self.games_played == other_state_monte.games_played)

  # Overload __str__ and __repr__ functions for printing state_monte objects

  def __str__(self):
    a = 48 - sum(self.array)
    return """ 
          |{0}| [{12}] [{11}] [{10}] [{9}] [{8}] [{7}]
              [{1}] [{2}] [{3}] [{4}] [{5}] [{6}] |{13}|
        """.format(*self.array, a)
    
  def __repr__(self):
    a = 48 - sum(self.array)
    return """
       |{0}| [{12}] [{11}] [{10}] [{9}] [{8}] [{7}]
              [{1}] [{2}] [{3}] [{4}] [{5}] [{6}] |{13}|
        """.format(*self.array, a)

  def __hash__(self):
    return hash(str(self) + self.player)

  # Evaluation function for state s. Returns how good the current state is for the AI
  def eval(self):  
    return self.array[7:].sum() + self.array[0]


  # Generate all accessible states from current state
  def accessible(self):
    children = set()
    if(self.player == 'H'):
      for i in range(1,7):
        if( self.array[i] != 0):
          x = self.actions(i)
          children.add(state_monte(x[0], x[1], 0, 0, self))
    else:
      for i in range(7,13):
        if( self.array[i] != 0):
          x = self.actions(i)
          children.add(state_monte(x[0], x[1], 0, 0, self))
    self.children = children
    return children

  # Return new state of board and the next player, when the current player chooses pit "move"
  def actions(self, move):
    seeds = self.array[move]
    new_board = self.array.copy()
    next_player = self.player
    amount_stolen = 0

    new_board[move] = 0
    if(self.player == 'H'):
      l = ((seeds + 6 + move) % 13 - 6) % 13

      #Steal move
      if( (new_board[l] == 0 or l == move) and (seeds < 14) and (l in range(1,7)) and distribution_H(new_board.copy(),move, seeds)[13-l]!=0):
        new_board = distribution_H(new_board,move, seeds)
        amount_stolen = new_board[13 - l] 
        new_board[13 - l] = 0 
        new_board[l] = 0
        next_player = 'AI'

      #Macala Hit: Extra Turn  
      elif ((seeds + 6 + move) % 13 == 0):
        new_board = distribution_H(new_board,move, seeds) 
      
      #Simple play
      else:
        new_board = distribution_H(new_board,move, seeds) 
        next_player = 'AI'

    if(self.player == 'AI'):
      l =(seeds + move) % 13

      #Steal move
      if(seeds < 14 and l in range(7,13) and (self.array[l] == 0 or l == move) and distribution_H(new_board.copy(),move, seeds)[13-l]!=0):
        new_board = distribution_AI(new_board,move, seeds)
        new_board[0] += (new_board[13 - l] + 1)
        amount_stolen = new_board[13-l]  
        new_board[13-l] = 0
        new_board[l] = 0 
        next_player = 'H'
      
      #Mancala Hit: Extra Turn
      elif(l == 0):
        new_board = distribution_AI(new_board,move, seeds) 
      
      #Simple play
      else:
        new_board = distribution_AI(new_board ,move, seeds) 
        next_player = 'H'

    return (new_board, next_player, l, amount_stolen)

  # Check if state is terminal
  # The sum of seeds in all the pits of the Human or the pits of the AI must be 0
  
  def terminal(self):
      flag_1 = flag_2 = False
      
      if(sum(self.array[1:7]) == 0):
        flag_1 = True
      elif(sum(self.array[7:]) == 0 ):
        flag_2 = True

      return flag_1 or flag_2

  # Expand node: Find node from which the game will be run. The human player is assumed
  # to always choose the child that minimises the AI's chances of winning. The AI always 
  # chooses the child that maximises its chances of winning.

  def expand(self):
    current = self
    while(current.games_played != 0 and (not current.terminal())):
      if(current.player == 'H'):
        current = min(current.state_monte_children())

      elif(current.player == 'AI'):
        current = max(current.state_monte_children())
    return current

  # Rollout game: From the given state we play a game until we reach a terminal state.
  # The AI chooses randomly one of the children of the state.
  # The Human always chooses the child that has the smallest evaluation function, therefore
  # the child that's worst for the AI 

  def rollout(self):
    current = self
    while(not current.terminal()):
      if(current.player == 'AI'):
        current = random.choice(list(current.state_monte_children()))
      elif(current.player == 'H'):
        best = float('inf')
        for i in current.state_monte_children():
          if(i.eval() < best):
            best = i.eval()
            current = i
          
    if ((current.array[7:].sum() + current.array[0]) > (current.array[1:7].sum() + 48 - current.array.sum())): #check
        return True
    return False   

  # Back propagate until root: From the given state, go back until we reach the root
  # Update_state_monte: On each state, increase the number of games played
  # If the game was won, increase the number of games won


  def back_propagate(self, leaf, endresult):
    current = leaf
    while(current != self):
      current.update_state_monte(endresult)
      current = current.parent
      current.update_state_monte(endresult)

  def update_state_monte(self,endresult):
    self.games_played += 1
    if (endresult):
      self.games_won += 1

# Monte Carlo Tree Search consists of three steps that are looped N times:
#   Expand to a node
#   Rollout a new game from that node
#   Update said node and all parent nodes upto tree root according to game result

def monte_carlo(init_state_monte, N):
  while (N!=0):
    leaf = init_state_monte.expand()
    endresult = leaf.rollout()
    init_state_monte.back_propagate(leaf, endresult)
    N-=1
  return max(init_state_monte.state_monte_children())

# Distribute seeds on the mancala board when player is Human
def distribution_H(board, move, seeds):
    counter = 0
    i = 0
    while(counter < seeds):
      if((i + 1 + move + 6) % 13 != 0 and (( i + 1 + move) % 13) != 0 ):
        board[(i+1+move) % 13 ] += 1
        counter += 1
      elif( (i + 1 + move + 6) % 13 == 0):
        counter += 1
        if(counter<seeds):
           board[(i+1+move) % 13 ] += 1
           counter += 1
      i += 1
    return board

#Distribute seeds on the mancala board when player is AI
def distribution_AI(board, move, seeds):
    for i in range(seeds):
      board[(move + i + 1) % 13] += 1
    return board

def main_monte(m):
  print("Playing with Monte Carlo")
  print()
  print ("""For every move, choose a number between 1 and 6. 
  Choosing an empty spot is not allowed.""")
  init = state_monte(np.array([0,4,4,4,4,4,4,4,4,4,4,4,4]),'H',0,0,None)
  current = init
  print(current)
  while(not current.terminal()):
    if(current.player == 'H'):
      move = int(input("Your move :"))
      while(move > 6  or move < 1 or current.array[move] == 0):
        print("Invalid Spot! Choose again!")
        move = int(input("Your move :"))
      x = current.actions(move)
      current = state_monte(x[0], x[1], 0, 0, None)
      if (x[3]!=0):
        print("Nice steal!")
      print(current)

      while (current.player == 'H' and not current.terminal()):
        print("Play again")
        move = int(input("Your move :"))
        while(move > 6  or move < 1 or current.array[move] == 0):
          print("Invalid Spot! Choose again!")
          move = int(input("Your move :"))
        x = current.actions(move)
        current = state_monte(x[0], x[1], 0, 0, None)
        if (x[3]!=0):
          print("Nice steal!")
        print(current)

      if (current.terminal()):
        if ((current.array[7:].sum() + current.array[0]) > (current.array[1:7].sum() + 48 - current.array.sum())):
          print("AI won!")
          return 
        else:
          print("Human won!")
          return 

    elif(current.player == 'AI'):
      while(current.player == 'AI' and not current.terminal()):
        print("AI's turn:")
        turns = m*1000
        current = monte_carlo(current,turns)
        #current = current.minimax_2_ABP(9)
        print(current)   

  if ((current.array[7:].sum() + current.array[0]) > (current.array[1:7].sum() + 48 - current.array.sum())):
    print("AI won!")
  else:
    print("Human won!")
  return 
