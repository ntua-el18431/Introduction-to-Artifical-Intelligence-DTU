import numpy as np

class state_minmax:
  def __init__(self, array, player):
    self.array = array
    self.player = player

  def accessible(self):
    # Generate all accessible states
    if(self.player == 'H'):
      for i in range(1, 7):
        if(self.array[i] != 0):
          x = self.actions(i)
          yield state_minmax(x[0], x[1])
    else:
      for i in range(7, 13):
        if(self.array[i] != 0):
          x = self.actions(i)
          yield state_minmax(x[0], x[1])

  def terminal(self):
      # The game is finished when either the human or the ai board has no seeds left
      flag_1 = flag_2 = False
      for i in range(1, 7):
        if(sum(self.array[1:7]) == 0):
          flag_1 = True
        elif(sum(self.array[7:]) == 0):
          flag_2 = True

      return flag_1 or flag_2

  def state_value(self):
    # Evaluating terminal nodes
    return self.array[0] + sum(self.array[7:])

  def utility(self):
    # Evaluating nodes in between
    # Number of seeds at mancala plus the players board
    state_minmax_eval = -1
    if(self.player == 'AI'):
      state_minmax_eval = sum(self.array[0:7])
    elif (self.player == 'H'):
      state_minmax_eval = 48 - sum(self.array[0:7])
    # Take into account potential steal moves and also getting a extra turn
    max_steal = 0
    max_move = 0
    if (self.player == 'H'):
      for i in range(1, 7):
        x = self.actions(i)
        max_steal = max(max_steal, x[3])
        if (x[1] == self.player):
          new_state_minmax = state_minmax(x[0], x[1])
          max_move = max(state_minmax_eval, new_state_minmax.utility())
    elif (self.player == 'AI'):
      for i in range(7, 13):
        x = self.actions(i)
        max_steal = max(max_steal, x[3])
        if (x[1] == self.player):
          new_state_minmax = state_minmax(x[0], x[1])
          max_move = max(state_minmax_eval, new_state_minmax.utility())

    move_eval = 2*max_steal + max_move
    return state_minmax_eval+move_eval
  # Printing  a state

  def __str__(self):
    a = 48 - sum(self.array)
    return """
          |{0}| [{12}] [{11}] [{10}] [{9}] [{8}] [{7}]
              [{1}] [{2}] [{3}] [{4}] [{5}] [{6}] |{13}|


        """.format(*self.array, a)

  def actions(self, move):
      seeds = self.array[move]
      new_board = self.array.copy()
      next_player = self.player
      amount_stolen = 0

      new_board[move] = 0
      if(self.player == 'H'):
        l = ((seeds + 6 + move) % 13 - 6) % 13

        # Steal move
        if((new_board[l] == 0 or l == move) and (seeds < 14) and (l in range(1, 7)) and distribution_H(new_board.copy(), move, seeds)[13-l] != 0):
          new_board = distribution_H(new_board, move, seeds)
          amount_stolen = new_board[13 - l]
          new_board[13 - l] = 0
          new_board[l] = 0
          next_player = 'AI'

        # Macala Hit: Extra Turn
        elif ((seeds + 6 + move) % 13 == 0):
          new_board = distribution_H(new_board, move, seeds)

        # Simple play
        else:
          new_board = distribution_H(new_board, move, seeds)
          next_player = 'AI'
      if(self.player == 'AI'):
        l = (seeds + move) % 13

        # Steal move
        if(seeds < 14 and l in range(7, 13) and (self.array[l] == 0 or l == move) and distribution_H(new_board.copy(), move, seeds)[13-l] != 0):
          new_board = distribution_AI(new_board, move, seeds)
          new_board[0] += (new_board[13 - l] + 1)
          amount_stolen = new_board[13-l]
          new_board[13-l] = 0
          new_board[l] = 0
          next_player = 'H'

        # Mancala Hit: Extra Turn
        elif(l == 0):
          new_board = distribution_AI(new_board, move, seeds)

        # Simple play
        else:
          new_board = distribution_AI(new_board, move, seeds)
          next_player = 'H'

      return (new_board, next_player, l, amount_stolen)

  def minimax_2_ABP(self, maxDepth=5):
    # AI's turn, try to maximize
    # Returns maximum output and chosen state that leads to it
    (best_utility, next_state_minmax) = self.max_value_2_ABP(maxDepth=maxDepth)
    return (best_utility, next_state_minmax)

  def max_value_2_ABP(self, depth=0, maxDepth=5, alpha=float('-inf'), beta=float('inf')):

    # Check if a state is terminal
    if self.terminal():
      return (self.state_value(), self)
    # Otherwise check if maximum depth of DFS iteration is reached
    elif(depth == maxDepth):
      return (self.utility(), self)
      # Increase depth
    depth += 1

    infinity=float('inf')
    max_value=(-1)*infinity  # v

    chosen_state_minmax=None
    # Generate all reachable states
    accessible_state_minmaxs=self.accessible()
    for state_minmax in accessible_state_minmaxs:
      if(state_minmax.player == 'AI'):
    # If AI gets an extra turn call the max function again for the generated state
        max_value=max(max_value, state_minmax.max_value_2_ABP(
            depth, maxDepth, alpha, beta)[0])
      else:
    # If it's human's turn seek to minimize value, thus call the min function
        max_value=max(max_value, state_minmax.min_value_2_ABP(
            depth, maxDepth, alpha, beta)[0])
    # Apply alpha-beta pruning
      if (max_value >= beta):
        return (max_value, self)

      if (max_value > alpha):
        chosen_state_minmax=state_minmax

      alpha=max(alpha, max_value)
    # After all the recursions, we always return the maximum outcome of the  original state
    # That's why, only the max_value function returns something as a second argument
    return (max_value, chosen_state_minmax)

  def min_value_2_ABP(self, depth=0, maxDepth=5, alpha=-100000, beta=100000):

    # Check if a state is termina
    if self.terminal():
      return (self.state_value(), self)
    # Otherwise check if maximum depth of DFS iteration is reached
    elif(depth == maxDepth):
      return (self.utility(), self)

    depth += 1

    infinity=float('inf')
    min_value=infinity

    # Generate all reachable states

    accessible_state_minmaxs=self.accessible()
    for state_minmax in accessible_state_minmaxs:

      # If human gets an extra turn call the min function again for the generated state
      if(state_minmax.player == 'H'):
        min_value=min(min_value, state_minmax.min_value_2_ABP(
            depth, maxDepth, alpha, beta)[0])
      else:
      # If it's AI's turn seek to maximize value, thus call the max function
        min_value=min(min_value, state_minmax.max_value_2_ABP(
            depth, maxDepth, alpha, beta)[0])

     # Apply alpha-beta pruning
      if (min_value <= alpha):
        return (min_value, self)

      beta=min(beta, min_value)

    return (min_value, self)

