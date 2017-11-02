#Sudoku Solver
#to solve as a CSP it uses AC-3 to preprocess sudoku then uses Human logic to solve the sudoku then uses backtracking if that fails
#to solve as a 2d-array it uses human logic then backtracking if that fails

from __future__ import print_function
import time
import copy
import math
import numpy as np
from matplotlib import pyplot as plt

Start = [] #Given Matrix

Solved = [] #Solution Matrix

Queue_Length = []

#V = [[0,0],[1,0]]
#D = [[1,2,3,4,5,6,7,8,9],[1,2]]
#C = [[0,1],[1,0]] Does not Equal
#C contains variable indexes in the V list

def AC_Three(V,D,C):
	Q = []
	Q = copy.deepcopy(C)
	return AC_Three_Given_Queue(V,D,C,Q,True)

#performs AC_Three with a given queue
def AC_Three_Given_Queue(V,D,C,Q,report):
	valid = True
	global Queue_Length
	while valid and len(Q) != 0:
		if len(D[Q[0][1]]) == 1:
			if D[Q[0][1]][0] in D[Q[0][0]]:
				D[Q[0][0]].remove(D[Q[0][1]][0])
				for i in C:
					if i[1] == Q[0][0]:
						if i not in Q:
							Q.append(copy.deepcopy(i))
		elif len(D[Q[0][1]]) == 0:
			valid = False
		del Q[0]

		if report:
			Queue_Length.append(len(Q))
	return valid

def visualize_Queue(queue):
    x, y = queue, queue
    plt.scatter(x, y, alpha=0.9)
    plt.title('Sudoku Solver using AC-3 by Group11')
    plt.xlabel('Length of the Queue')
    plt.ylabel('count')
    plt.show()
    return None

