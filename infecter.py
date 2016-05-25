import graphTraverser
import math

class Infecter():

	def __init__(self):
		pass

	def infect_single_user(self, user):
		user.infected = True

	def infect_from(self, user):
		graphTraverser.breadth_first_apply_function(user, self.infect_single_user)

	def infect_limited_from(self, user, numUsersToInfect, fudgeFactor):
		user.epicenter = True
		self.infect_single_user(user)
		infectedUsers = [user]
		activeInfectedUsers = [user]

		while len(infectedUsers) < numUsersToInfect:

			nextToInfect = None
			fewestConnections = math.inf

			for user in infectedUsers:
				
				neighborWithFewest = self.find_neighbor_with_fewest_connections(user)
				if neighborWithFewest is None:
					continue
				if neighborWithFewest.numConnections < fewestConnections:
					fewestConnections = neighborWithFewest.numConnections
					nextToInfect = neighborWithFewest

			if nextToInfect is None:
				return

			self.infect_single_user(nextToInfect)
			infectedUsers.append(nextToInfect)

	def find_neighbor_with_fewest_connections(self, user):
		cleanNeighbors = self.get_clean_neighbors(user)
		leastConnections = math.inf

		neighborWithFewest = None

		for neighbor in cleanNeighbors:
			connections = graphTraverser.traverse_from_to_depth_collect_if_avoid_if(neighbor, 4, lambda neighbor: True, lambda neighbor: neighbor.infected)
			neighbor.numConnections = len(connections)
			if neighbor.numConnections < leastConnections:
				leastConnections = neighbor.numConnections
				neighborWithFewest = neighbor

		return neighborWithFewest

	def get_clean_neighbors(self, user):
		return [ neighbor for neighbor in user.neighbors if not neighbor.infected ]

	def find_most_isolated_hubs(self, users):
		
		for user in users:
			pass


	def get_num_infected(self, users):

		numInfected = 0

		for subgraph in graphTraverser.get_subgraphs(users):
			someUser = subgraph.pop()
			infected = graphTraverser.traverse_from_collect_if(someUser, lambda user: user.infected)
			numInfected += len(infected)

		return numInfected
