import pytest
from user import User
from coachingGraph import CoachingGraph

def test_add_students():
	graph = CoachingGraph()
	A = User()
	graph.add_user(A)

	graph.add_coachees(A, 10)

	assert len(A.coachees) == 10
	
def test_random_graph():
	graph = CoachingGraph()
	graph.init_random(20)

	assert len(graph.users) == 20

def test_add_user():
	graph = CoachingGraph()
	userA = User()

	graph.add_user(userA)

	assert userA in graph.users

def test_infect():
	graph = CoachingGraph()
	userA = User()

	graph.add_user(userA)	
	graph.infect(userA)

	assert userA.infected

@pytest.fixture()
def resource_start_coaching():
	graph = CoachingGraph()
	A = User()
	B = User()
	graph.add_user(A)
	graph.add_user(B)

	graph.start_coaching(A, B)
	return A,B

def test_start_coaching_adds_coachee(resource_start_coaching):
	A,B = resource_start_coaching
	assert B in A.coachees 

def test_start_coaching_adds_coach(resource_start_coaching):
	A,B = resource_start_coaching
	assert A in B.coaches

def test_start_coaching_doesnt_add_coachee(resource_start_coaching):
	A,B = resource_start_coaching
	assert B not in A.coaches

def test_start_coaching_doesnt_add_coach(resource_start_coaching):
	A,B = resource_start_coaching
	assert A not in B.coachees


def test_limited_infection():
	graph = CoachingGraph()
	A = User()
	B = User()
	C = User()
	D = User()

	graph.add_user(A)
	graph.add_user(B)
	graph.add_user(C)
	graph.add_user(D)

	A.add_coach(B)
	B.add_coach(C)
	A.add_coach(D)
	graph.infect_limited(A, 2)

	num_infected = 0
	for user in graph.users:
		if user.infected:
			num_infected += 1

	assert num_infected == 2



