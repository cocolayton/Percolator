import copy
from random import *

count = 0
class PercolationPlayer:

	# this function is used to determine how many possible triangles there are associated with
	# a each uncolored vertex in the graph
	#@classmethod
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


	# determine the center vertex (edges is a list and so is vertices)
	def GetCenterVertex(edges, vertices):
		edge1 = edges.pop()
		edge2 = edges.pop()
		
		v1 = edge1.a
		v2 = edge1.b

		if edge2.a == v1 or edge2.b == v1:
			return v1
		elif edge2.a == v2 or edge2.b == v2:
			return v2
		"""
		for edge in edges:
			v1 = edge.a
			v2 = edge.b
			if v1.color == v2.color:
				return v2
			
		color1_count = 0
		color2_count = 1
		vertex1 = Vertex(3) # placeholders
		vertex2 = Vertex(3)
		for vertex in vertices:
			if vertex.color == 0:
				color1_count +=1
				vertex1 = vertex
			else:
				color2_count += 1
				Vertex2 = vertex
		
		if color1_count > color2_count:
			return vertex1
		else:
			return vertex2
		"""


	# get neighbors of a given vertex
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


	# if we care about valid triangles
	def getNumTriangles(graph, vertex):
		allNeighbors = PercolationPlayer.Neighbors(graph, vertex)

		if len(allNeighbors) == 0:
			return 0
		else:
			for v, color in allNeighbors.items():
				neighbor1 = v
				color1 = color

				if color1 != vertex.color:
					triangle_list = allNeighbors.keys() # dict not list
					return len(triangle_list)

				else:
					valid_neighbors = {key:val for key, val in allNeighbors.items() if key != neighbor1} #better var names
					triangle_list = [neighbor_vertex for neighbor_vertex, neighbor_color in valid_neighbors.items() if neighbor_color != vertex.color] #need to remove from neighbors
					return len(triangle_list)


	#if we don’t care about valid triangles
	#def getNumTriangles(graph, vertex):
		#allNeighbors = PercolationPlayer.Neighbors(graph, vertex)
		#numNeighbors = len(allNeighbors)
		#return numNeighbors * (numNeighbors - 1) / 2



	# this function is going to return a dictionary all possible future states and the vertex
	# that was removed to achieve that state
	def getFutureStates(graph, player):
		all_vertices = graph.V
		new_graph_states = {}
		for vertex in all_vertices:
			if vertex.color == player:
				graph_copy = copy.deepcopy(graph)
				send_in_vertices = graph_copy.V
				vertex_send_in = Vertex(3) #placeholder
				for v in send_in_vertices:
					if v.color == vertex.color and v.index == vertex.index: #should be the same
						vertex_send_in = v
				
				new_graph = PercolationPlayer.RemoveVertex(graph_copy, vertex_send_in)
				new_graph_states[vertex] = new_graph
		
		return new_graph_states

	def getFutureFutureStates(graph, color):
		all_vertices = graph.V
		new_graph_states = []
		for vertex in all_vertices:
			if vertex.color == color: # !=
				graph_copy = copy.deepcopy(graph)
				send_in_vertices = graph_copy.V
				vertex_send_in = Vertex(3) #placeholder
				for v in send_in_vertices:
					if v.color == vertex.color and v.index == vertex.index: #should be the same
						vertex_send_in = v
				
				new_graph = PercolationPlayer.RemoveVertex(graph_copy, vertex_send_in)
				new_graph_states.append(new_graph)
		
		return new_graph_states


	# RemoveVertex(v) that takes v (an instance of a Vertex) and "deletes" v from the graph.
	# When you delete a vertex, delete the edges attached to it.
	def RemoveVertex(graph, v):
		# remove v from vertex list
		vertices_set = graph.V
		vertices_set.remove(v)
		graph.V = vertices_set
		

		new_edges_list = []
		for edge in graph.E:
			if edge.a != v and edge.b != v: # change to !
				new_edges_list.append(edge)

		graph.E = set(new_edges_list)


		vertices_still_in_graph = set()
		for edge in graph.E:
			vertices_still_in_graph.add(edge.a)
			vertices_still_in_graph.add(edge.b)

		graph.V = vertices_still_in_graph


		return graph



	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
	# Should return a vertex `v` from graph.V where v.color == -1
	#@staticmethod
	def ChooseVertexToColor(graph, player):
		global count
		if count % 3 != 0:
			list_vertices = graph.V
			potential_vertices = []
			for vertex in list_vertices:
				if vertex.color == -1:
					potential_vertices.append(vertex)
			v_dict = PercolationPlayer.GetNumVerticesAttached(potential_vertices, graph)
			biggest_num_vertices = 0
			vertex = Vertex(3) #just a placeholder until find the actual biggest vertex
			for key, value in v_dict.items():
				if value > biggest_num_vertices:
					biggest_num_vertices = value
					vertex = key
			count += 1
			return vertex
		else:
			list_vertices = graph.V
			potential_vertices = []
			for vertex in list_vertices:
				if vertex.color == -1:
					potential_vertices.append(vertex)
			v_dict = PercolationPlayer.GetNumVerticesAttached(potential_vertices, graph)
			smallest_num_vertices = len(graph.V)
			vertex = Vertex(3)
			for key, value in v_dict.items():
				if value < smallest_num_vertices:
					smallest_num_vertices = value
					vertex = key
			count += 1
			return vertex

	def CheckIfWin4(graph_state, player):
		#print(len(graph_state.E))
		#print(len(graph_state.V))
		#print()
		if len(graph_state.E) == 3 and len(graph_state.V) == 3: # a fully connected trianlge = we win since going second
			return True
		elif len(graph_state.E) == 2 and len(graph_state.V) == 3:
			#print(graph_state)
			middle_vertex = PercolationPlayer.GetCenterVertex(graph_state.E, graph_state.V)
			if middle_vertex.color == player:
				return True
			else:
				return False
		elif len(graph_state.E) == 2 and len(graph_state.V) == 4: #four vertices
			colorPlayer = 0
			colorOther = 0

			for vertex in graph_state.V:
				if vertex.color == player:
					colorPlayer += 1
				else:
					colorOther += 1

			if len(colorPlayer) == 4 or len(colorPlayer) == 3:
				return True
			elif len(colorPlayer) == 0 or len(colorPlayer) == 1 or len(colorPlayer) == 2:
				return False

		else:
			color_count = 0
			for vertex in graph_state.V:
				if vertex.color == player:
					color_count += 1

			if color_count > 0:
				return True
			else:
				return False

	def CheckIfWin3(graph_state, player):
		if len(graph_state.E) == 2:
			middle_vertex = PercolationPlayer.GetCenterVertex(graph_state.E, graph_state.V)
			if middle_vertex.color == player:
				return middle_vertex
		else:
			return None

	def SpecialCase(graph, player):
		pass
		# need to call future states where test if remove each thing and see if results in winning state

	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
	# Should return a vertex `v` from graph.V where v.color == player
	def ChooseVertexToRemove(graph, player):
		if len(graph.V) == 6:
			future_states = PercolationPlayer.getFutureStates(graph, player)
	
			highest_win_probability = -1
			highest_vertex = Vertex(3)
	
			for vertex, state in future_states.items():
				win_count = 0
				win_probability = 0
				denominator = 0
				future_future_states = PercolationPlayer.getFutureFutureStates(state, 1-player)
		
				for future_future_state in future_future_states:
					future_future_future_states = PercolationPlayer.getFutureFutureStates(state, player) # adapt function so not just other player
					denominator = denominator + len(future_future_future_states)
					
					for future_future_future_state in future_future_future_states:
						vertices_future_future_future_state = future_future_future_state.V
						is_player_color_in_graph = 0
						
						for v in vertices_future_future_future_state:
							if v.color == player:
								is_player_color_in_graph += 1

						if is_player_color_in_graph > 0 and len(future_future_future_state.V) == 3 and len(future_future_future_state.E) == 3: # this is a connected triangle CHECK FOR COLORS OF OTHER PLAYER
							win_count += 1
						
						if len(future_future_future_state.V) == 3:
							edges = future_future_future_state.E
							vertices = future_future_future_state.V
							middle_vertex = PercolationPlayer.GetCenterVertex(edges, vertices)
						
							if len(edges) == 2 and middle_vertex.color == player:
								win_count += 1

						if len(future_future_future_state.V) == 2:
							colorOther = 0
							for v in future_future_future_state.V:
								if v.color != player:
									colorOther += 1
							
							if colorOther != 2:
								win_count += 1
		
				#print("win count", win_count)
				#print("denom", len(future_future_states))

				if denominator != 0:
					win_probability = win_count/denominator
				else:
					win_probability = 0 #double check this (what if no future future future states)
				
				if win_probability == 1:
					##print("n=6  prob = 1", vertex)
					#print("player", player)
					return vertex
				elif win_probability > highest_win_probability:
					highest_win_probability = win_probability
					highest_vertex = vertex
					#print("highest", highest_vertex)
			
			#print("n=6", highest_vertex)
			#print("player", player)
			return highest_vertex


		if len(graph.V) == 5:
			#print("N=5")
			future_states = PercolationPlayer.getFutureStates(graph, player)
	
			highest_win_probability = -1
			highest_vertex = Vertex(3)
	
			for vertex, state in future_states.items():
				win_count = 0
				win_probability = 0
				future_future_states = PercolationPlayer.getFutureFutureStates(state, 1-player)
				for future_future_state in future_future_states:
					if len(future_future_state.V) == 3:
						edges = future_future_state.E
						vertices = future_future_state.V
						middle_vertex = PercolationPlayer.GetCenterVertex(edges, vertices)
						
						if len(edges) == 2 and middle_vertex.color == player:
							win_count += 1

					if len(future_future_state.V) == 2:
						colorOther = 0
						for v in future_future_state.V:
							if v.color != player:
								colorOther += 1
						if colorOther != 2:
							win_count += 1

				#print("win count", win_count)
				#print("denom", len(future_future_states))

				if len(future_future_states) != 0:
					win_probability = win_count/len(future_future_states)
				else:
					win_probability = 0
				
				if win_probability == 1:
					#print("player", player)
					#print("vertex", vertex)
					#print("n=5  prob = 1", vertex)
					return vertex
				elif win_probability > highest_win_probability:
					highest_win_probability = win_probability
					highest_vertex = vertex
					#print("highest", highest_vertex)
			
			#print("n=5", highest_vertex)
			#print("player", player)
			return highest_vertex


		# When down to the last four total vertices — look ahead
		if len(graph.V) == 4: #len>1
			future_states = PercolationPlayer.getFutureStates(graph, player)
			for vertex, graph_state in future_states.items():
				# losing states for 3 or less vertices: two vertices that are different colors/their colors
				# winning: connected triangle (because we would go second)
				# triangle with us as center vertex
				isWinningState = PercolationPlayer.CheckIfWin4(graph_state, player)
				if isWinningState:
					#print("vertex", vertex)
					return vertex

			# if there aren’t any winners then pick randomly
			for v in graph.V:
				if v.color == player:
					#print("random pick 1", v)
					return v

		if len(graph.V) == 3:
			# if triangle is open and we are in middle then pick middle vertex
			winning_vertex = PercolationPlayer.CheckIfWin3(graph, player)
			if winning_vertex != None:
				
				return winning_vertex
			else:
				# if there aren’t any winners (ie closed triangle or we aren't middle vertex) then pick randomly
				for v in graph.V:
					if v.color == player:
						return v
		else:
			# If not down to last four vertices, proceed as usual
			min_num_triangles = 1000
			chosen_vertex = Vertex(3) #placeholder
			for vertex in graph.V:
				if vertex.color == player:
					num_triangles = PercolationPlayer.getNumTriangles(graph, vertex)

					if num_triangles < min_num_triangles:
						min_num_triangles = num_triangles
						chosen_vertex = vertex
			return chosen_vertex


			"""
		elif len(graph.V) == 1: # MORE EFFICIENT WAY TO TO DO THIS?
			for v in graph.V:
					if v.color == player:
						print("n=1", v)
						#print("random pick 3", v)
						return v
		"""

	
	# Feel free to put any personal driver code here.
	#def main():
    	#pass


