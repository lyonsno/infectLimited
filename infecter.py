import math
import random

from logger import logger
import graphTraverser

class Infecter():

	def __init__(self):
		pass 

	def infect_single_user(self, user):
		user.infected = True

	def infect_random(self, users, numToInfect):
		users = users[:]
		for i in range(numToInfect):
			user = random.choice(users)
			user.infected = True
			users.remove(user)

	def infect_all(self, users):
		for user in users:
			user.infected = True

	def infect_from(self, user):
		graphTraverser.breadth_first_apply_function(user, self.infect_single_user)

	def infect_limited(self, users, numUsersToInfect, acceptableErrorPercentage, debug=False):
		numOptionalUsers = self.get_int_percentage_of(numUsersToInfect, acceptableErrorPercentage)
		minNumToInfect = numUsersToInfect - numOptionalUsers
		maxNumToInfect = numUsersToInfect + numOptionalUsers
		remaining = minNumToInfect

		subgraphs = graphTraverser.get_subgraphs_sorted(users)

		finalSubgraph = None
		for subgraph in subgraphs:
			if remaining <= 0:
				break
			if debug:
				logger.info("\n")
				duds = 0
				for u in subgraph:
					if u not in users:
						duds += 1
				# noExtras = set(subgraph) in set(users)
				# logger.info("all subgraph users in users: {}".format(noExtras))
				logger.info("rouge users: {}".format(duds))
				logger.info("size of subgraph: {}".format(len(subgraph)))
				logger.info("remaining users before: {}".format(remaining))
			# 	debugInfected = self.get_num_infected(users)
			# 	logger.info("infected users: {}".format(debugInfected))

			bestStartCandidate = self.find_user_with_fewest_connections(subgraph)
			self.infect_limited_from(bestStartCandidate, remaining)

			remaining -= self.get_num_infected(subgraph)
			if debug:
				logger.info("new infected users: {}".format(self.get_num_infected(subgraph)))
				logger.info("total infected users: {}".format(self.get_num_infected(users)))
				debugInfected = self.get_num_infected(users)
				logger.info("remaining users after: {}".format(remaining))
			# if debug:
				# subgraphInfected = self.get_num_infected(subgraph)
				# logger.info("infected subgraph users: {}".format(subgraphInfected))
			# logger.info("remaining users: {}".format(remaining))
			finalSubgraph = subgraph

		optionalRemaining = maxNumToInfect - minNumToInfect 
		self.infect_while_improving(finalSubgraph, optionalRemaining)

	def get_int_percentage_of(self, value, percentage):
		return math.floor(value * (percentage / 100))

	def infect_limited_from(self, user, numUsersToInfect):
		user.epicenter = True
		self.infect_single_user(user)
		infectedUsers = [user]
		numInfected = 1
		while len(infectedUsers) < numUsersToInfect:

			nextToInfect = None
			fewestConnections = math.inf

			for user in infectedUsers:

				neighborWithFewest = self.find_neighbor_with_fewest_connections(user)
				
				# no uninfected neighbors
				if neighborWithFewest is None:
					continue

				if neighborWithFewest.numConnections < fewestConnections:
					fewestConnections = neighborWithFewest.numConnections
					nextToInfect = neighborWithFewest

			if nextToInfect is None:
				return

			self.infect_single_user(nextToInfect)
			numInfected += 1
			infectedUsers.append(nextToInfect)
			# logger.info("num infected by traversal: {}".format(numInfected))

	def infect_while_improving(self, users, limit):
		quality_level = self.get_solution_quality(users)
		remainingUsers = self.get_all_infected(users)
		while len(remainingUsers) > 0:
			user = remainingUsers.pop()
			for neighbor in self.get_clean_neighbors(user):
				if limit <= 0: return
				neighbor.infected = True
				new_quality_level = self.get_solution_quality(users)
				if new_quality_level > quality_level:
					neighbor.infected = False
				else:
					remainingUsers.append(neighbor)
					limit -= 1
					quality_level = new_quality_level

	def find_neighbor_with_fewest_connections(self, user):
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

	def find_user_with_fewest_connections(self, users):
		fewestConnections = math.inf
		userWithFewest = None
		for user in users:
			numConnections = len(user.neighbors)
			if numConnections < fewestConnections and user.infected == False: 
				fewestConnections = numConnections
				userWithFewest = user

		return userWithFewest 

	def get_all_infected(self, users):
		return [user for user in users if user.infected]

	def get_solution_quality(self, users):
		cleanNeighbors = []
		infected = [user for user in users if user.infected]
		for user in infected:
			cleanNeighbors.extend(self.get_clean_neighbors(user))
		return len(cleanNeighbors)

	def get_clean_neighbors(self, user):
		return [ neighbor for neighbor in user.neighbors if not neighbor.infected ]

	def get_num_infected(self, users):
		numInfected = 0
		for user in users:
			if user.infected:
				numInfected += 1
		return numInfected