#attempts to solve the sudoku the same way the average person does as a 2d-array
def human_logic(board):
	moves = 1
	while moves > 0: #loops until no moves are made
		moves = 0
		places = []
		possible = [[[True for k in range(0,9)] for j in range(0,9)] for i in range(0,9)] #list of all numbers that can go into every empty spot
		count = [[0 for k in range(9)] for j in range(9)] #count of possible nubers for each spot
		for x in range(0,9): #loop through all spots on the board
			for y in range(0,9):
				if board[x][y] == 0: #if spot is empty
					for t in range(0,9): #loop through the row, column and box associated with the spot, if not blank remove from possible
						if board[x][t] != 0:
							possible[x][y][board[x][t]-1] = False
						if board[t][y] != 0:
							possible[x][y][board[t][y]-1] = False
						if board[(x//3)*3+t%3][(y//3)*3+t//3] != 0:
							possible[x][y][board[(x//3)*3+t%3][(y//3)*3+t//3]-1] = False

					for t in range(0,9): #count possible numbers
						if possible[x][y][t]:
							count[x][y] = count[x][y] + 1

					if count[x][y] == 1: #if only 1 possible make the square that number
						for t in range(0,9):
							if possible[x][y][t]:
								board[x][y] = t+1
								moves = moves + 1
		
		for x in range(0,9): #loop through all rows, columns and boxes
			rowhas = [False for k in range(9)] #the numbers the row has
			colhas = [False for k in range(9)] #the numbers the column has
			boxhas = [False for k in range(9)] #the numbers the box has

			for y in range(0,9): #fill the lists
				if board[x][y] != 0:
					rowhas[board[x][y]-1] = True
				if board[y][x] != 0:
					colhas[board[y][x]-1] = True
				if board[x%3*3+y//3][x//3*3+y%3] != 0:
					boxhas[board[x%3*3+y//3][x//3*3+y%3]-1] = True
		
			for t in range(0,9): #check if there is only 1 possible place for a number in the row, column or box and record the move
				if not rowhas[t]:
					counter = 0
					pos = -1
					for y in range(0,9):
						if possible[x][y][t] and board[x][y] == 0:
							counter = counter + 1
							pos = y
					if counter == 1 and pos != -1:
						places.append([x,pos,t+1])
						moves = moves + 1

				if not colhas[t]:
					counter = 0
					pos = -1
					for y in range(0,9):
						if possible[y][x][t] and board[y][x] == 0:
							counter = counter + 1
							pos = y
					if counter == 1 and pos != -1:
						places.append([pos,x,t+1])
						moves = moves + 1

				if not boxhas[t]:
					counter = 0
					pos = -1
					for y in range(0,9):
						if possible[x%3*3+y//3][x//3*3+y%3][t] and board[x%3*3+y//3][x//3*3+y%3] == 0:
							counter = counter + 1
							pos = y
					if counter == 1 and pos != -1:
						places.append([x%3*3+pos//3,x//3*3+pos%3,t+1])
						moves = moves + 1

		for place in places: #make all recorded moves
			board[place[0]][place[1]] = place[2]

#attempts to solve the sudoku the same way the average person does as a CSP
def human_logic_CSP(V,D,C):
	moves = 1
	while moves > 0: #loops until no moves are made
		moves = 0
		changed = []
		
		rowhas = [[[0,0] for k in range(0,9)] for j in range(0,9)] #a counter of how many places in a row can have each number
		colhas = [[[0,0] for k in range(0,9)] for j in range(0,9)] #a counter of how many places in a column can have each number
		boxhas = [[[0,0] for k in range(0,9)] for j in range(0,9)] #a counter of how many places in a box can have each number

		for i in range(0,len(V)): #fill the lists
			if len(D[i]) != 1:
				for x in D[i]:
					rowhas[V[i][0]][x-1][0] += 1
					rowhas[V[i][0]][x-1][1] = i
					colhas[V[i][1]][x-1][0] +=1
					colhas[V[i][1]][x-1][1] = i
					boxhas[V[i][0]//3*3+V[i][1]//3][x-1][0] += 1
					boxhas[V[i][0]//3*3+V[i][1]//3][x-1][1] = i
				
		for x in range(0,9): #check if only one place can have the value
			for y in range(0,9):
				if rowhas[x][y][0] == 1:
					D[rowhas[x][y][1]] = [y+1]
					changed.append(rowhas[x][y][1])
				if colhas[x][y][0] == 1:
					D[colhas[x][y][1]] = [y+1]
					changed.append(colhas[x][y][1])
				if boxhas[x][y][0] == 1:
					D[boxhas[x][y][1]] = [y+1]
					changed.append(boxhas[x][y][1])
					
		Q = []
		for u in C:
			if u[1] in changed:
				Q.append(copy.deepcopy(u))
		AC_Three_Given_Queue(V,D,C,Q,False)
		moves = len(changed)
		
#finds the first blank space and trys all possible moves
def rec_trymove(board):
	global Solved
	if len(Solved) == 0: #if it's not already solved
		
		#loop to find first blank space
		for x in range(0,9):
			for y in range(0,9):
				if board[x][y] == 0:
					break
			if board[x][y] == 0:
				break
		if board[x][y] == 0:
			moves = [True] * 10 #list of possible moves
			for t in range(0,9): #loop to remove rule breaking moves
				moves[board[t][y]] = False #remove all values already in the row
				moves[board[x][t]] = False #remove all values already in the column
				moves[board[(x//3)*3+t%3][(y//3)*3+t//3]] = False #remove all values already in the box

			for t in range(1,10):
				if moves[t]: #loop to try all remaining moves
					board[x][y] = t
					rec_trymove(copy.deepcopy(board))
		else:
			Solved = copy.deepcopy(board) #save the completed matrix

#finds the first blank space and trys all possible moves
def rec_trymove_CSP(V,D,C):
	global Solved
	if len(Solved) == 0: #if it's not already solved
		
		min = 10
		minplace = -1
		#loop to find first blank space
		for i in range(0,len(V)):
			if len(D[i]) != 1 and len(D[i]) < min:
				min = len(D[i])
				minplace = i
		
		if min > 1 and min < 10:
			i = minplace
			for move in D[i]:
				D2 = copy.deepcopy(D)
				D2[i] = [move]
				Q = []
				for u in C:
					if u[1] == i:
						Q.append(copy.deepcopy(u))
				if AC_Three_Given_Queue(V,D2,C,Q,False):
					rec_trymove_CSP(V,D2,C)
				
		else:
			global Start
			Solved = copy.deepcopy(Start)
			for i in range(0,len(V)): #make any moves that AC-3 determined
				if len(D[i]) == 1:
					Solved[V[i][0]][V[i][1]] = D[i][0]
			
#Solves the given sudoku as a 2d-array			
def solve_sudoku(Start):	
	#start_time = time.time()
	global Solved
	print("Given:")
	for x in range(0,9): #print the given matrix
		for y in range(0,9):
			if Start[x][y] == 0:
				print("-", end = " "),
			else:
				print(Start[x][y],end=" ")
		print("")

	board = copy.deepcopy(Start)
	
	#if already solved, will do nothing. else it will apply basic sudoku solving logic. This step is to remove any low hanging fruit to avoid or speed up recursion.
	human_logic(board)
	
	#if already solved, then it will simply save the solution to Solved. else it will solve the sudoku recursivly
	rec_trymove(board)

	#print results
	print("")
	if len(Solved) == 0:
		print("Unsolveable")
	else:
		print("Solution:")
		for x in range(0,9): #print the completed matrix
			for y in range(0,9):
				print(Solved[x][y],end=" ")
			print("")
	print("")
	#print("Took %.4f seconds to run" % (time.time() - start_time))
	
#Solves the given sudoku as a CSP			
def solve_sudoku_CSP(Start):	
	#start_time = time.time()
	global Solved
	print("Given:")
	for x in range(0,9): #print the given matrix
		for y in range(0,9):
			if Start[x][y] == 0:
				print("-", end = " "),
			else:
				print(Start[x][y],end=" ")
		print("")
	print("")
	board = copy.deepcopy(Start)
		
		
	V = [] #Variable array
	D = [] #Domain array
	C = [] #Constraignt array
	for x in range(0,9): #populate V and D
		for y in range(0,9):
			V.append([x,y])
			if board[x][y] == 0:
				D.append([1,2,3,4,5,6,7,8,9])
			else:
				D.append([board[x][y]])
				
	for i in range(0,len(V)): #populate C
		for u in range(0,len(V)):
			if i != u and (V[i][0] == V[u][0] or V[i][1] == V[u][1] or (V[i][0]//3 == V[u][0]//3 and V[i][1]//3 == V[u][1]//3)):
				C.append([i,u])
	
	#Run AC-3 to pre-process array, sometimes will solve array
	valid = AC_Three(V,D,C)
	
	solved_by_AC_Three = True
	for x in D:
		if len(x) != 1:
			solved_by_AC_Three = False
	
	if solved_by_AC_Three:
		print("Solved by AC-3")
		Solved = copy.deepcopy(Start)
		for i in range(0,len(V)): #make any moves that AC-3 determined
			if len(D[i]) == 1:
				Solved[V[i][0]][V[i][1]] = D[i][0]
	elif valid:
		print("Not Solved by AC-3")
		#will apply basic sudoku solving logic. This step is to remove any low hanging fruit to avoid or speed up recursion.
		human_logic_CSP(V,D,C)
		
		#if already solved, then it will simply save the solution to Solved. else it will solve the sudoku recursivly
		rec_trymove_CSP(V,D,C)
		

	#print results
	if not valid:
		print("CSP determined invalid by AC-3")
	elif len(Solved) == 0:
		print("Unsolveable")
	else:
		print("Solution:")
		for x in range(0,9): #print the completed matrix
			for y in range(0,9):
				print(Solved[x][y],end=" ")
			print("")
	print("")
	#print("Took %.4f seconds to run" % (time.time() - start_time))



### TESTING ###


#Easy Suduko (AC-3 does nothing, fast to solve using logic, fast to solve using recursion)
Start.append([0,8,0,0,0,0,2,0,0])
Start.append([0,0,0,0,8,4,0,9,0])
Start.append([0,0,6,3,2,0,0,1,0])
Start.append([0,9,7,0,0,0,0,8,0])
Start.append([8,0,0,9,0,3,0,0,2])
Start.append([0,1,0,0,0,0,9,5,0])
Start.append([0,7,0,0,4,5,8,0,0])
Start.append([0,3,0,7,1,0,0,0,0])
Start.append([0,0,8,0,0,0,0,4,0])

solve_sudoku_CSP(Start)
visualize_Queue(Queue_Length)
print("Length of the queue is " + str(len(Queue_Length)))

Start = []
Solved = []
Queue_Length = []
print("------------------------------------")

#Solveable by AC-3
Start.append([0,0,3,0,2,0,6,0,0])
Start.append([9,0,0,3,0,5,0,0,1])
Start.append([0,0,1,8,0,6,4,0,0])
Start.append([0,0,8,1,0,2,9,0,0])
Start.append([7,0,0,0,0,0,0,0,8])
Start.append([0,0,6,7,0,8,2,0,0])
Start.append([0,0,2,6,0,9,5,0,0])
Start.append([8,0,0,2,0,3,0,0,9])
Start.append([0,0,5,0,1,0,3,0,0])

solve_sudoku_CSP(Start)
visualize_Queue(Queue_Length)
print("Length of the queue is " + str(len(Queue_Length)))

Start = []
Solved = []
Queue_Length = []
print("------------------------------------")

#AC-3 does nothing, fast to solve by logic
Start.append([0,0,0,1,0,0,7,0,2])
Start.append([0,3,0,9,5,0,0,0,0])
Start.append([0,0,1,0,0,2,0,0,3])
Start.append([5,9,0,0,0,0,3,0,1])
Start.append([0,2,0,0,0,0,0,7,0])
Start.append([7,0,3,0,0,0,0,9,8])
Start.append([8,0,0,2,0,0,1,0,0])
Start.append([0,0,0,0,8,5,0,6,0])
Start.append([6,0,5,0,0,9,0,0,0])

solve_sudoku_CSP(Start)
visualize_Queue(Queue_Length)
print("Length of the queue is " + str(len(Queue_Length)))

Start = []
Solved = []
Queue_Length = []
print("------------------------------------")

#Hardest Suduko (impossible to solve using logic, fast to solve using recursion)
Start.append([8,0,0,0,0,0,0,0,0])
Start.append([0,0,3,6,0,0,0,0,0])
Start.append([0,7,0,0,9,0,2,0,0])
Start.append([0,5,0,0,0,7,0,0,0])
Start.append([0,0,0,0,4,5,7,0,0])
Start.append([0,0,0,1,0,0,0,3,0])
Start.append([0,0,1,0,0,0,0,6,8])
Start.append([0,0,8,5,0,0,0,1,0])
Start.append([0,9,0,0,0,0,4,0,0])

solve_sudoku_CSP(Start)
visualize_Queue(Queue_Length)
print("Length of the queue is " + str(len(Queue_Length)))

Start = []
Solved = []
Queue_Length = []
print("------------------------------------")

#Brute force resistant Suduko (fast to solve using logic, very slow to solve using recursion)
Start.append([0,0,0,0,0,0,0,0,0])
Start.append([0,0,0,0,0,3,0,8,5])
Start.append([0,0,1,0,2,0,0,0,0])
Start.append([0,0,0,5,0,7,0,0,0])
Start.append([0,0,4,0,0,0,1,0,0])
Start.append([0,9,0,0,0,0,0,0,0])
Start.append([5,0,0,0,0,0,0,7,3])
Start.append([0,0,2,0,1,0,0,0,0])
Start.append([0,0,0,0,4,0,0,0,9])
	
solve_sudoku_CSP(Start)
visualize_Queue(Queue_Length)
print("Length of the queue is " + str(len(Queue_Length)))