import random
from user import User

class CoachingGraph():
	def __init__(self):
		self.users = []

	def init_random(self, size):
		self.users = []
		for i in range(size):
			user = User()
			self.add_user(user)
		self.make_random_connections(3)

	def init_semi_random(self, size):
		self.users = []

		numCoaches = (size // 10) + 1
		remainingCoachees = size - numCoaches
		coacheesPerCoach = remainingCoachees // numCoaches
		remaining = size

		while remaining > 0:

			numCoachees = random.randint(1, coacheesPerCoach * 2)
			numCoachees = min(numCoachees, remaining)
			self.add_coach(numCoachees)
			remaining -= numCoachees + 1

		self.make_sparse_random_connections(size // 4)

	def add_coach(self, numCoachees):
		coach = User()
		self.add_user(coach)
		self.add_coachees(coach, numCoachees)

	def make_sparse_random_connections(self, numConnections):
		for user in random.sample(self.users, numConnections):
				self.make_random_connection(user)

	def make_random_connections(self, iterations):
		for i in range(iterations):
			for user in self.users:
				self.make_random_connection(user)

	def make_random_connection(self, user):
		coachee = user
		while coachee == user:
			coachee = random.choice(self.users)
			if user.has_coachee(coachee): continue
		self.start_coaching(user, coachee)

	def add_coachees(self, user, numToAdd):
		if user not in self.users: return
		for i in range(numToAdd):
			coachee = User()
			self.add_user(coachee)
			self.start_coaching(user, coachee)

	def add_user(self, user):
		self.users.append(user)

	def start_coaching(self, userA, userB):
		if userA not in self.users or userB not in self.users: return
		userA.add_coachee(userB)
		userB.add_coach(userA)

	def infect(self, user):
		if not user in self.users: return

		user.infect()

	def infect_limited(self, user, limit):
		if not user in self.users: return

