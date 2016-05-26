class User():
	def __init__(self):
		self.coachees = []
		self.coaches = []
		self.neighbors = []
		self.infected = False
		self.visited = False
		self.numConnections = 0
		self.epicenter = False

	def add_coach(self, user):
		self.coaches.append(user)
		self.neighbors.append(user)

	def add_coachee(self, user):
		self.coachees.append(user)
		self.neighbors.append(user)


