import math
import random

import graphTraverser

class Infecter():

	def __init__(self):
		self.numUsersToInfect = 25

	def infect_single_user(self, user):
		user.infected = True

	def infect_from(self, user):
		graphTraverser.breadth_first_apply_function(user, self.infect_single_user)

	def infect_limited(self, users, numUsersToInfect):
		remaining = numUsersToInfect

		subgraphs = graphTraverser.get_subgraphs(users)
		subgraphs.sort(key=lambda subgraph: len(subgraph))

		for subgraph in subgraphs:
			if remaining <= 0: return

			bestStartCandidate = self.find_user_with_fewest_connections(subgraph)
			self.infect_limited_from(bestStartCandidate, remaining, 3)

			remaining -= self.get_num_infected(subgraph)


	def find_user_with_most_connections_up_to(self, users, maxConnections):
		mostConnections = 0
		userWithMost = None
		for user in users:
			numConnections = len(user.neighbors)
			if numConnections > mostConnections and numConnections <= maxConnections:
				mostConnections = numConnections
				userWithMost = user

		if userWithMost is None:
			userWithMost = self.find_user_with_fewest_connections(users)

		return userWithMost

	def find_user_with_num_connections_closest_to(self, users, goal):
		minDifference = math.inf
		closestUser = None
		for user in users:
			numConnections = len(user.neighbors)
			difference = abs(goal - numConnections)
			if difference < minDifference:
				minDifference = difference
				closestUser = user

		return closestUser

	def infect_limited_from(self, user, numUsersToInfect, fudgeFactor):
		user.epicenter = True
		self.infect_single_user(user)
		infectedUsers = [user]

		while len(infectedUsers) < numUsersToInfect:

			nextToInfect = None
			fewestConnections = math.inf

			for user in infectedUsers:
				
				neighborWithFewest = self.find_neighbor_with_fewest_neighbors(user)
				
				# no uninfected neighbors
				if neighborWithFewest is None:
					continue

				if neighborWithFewest.numConnections < fewestConnections:
					fewestConnections = neighborWithFewest.numConnections
					nextToInfect = neighborWithFewest

			if nextToInfect is None:
				return

			self.infect_single_user(nextToInfect)
			infectedUsers.append(nextToInfect)

	def find_neighbor_with_fewest_neighbors(self, user):
		cleanNeighbors = self.get_clean_neighbors(user)
		fewestNeighbors = math.inf
		neighborWithFewest = None
		for neighbor in cleanNeighbors:
			numNeighbors = len(self.get_clean_neighbors(neighbor))
			if numNeighbors < fewestNeighbors:
				neighbor.numConnections = numNeighbors
				fewestNeighbors = numNeighbors
				neighborWithFewest = neighbor


		return neighborWithFewest


	# TODO REMOVE IF NOT NEEDED
	def find_neighbor_with_fewest_connections(self, user):
		cleanNeighbors = self.get_clean_neighbors(user)
		leastConnections = math.inf

		neighborWithFewest = None

		for neighbor in cleanNeighbors:
			connections = graphTraverser.traverse_from_to_depth_collect_if_avoid_if(neighbor, 3, lambda neighbor: True, lambda neighbor: neighbor.infected)
			neighbor.numConnections = len(connections)
			if neighbor.numConnections < leastConnections:
				leastConnections = neighbor.numConnections
				neighborWithFewest = neighbor

		return neighborWithFewest

	def find_user_with_fewest_connections(self, users):
		fewestConnections = math.inf
		userWithFewest = None
		for user in users:
			numConnections = len(user.neighbors)
			if numConnections < fewestConnections: 
				fewestConnections = numConnections
				userWithFewest = user

		return userWithFewest 

	def get_all_clean_neighbors(self, users):
		cleanNeighbors = set()
		infected = [user for user in users if user.infected]
		for user in infected:
			cleanNeighbors.update(self.get_clean_neighbors(user))
		return cleanNeighbors

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