#if __name__ == "__main__":
    #main()



class Vertex:
	# `index` is a unique integer identifier, `color` is an integer in [-1, 0, 1].
	# Silver vertices have color=0, and teal vertices have color=1.
	# Unmarked vertices have color=-1.
	def __init__(self, index, color=-1):
		self.index = index
		self.color = color

class Edge:
	# `a` and `b` are Vertex objects corresponding to the endpoints of this edge.
	def __init__(self, a, b):
		self.a = a
		self.b = b

class Graph:
	# `vertices` and `edges` are iterables of Vertex and Edge objects respectively
	# Internally, we store these as set()s on the graph class.
	def __init__(self, vertices, edges):
		self.V = set(vertices)
		self.E = set(edges)





#####################TESTING

import random
import itertools
import copy
import sys
import traceback

import time
import signal
import errno

from util import *


# Removes the given vertex v from the graph, as well as the edges attached to it.
# Removes all isolated vertices from the graph as well.
def Percolate(graph, v):
    # Get attached edges to this vertex, remove them.
    for e in IncidentEdges(graph, v):
        graph.E.remove(e)
    # Remove this vertex.
    graph.V.remove(v)
    # Remove all isolated vertices.
    to_remove = {u for u in graph.V if len(IncidentEdges(graph, u)) == 0}
    graph.V.difference_update(to_remove)

