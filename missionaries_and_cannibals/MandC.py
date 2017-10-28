MISSIONARIES = 3 #Number of Missionaries at start
CANNIBALS = 3 #Number of Cannibals at start
BOAT_SIZE = 2 #Maximum number of passengers

#Holds a list of states and ensures no duplicates
class Data_Structure:
	states = [] #list of states
	current_id = 0 #current position in the list
	
	#returns the id for a given Cannibal, Missionaries and side combination, -1 if not found
	def Get_Id(self, c, m, side):
		id = -1
		for x in range(0, len(self.states)):
			if self.states[x].c == c and self.states[x].m == m and self.states[x].side == side:
				id = x
				break
		return id

	#creates a new state and returns id if it does not already exist, returns the id of the state if it already exists
	def Create_State(self, c, m, side, depth):
		id = self.Get_Id(c, m, side)
		if id == -1:
			self.states.append(State(c, m, side, depth))
			id = self.current_id
			self.current_id += 1

		return id	

#Holds the information for each state
class State:
	c = -1 			#Number of Cannibals on the right bank
	m = -1 			#Number of missionaries on the right bank
	side = 0 		#Which side the boat is on, 1 for right, -1 for left
	depth = -1 		#length of shortest path to the state from the initial state
	Following_States = [] 	#list of the ids of the states that are reachable in one move

	def __init__(self, given_c, given_m, given_side, given_depth):
		self.c = given_c
		self.m = given_m
		self.side = given_side
		self.depth = given_depth
		self.Following_States = []

	#Adds the given state to the following states list if it is not already there
	def Add_Follower(self, id):
		if id != -1 and id not in self.Following_States:
			self.Following_States.append(id)


tree = Data_Structure()

#Creates a new state if the new state is possible
def Send_Boat(id, c_over, m_over, depth):
	if c_over + m_over > 0 and m_over + c_over <= BOAT_SIZE:
		if ((tree.states[id].side-1)*tree.states[id].c <= (tree.states[id].side-1)*c_over and #If sending from the left side, is there enough cannibals
		(tree.states[id].side-1)*tree.states[id].m <= (tree.states[id].side-1)*m_over and #If sending from the left side, is there enough missionaries
		(tree.states[id].side+1)*(CANNIBALS-tree.states[id].c) >= (tree.states[id].side+1)*c_over and #If sending from the right side, is there enough cannibals
		(tree.states[id].side+1)*(MISSIONARIES-tree.states[id].m) >= (tree.states[id].side+1)*m_over and #if sending from the right side, is there enough missionaries
		(tree.states[id].m + m_over*tree.states[id].side == 0 or #will the missionaries not be outnumbered on the right side
		tree.states[id].m + m_over*tree.states[id].side >= tree.states[id].c + c_over*tree.states[id].side) and 
		(MISSIONARIES-tree.states[id].m - m_over * tree.states[id].side == 0 or #will the missionaries not be outnumbered on the left side
		MISSIONARIES-tree.states[id].m - m_over * tree.states[id].side >= CANNIBALS-tree.states[id].c - c_over*tree.states[id].side)):

			temp_id = tree.Create_State(tree.states[id].c + c_over*tree.states[id].side, tree.states[id].m + m_over*tree.states[id].side, tree.states[id].side*-1, depth)
			tree.states[id].Add_Follower(temp_id)


optimal_paths = [] #list of the optimal paths

#populates the optimal_paths list recursively
def rec_find_optimal(id, end_id, path = []):
  path.append(id)
  if id == end_id:	#if we reached the end state
    optimal_paths.append(path)
  elif tree.states[id].depth < tree.states[end_id].depth: #elif we still are not as deep as the end state
    for x in range(0,len(tree.states)):				#find a following state which is 1 deeper
      if tree.states[x].depth == tree.states[id].depth+1 and x in tree.states[id].Following_States:
        rec_find_optimal(x, end_id, list(path))


#create the initial state
id = tree.Create_State(0, 0, 1,0)

end_state_id = -1

while id < len(tree.states):	#loop through all states and try all possible actions to find more states
	if tree.states[id].c == CANNIBALS and tree.states[id].m == MISSIONARIES:
		end_state_id = id	#record the id of the end state

	for c_over in range(0,BOAT_SIZE+1):	#try all possible boat combinations
		for m_over in range(0,BOAT_SIZE-c_over+1):
			Send_Boat(id, c_over, m_over, tree.states[id].depth+1)
	
	id += 1


if end_state_id == -1: #if the end state was not found
	print("Unsolveable")
else:
  rec_find_optimal(0,end_state_id) #find all optimal paths
  for x in optimal_paths: #print all optimal paths
    path = ""
    pos = 0
    while pos+1 < len(x):
      path = path + "C"*(tree.states[x[pos+1]].c-tree.states[x[pos]].c) + "M"*(tree.states[x[pos+1]].m-tree.states[x[pos]].m) + "-"
      pos += 1
      if pos+1 < len(x):
        path = path + "C"*(tree.states[x[pos]].c-tree.states[x[pos+1]].c) + "M"*(tree.states[x[pos]].m-tree.states[x[pos+1]].m) + "-"
        pos += 1
    print (path[:-1])















