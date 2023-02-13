import minimax
import monte
import fight
import sys


if __name__ == "__main__":
	if(sys.argv[1] == "1"):
		n = int(input("Add number of Iterations (*1000) for Monte Carlo:"))
		monte.main_monte(n)
	if(sys.argv[1] == "2"):
		n = int(input("Add search depth limit for MiniMax:"))
		minimax.main_minmax(n)
	if(sys.argv[1] == "3"):
		n = int(input("Add number of Iterations (*1000) for Monte Carlo:"))
		m = int(input("Add search depth limit for MiniMax:"))
		fight.main_fight(n,m)
	else:
		print("Invalid argument provided!")