class TimeoutError(Exception):
    pass

class Timeout:
    def __init__(self, seconds=0.5, error_message="Timeout of {0} seconds hit"):
        self.seconds = seconds
        self.error_message = error_message.format(seconds)
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.setitimer(signal.ITIMER_REAL, self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)


# This is the main game loop.
def PlayGraph(s, t, graph):
    players = [s, t]
    active_player = 0

    # Phase 1: Coloring Phase
    while any(v.color == -1 for v in graph.V):
        # First, try to just *run* the player's code to get their vertex.
        try:
            with Timeout():
                chosen_vertex = players[active_player].ChooseVertexToColor(copy.deepcopy(graph), active_player)

        # If user code does not return within appropriate timeout, select random action.
        except TimeoutError as e:
            print(e)
            traceback.print_exc(file=sys.stdout)
            chosen_vertex = RandomPlayer.ChooseVertexToColor(copy.deepcopy(graph), active_player)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Next, check that their output was reasonable.
        try:
            original_vertex = GetVertex(graph, chosen_vertex.index)
            if not original_vertex:
                return 1 - active_player
            if original_vertex.color != -1:
                return 1 - active_player
            # If output is reasonable, color this vertex.
            original_vertex.color = active_player
        # Only case when this should fire is if chosen_vertex.index does not exist or similar error.
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player

        # Swap current player.
        active_player = 1 - active_player

    # Check that all vertices are colored now.
    assert all(v.color != -1 for v in graph.V)

    # Phase 2: Removal phase
    # Continue while both players have vertices left to remove.
    while len([v for v in graph.V if v.color == active_player]) > 0:
        # First, try to just *run* the removal code.
        try:
            with Timeout():
                chosen_vertex = players[active_player].ChooseVertexToRemove(copy.deepcopy(graph), active_player)

        # If user code does not return within appropriate timeout, select random action.
        except TimeoutError as e:
            print(e)
            traceback.print_exc(file=sys.stdout)
            chosen_vertex = RandomPlayer.ChooseVertexToRemove(copy.deepcopy(graph), active_player)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Next, check that their output was reasonable.
        try:
            original_vertex = GetVertex(graph, chosen_vertex.index)
            if not original_vertex:
            	print("BAD 1")
            	return 1 - active_player
            if original_vertex.color != active_player:
            	print("BAD 2")
            	return 1 - active_player
            # If output is reasonable, remove ("percolate") this vertex + edges attached to it, as well as isolated vertices.
            Percolate(graph, original_vertex)
        # Only case when this should fire is if chosen_vertex.index does not exist or similar error.
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Swap current player
        active_player = 1 - active_player

    # Winner is the non-active player.
    return 1 - active_player


