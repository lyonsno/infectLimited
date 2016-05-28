import random
import math

import pickler
from logger import logger
from user import User
from infecter import Infecter
from graphVisualizer import GraphVisualizer
import graphTraverser

class CoachingGraph():	
	def __init__(self):
		self.users = []
		self.infecter = Infecter()
		self.visualizer = GraphVisualizer(self.users)

	def init_random(self, numUsers):
		self.users = []
		self.create_and_add_users(numUsers)
		self.make_random_connections(3)

	def create_and_add_users(self, numUsers):
		for i in range(numUsers):
			user = User()
			self.add_user(user)

	def make_random_connections(self, iterations):
		for i in range(iterations):
			for user in self.users:
				self.make_random_connection(user)

	# generates a random aproximation of coach coachee relations
	def init_semi_random(self, size, connectionFactor=10, coacheesFactor=2):
		self.users = []

		numCoaches = (size // 6) + 1
		remainingCoachees = size - numCoaches
		coacheesPerCoach = remainingCoachees // numCoaches
		remaining = size

		while remaining > 0:

			numCoachees = random.randint(1, math.floor(coacheesPerCoach * coacheesFactor))
			remaining -= 1

			numCoachees = min(numCoachees, remaining)
			self.add_coach(numCoachees)
			remaining -= numCoachees

		self.make_sparse_random_connections(size // connectionFactor)

	def init_semi_random_connected(self, size):
		self.init_semi_random(size, connectionFactor=1)

	def add_coach(self, numCoachees):
		coach = User()
		self.add_user(coach)
		self.add_coachees(coach, numCoachees)

	def add_coachees(self, user, numToAdd):
		if user not in self.users: return
		for i in range(numToAdd):
			coachee = User()
			self.add_user(coachee)
			self.create_coach_coachee_relationship(user, coachee)

	def make_sparse_random_connections(self, numConnections):
		for user in random.sample(self.users, numConnections):
				self.make_random_connection(user)

	def make_random_connection(self, user):
		coachee = user
		while coachee == user:
			coachee = random.choice(self.users)
			if coachee in user.neighbors: continue
		self.create_coach_coachee_relationship(user, coachee)

	def add_user(self, user):
		if user in self.users: return
		self.users.append(user)

	def add_users(self, users):
		for user in users:
			self.add_user(user)

	def create_coach_coachee_relationship(self, userA, userB):
		if userA not in self.users or userB not in self.users: return
		userA.add_coachee(userB)
		userB.add_coach(userA)

	def clean(self):
		for user in self.users:
			user.infected = False
			user.numConnections = 0
			user.epicenter = False
			user.visited = False

	def draw(self):
		self.visualizer.update(self.users)
		self.visualizer.draw()

	def save_as(self, filename):
		self.visualizer.update(self.users)
		data = [self.users, self.visualizer]
		pickler.save_as(data, filename)

	def load_from(self, filename):
		try:
			data = pickler.load_file(filename)
		except FileNotFoundError:
			logger.error('Failed to load, File not found', exc_info=True)
			return
		except Exception:
			logger.error('Failed to load, something else went wrong', exc_info=True)
			return
		self.users, self.visualizer = data




