import numpy as np
import minimax
import monte
import time

def board_reverse(state_array):
	end_array = state_array.copy()
	end_array[0] = 48 - state_array.sum()
	for i in range(1,7):
		end_array[i] = state_array[i+6]
		end_array[i+6] = state_array[i]
	return end_array

#monte plays first
def main_fight(n,m):
	init = monte.state_monte(np.array([0,4,4,4,4,4,4,4,4,4,4,4,4]),'AI',0,0,None)
	print("Initial State")
	current = init
	print(current)
	while(not current.terminal()):

		while(current.player == 'AI' and not current.terminal()):
			print("Monte Plays:")
			current = monte.monte_carlo(current,n)
			print(current)
			#time.sleep(3)

		current.array = board_reverse(current.array)
		current = minimax.state_minmax(current.array,'AI')

		while(current.player == 'AI' and not current.terminal()):
			print("Minimax Plays:")
			current = current.minimax_2_ABP(m)[1]
			current.array = board_reverse(current.array)
			print(current)
			current.array = board_reverse(current.array)
			#time.sleep(3)

		current.array = board_reverse(current.array)
		current = monte.state_monte(current.array,'AI',0,0,None)

	if ((current.array[7:].sum() + current.array[0]) > (current.array[1:7].sum() + 48 - current.array.sum())):
		print("Monte won!")
	else:
		print("Minimax won!")