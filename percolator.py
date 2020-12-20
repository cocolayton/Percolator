import copy

# variable used later when chosing which vertices to color
count = 0

class PercolationPlayer:

	# this function is used to determine how many possible triangles there are associated with
	# a each uncolored vertex in the graph (used to determine which vertex to color)
	def GetNumVerticesAttached(list, graph):
		# return a dictionary {vertex: num vertices attached}
		attached = {}
		for v in list:
			num_neighbors = 0
			for element in graph.E:
				if element.a == v or element.b == v:
					num_neighbors = num_neighbors +1
				attached[v] = num_neighbors

		return attached


	# return the center vertex in a graph of three vertices and two edges
	# used to determine winning states for our player
	def GetCenterVertex(edges, vertices):
		edge1 = edges.pop()
		edge2 = edges.pop()
		
		v1 = edge1.a
		v2 = edge1.b

		if edge2.a == v1 or edge2.b == v1:
			return v1
		elif edge2.a == v2 or edge2.b == v2:
			return v2


	# returns a dictionary with the neighbors to a given vertex as the keys and the corresponding
	# color of each neighbor as its value
	def Neighbors(graph, v):
		neighbors = {}
		graph_edges = graph.E
		for element in graph_edges:
			if element.a == v:
				vertex2 = element.b
				neighbors[vertex2] = vertex2.color
			elif element.b == v:
				vertex1 = element.a
				neighbors[vertex1] = vertex1.color
		return neighbors


	# computes the number of triangles associated with a given vertex
	# a triangle is defined as having the given vertex in the middle have two vertices on either side
	# of that vertex where at least one is of the opposing player's color
	def getNumTriangles(graph, vertex):
		# get neighbors of the vertex
		allNeighbors = PercolationPlayer.Neighbors(graph, vertex)

		if len(allNeighbors) == 0:
			return 0
		else:
			for v, color in allNeighbors.items():
				neighbor1 = v
				color1 = color

				# we already know of the vertices is of the opposing players color so then all resulting triangles
				# made with this neighbor are valid
				if color1 != vertex.color:
					triangle_list = allNeighbors.keys()
					return len(triangle_list)
				else:
					# new dictionary without the neighbor that is acting as the first side vertex (key = neighboring vertex, value = vertex's color)
					valid_neighbors = {key:val for key, val in allNeighbors.items() if key != neighbor1}
					triangle_list = [neighbor_vertex for neighbor_vertex, neighbor_color in valid_neighbors.items() if neighbor_color != vertex.color]
					return len(triangle_list)


	# this function returns a dictionary of all possible future states (given an intial graph).
	# The keys are the vertices that were removed to achieve each state and the states are the values.
	def getFutureStates(graph, player):
		all_vertices = graph.V
		new_graph_states = {}
		for vertex in all_vertices:
			if vertex.color == player:
				graph_copy = copy.deepcopy(graph)
				send_in_vertices = graph_copy.V
				vertex_send_in = Vertex(3) #placeholder

				# vertex sent in has to be from the graph copy
				for v in send_in_vertices:
					if v.color == vertex.color and v.index == vertex.index:
						vertex_send_in = v
				
				new_graph = PercolationPlayer.RemoveVertex(graph_copy, vertex_send_in)
				new_graph_states[vertex] = new_graph
		
		return new_graph_states


	# this function returns a list of all possible future states given an intial graph and the color
	# of the player that is to remove a vertex. This function is used when we don't want a dictionary
	# that includes the vertices removed like above.
	def getFutureFutureStates(graph, color):
		all_vertices = graph.V
		new_graph_states = []
		for vertex in all_vertices:
			if vertex.color == color:
				graph_copy = copy.deepcopy(graph)
				send_in_vertices = graph_copy.V
				vertex_send_in = Vertex(3) #placeholder

				# vertex sent in has to be from the graph copy
				for v in send_in_vertices:
					if v.color == vertex.color and v.index == vertex.index:
						vertex_send_in = v
				
				new_graph = PercolationPlayer.RemoveVertex(graph_copy, vertex_send_in)
				new_graph_states.append(new_graph)
		
		return new_graph_states


	# RemoveVertex takes a given vertex and deletes it (and associated edges) from the graph.
	def RemoveVertex(graph, v):
		# remove v from vertex list
		vertices_set = graph.V
		vertices_set.remove(v)
		graph.V = vertices_set
		
		# make a new edge list given vertex removal
		new_edges_list = []
		for edge in graph.E:
			if edge.a != v and edge.b != v:
				new_edges_list.append(edge)

		graph.E = set(new_edges_list)

		# make new vertices list excluding any isolated vertices
		vertices_still_in_graph = set()
		for edge in graph.E:
			vertices_still_in_graph.add(edge.a)
			vertices_still_in_graph.add(edge.b)

		graph.V = vertices_still_in_graph

		return graph


	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
	# Should return a vertex `v` from graph.V where v.color == -1
	def ChooseVertexToColor(graph, player):
		global count # used to determine when to pick a vertex with max vs. min possible triangles
		if count % 3 != 0: # the number three was chosen so the player would pick the "max" vertex more often than "min"
			# make a list of possible vertices to choose from
			list_vertices = graph.V
			potential_vertices = []
			for vertex in list_vertices:
				if vertex.color == -1:
					potential_vertices.append(vertex)

			# dictionary that stores the number of possible triangles that can be formed by each vertex
			v_dict = PercolationPlayer.GetNumVerticesAttached(potential_vertices, graph)
			
			# return the vertex with max triangles
			biggest_num_vertices = 0
			vertex = Vertex(3) #placeholder
			for potential_vertex, num_triangles_possible in v_dict.items():
				if num_triangles_possible > biggest_num_vertices:
					biggest_num_vertices = num_triangles_possible
					vertex = potential_vertex
			
			count += 1
			return vertex
		else:
			# make a list of possible vertices to choose from
			list_vertices = graph.V
			potential_vertices = []
			for vertex in list_vertices:
				if vertex.color == -1:
					potential_vertices.append(vertex)

			# dictionary that stores the number of possible triangles that can be formed by each vertex
			v_dict = PercolationPlayer.GetNumVerticesAttached(potential_vertices, graph)
			
			# return the vertex with min triangles
			smallest_num_vertices = len(graph.V)
			vertex = Vertex(3)
			for potential_vertex, num_triangles_possible in v_dict.items():
				if num_triangles_possible < smallest_num_vertices:
					smallest_num_vertices = num_triangles_possible
					vertex = potential_vertex
			count += 1
			return vertex


	# In the case where we are removing a vertex from a graph of four vertices, the future states
	# (ie 3 or less vertices) are sent into this function to check if they are winning states or not
	def CheckIfWin4(graph_state, player):
		# a fully connected trianlge (3 edges, 3 vertices) = we win since we would approach it second
		if len(graph_state.E) == 3 and len(graph_state.V) == 3:
			return True
		# straight line or open triangle (2 edges, 3 vertices) -- we win if we have the middle vertex
		elif len(graph_state.E) == 2 and len(graph_state.V) == 3:
			middle_vertex = PercolationPlayer.GetCenterVertex(graph_state.E, graph_state.V)
			if middle_vertex.color == player:
				return True
			else:
				return False
		# two separate pairs of vertices -- we win if we are 3 or 4 of the vertices
		elif len(graph_state.E) == 2 and len(graph_state.V) == 4: #four vertices
			colorPlayer = 0 # keeping track of how many vertices belong to us

			for vertex in graph_state.V:
				if vertex.color == player:
					colorPlayer += 1

			if len(colorPlayer) == 4 or len(colorPlayer) == 3:
				return True
			elif len(colorPlayer) == 0 or len(colorPlayer) == 1 or len(colorPlayer) == 2:
				return False

		# one pair of vertices -- winning state if we occupy at least one of the two vertices
		else:
			color_count = 0 # keeping track of how many vertices belong to us
			for vertex in graph_state.V:
				if vertex.color == player:
					color_count += 1

			if color_count > 0:
				return True
			else:
				return False


	# If we face the situation of three vertices in the graph, this method is used to return a vertex
	# that will lead to a win or a random vertex if there is no vertex that will lead us to win 
	def CheckIfWin3(graph_state, player):
		# open triangle/straight line situation -- we win if we have the middle vertex
		if len(graph_state.E) == 2:
			middle_vertex = PercolationPlayer.GetCenterVertex(graph_state.E, graph_state.V)
			if middle_vertex.color == player:
				return middle_vertex
		# other option: connected triangle -- we automatically lose because we approach it first
		else:
			return None


	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
	# Should return a vertex `v` from graph.V where v.color == player
	def ChooseVertexToRemove(graph, player):
		# if six vertices in the graph, do a double look ahead to determine best vertex choice
		if len(graph.V) == 6:
			future_states = PercolationPlayer.getFutureStates(graph, player)
	
			highest_win_probability = -1
			highest_vertex = Vertex(3)
	
			for vertex, state in future_states.items():
				win_count = 0
				win_probability = 0
				denominator = 0 # used to calculate win probability

				# get the next set of future states
				future_future_states = PercolationPlayer.getFutureFutureStates(state, 1-player)
		
				for future_future_state in future_future_states:
					# then get the future states of those future states
					future_future_future_states = PercolationPlayer.getFutureFutureStates(state, player)
					denominator = denominator + len(future_future_future_states) # keeping track of number of possible outcomes
					
					for future_future_future_state in future_future_future_states:
						vertices_future_future_future_state = future_future_future_state.V
						is_player_color_in_graph = 0
						
						# make sure our color is still in the graph
						for v in vertices_future_future_future_state:
							if v.color == player:
								is_player_color_in_graph += 1

						# fully connected triangle = win for us
						if is_player_color_in_graph > 0 and len(future_future_future_state.V) == 3 and len(future_future_future_state.E) == 3:
							win_count += 1
						
						# straight line/open triangle -- if we are the middle vertex then we win
						elif len(future_future_future_state.V) == 3: #HEREEEEE
							edges = future_future_future_state.E
							vertices = future_future_future_state.V
							middle_vertex = PercolationPlayer.GetCenterVertex(edges, vertices)
						
							if len(edges) == 2 and middle_vertex.color == player:
								win_count += 1

						# if only two vertices we need to have at least one of those two
						elif len(future_future_future_state.V) == 2: #HEREEEEEE
							colorOther = 0
							for v in future_future_future_state.V:
								if v.color != player:
									colorOther += 1
							
							if colorOther != 2:
								win_count += 1

				if denominator != 0:
					win_probability = win_count/denominator
				else:
					win_probability = 0
				
				if win_probability == 1:
					return vertex # automatic win for us
				elif win_probability > highest_win_probability:
					highest_win_probability = win_probability
					highest_vertex = vertex

			return highest_vertex

		# if there's 5 vertices in the graph
		if len(graph.V) == 5:
			future_states = PercolationPlayer.getFutureStates(graph, player)
	
			highest_win_probability = -1
			highest_vertex = Vertex(3)
	
			for vertex, state in future_states.items():
				win_count = 0
				win_probability = 0

				# get the next set of future states
				future_future_states = PercolationPlayer.getFutureFutureStates(state, 1-player)

				for future_future_state in future_future_states:
					# the only way we win with 3 vertices still in the graph is if its an open
					# triangle/straight line and we have the center vertex
					if len(future_future_state.V) == 3:
						edges = future_future_state.E
						vertices = future_future_state.V
						middle_vertex = PercolationPlayer.GetCenterVertex(edges, vertices)
						
						if len(edges) == 2 and middle_vertex.color == player:
							win_count += 1

					# if only two vertices we need to have at least one of those two
					elif len(future_future_state.V) == 2: #HEREEEE
						colorOther = 0
						for v in future_future_state.V:
							if v.color != player:
								colorOther += 1
						if colorOther != 2:
							win_count += 1

				if len(future_future_states) != 0:
					win_probability = win_count/len(future_future_states)
				else:
					win_probability = 0
				
				if win_probability == 1:
					return vertex
				elif win_probability > highest_win_probability:
					highest_win_probability = win_probability
					highest_vertex = vertex

			return highest_vertex


		# When there's four vertices in the graph
		if len(graph.V) == 4:
			# get future states
			future_states = PercolationPlayer.getFutureStates(graph, player)
			for vertex, graph_state in future_states.items():
				# check if the future state is a winning state or not
				isWinningState = PercolationPlayer.CheckIfWin4(graph_state, player)
				
				if isWinningState:
					return vertex

			# if there aren’t any winners then pick randomly
			for v in graph.V:
				if v.color == player:
					return v

		# if there's 3 vertices in the graph
		if len(graph.V) == 3:
			# determine which vertex to pick that will lead to a win
			winning_vertex = PercolationPlayer.CheckIfWin3(graph, player)
			if winning_vertex != None:
				return winning_vertex
			else:
				# if there aren’t any winners (ie closed triangle or we aren't middle vertex) then pick randomly
				for v in graph.V:
					if v.color == player:
						return v
		else:
			# If more than six vertices in the graph, pick the vertex with the smallest number of possible trianlges
			min_num_triangles = 1000
			chosen_vertex = Vertex(3) #placeholder
			for vertex in graph.V:
				if vertex.color == player:
					num_triangles = PercolationPlayer.getNumTriangles(graph, vertex)

					if num_triangles < min_num_triangles:
						min_num_triangles = num_triangles
						chosen_vertex = vertex
			return chosen_vertex
