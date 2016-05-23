class User():
	def __init__(self):
		self.coachees = []
		self.coaches = []
		self.infected = False

	def add_coach(self, user):
		self.coaches.append(user)

	def has_coach(self, coach):
		return coach in self.coaches

	def add_coachee(self, user):
		self.coachees.append(user)

	def has_coachee(self, coachee):
		return coachee in self.coachees

	def infect(self):
		if self.infected: return
		self.infected = True
		self.infect_coachees()
		self.infect_coaches()

	def infect_coachees(self):
		for coachee in self.coachees:
			coachee.infect()

	def infect_coaches(self):
		for coach in self.coaches:
			coach.infect()