# This method generates a binomial random graph with 2k vertices
# having probability p of an edge between each pair of vertices.
def BinomialRandomGraph(k, p):
    v = {Vertex(i) for i in range(2 * k)} # 2*k
    e = {Edge(a, b) for (a, b) in itertools.combinations(v, 2) if random.random() < p}
    return Graph(v, e)


# This method creates and plays a number of random graphs using both passed in players.
def PlayBenchmark(p1, p2, iters):
    graphs = (
        BinomialRandomGraph(random.randint(1, 20), random.random()) #20 
        for _ in range(iters)
    )
    wins = [0, 0]
    for graph in graphs:
        g1 = copy.deepcopy(graph)
        g2 = copy.deepcopy(graph)
        # Each player gets a chance to go first on each graph.
        winner_a = PlayGraph(p1, p2, g1)
        winner_b = PlayGraph(p2, p1, g2)
        wins[1-winner_b] += 1
    return wins


# This is a player that plays a legal move at random.
class RandomPlayer:
    # These are "static methdods" - note there's no "self" parameter here.
    # These methods are defined on the blueprint/class definition rather than
    # any particular instance.
    def ChooseVertexToColor(graph, active_player):
        return random.choice([v for v in graph.V if v.color == -1])

    def ChooseVertexToRemove(graph, active_player):
    	#print("other player choice")
    	#print(random.choice([v for v in graph.V if v.color == active_player]))
    	return random.choice([v for v in graph.V if v.color == active_player])


if __name__ == "__main__":
    # NOTE: we are not creating INSTANCES of these classes, we're defining the players
    # as the class itself. This lets us call the static methods.
    p1 = RandomPlayer
    # Comment the above line and uncomment the next two if
    # you'd like to test the PercolationPlayer code in this repo.
    # from percolator import PercolationPlayer
    # p1 = PercolationPlayer
    p2 = PercolationPlayer
    iters = 200
    wins = PlayBenchmark(p1, p2, iters)
    print(wins)
    print(
        "Player 1: {0} Player 2: {1}".format(
            1.0 * wins[0] / sum(wins), 1.0 * wins[1] / sum(wins)
        )
    )