# Distribute seeds on the mancala board when player is Human
def distribution_H(board, move, seeds):
  counter=0
  i=0
  while(counter < seeds):
    if((i + 1 + move + 6) % 13 != 0 and ((i + 1 + move) % 13) != 0):
      board[(i+1+move) % 13] += 1
      counter += 1
    elif((i + 1 + move + 6) % 13 == 0):
      counter += 1
      if(counter < seeds):
          board[(i+1+move) % 13] += 1
          counter += 1
    i += 1
  return board

# Distribute seeds on the mancala board when player is AI
def distribution_AI(board, move, seeds):
  for i in range(seeds):
    board[(move + i + 1) % 13] += 1
  return board


def main_minmax(m):
  print("Playing with Minimax")
  print()
  print("""For every move, choose a number between 1 and 6.
  Choosing an empty spot is not allowed.""")
  init=state_minmax(np.array([0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]), 'H')
  current=init
  print(current)
  while(not current.terminal()):
    if(current.player == 'H'):
      move=int(input("Your move :"))
      while(move > 6 or move < 1 or current.array[move] == 0):
        print("Invalid Spot! Choose again!")
        move=int(input("Your move :"))
      x=current.actions(move)
      current=state_minmax(x[0], x[1])
      if (x[3] != 0):
        print("Nice steal!")
      print(current)

      while (current.player == 'H' and not current.terminal()):
        print("Play again")
        move=int(input("Your move :"))
        while(move > 6 or move < 1 or current.array[move] == 0):
          print("Invalid Spot! Choose again!")
          move=int(input("Your move :"))
        x=current.actions(move)
        current=state_minmax(x[0], x[1])
        if (x[3] != 0):
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
        current=current.minimax_2_ABP(m)[1]
        print(current)

  if ((current.array[7:].sum() + current.array[0]) > (current.array[1:7].sum() + 48 - current.array.sum())):
    print("AI won!")
  else:
    print("Human won!")
  return
