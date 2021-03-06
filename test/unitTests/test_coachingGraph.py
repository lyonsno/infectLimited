import pytest
from user import User
from coachingGraph import CoachingGraph
import graphTraverser

def test_semi_random_graph():
	graph = CoachingGraph()
	graph.init_semi_random(20)

	assert len(graph.users) == 20

def test_add_students():
	graph = CoachingGraph()
	A = User()
	graph.add_user(A)

	graph.add_coachees(A, 10)

	assert len(A.coachees) == 10

@pytest.fixture()
def resource_add_coach():
	graph = CoachingGraph()

	graph.add_coach(20)
	
	coaches = [user for user in graph.users if len(user.coachees) > 0]
	coachees = [user for user in graph.users if len(user.coaches) > 0]
	return coaches, coachees

def test_add_coach_creates_proper_number_of_coaches_and_coachees(resource_add_coach):
	coaches, coachees = resource_add_coach

	assert len(coaches) == 1	
	assert len(coachees) == 20

def test_add_coach_creates_proper_coach_relationships(resource_add_coach):
	coaches, coachees = resource_add_coach
	coach = coaches[0]

	for coachee in coachees:
		assert coachee in coach.coachees
		assert coach in coachee.coaches

def test_add_coach_creates_no_extra_relationships(resource_add_coach):
	coaches, coachees = resource_add_coach
	coach = coaches[0]

	assert len(coach.coaches) == 0

	for coachee in coachees:
		assert len(coachee.coachees) == 0

def test_init_semi_random_connected():
	graph = CoachingGraph()
	graph.init_semi_random_connected(200)
	numSubgraphs = len(graphTraverser.get_subgraphs(graph.users))

	assert numSubgraphs == 1

def test_make_sparse_random_connections():
	graph = CoachingGraph()
	graph.create_and_add_users(20)
	graph.make_sparse_random_connections(5)

	numConnections = 0
	for user in graph.users:
		numConnections += len(user.coaches)
	assert numConnections == 5

def test_random_graph():
	graph = CoachingGraph()
	graph.init_random(20)

	assert len(graph.users) == 20

def test_add_user():
	graph = CoachingGraph()
	userA = User()

	graph.add_user(userA)

	assert userA in graph.users

def test_no_user_has_self_as_neighbor():
	graph = CoachingGraph()
	graph.init_semi_random(100)
	for user in graph.users:
		if user in user.neighbors:
			assert False
	assert True

def test_get_subgraphs():
	graph = CoachingGraph()
	A = User()
	B = User()	
	C = User()
	D = User()
	E = User()
	F = User()
	graph.add_users([A, B, C, D, E, F])
	graph.create_coach_coachee_relationship(A, B)
	graph.create_coach_coachee_relationship(C, D)
	graph.create_coach_coachee_relationship(D, E)
	
	subgraphs = graphTraverser.get_subgraphs(graph.users)
	subgraphs = set(tuple([frozenset(tuple(subgraph)) for subgraph in subgraphs]))

	assert frozenset(tuple([A, B])) in subgraphs
	assert frozenset(tuple([C, D, E])) in subgraphs
	assert frozenset(tuple([F])) in subgraphs

@pytest.fixture()
def resource_create_coach_coachee_relationship():
	graph = CoachingGraph()
	A = User()
	B = User()
	graph.add_user(A)
	graph.add_user(B)

	graph.create_coach_coachee_relationship(A, B)
	return A,B

def test_create_coach_coachee_relationship_adds_correct_coachee(resource_create_coach_coachee_relationship):
	A,B = resource_create_coach_coachee_relationship
	assert B in A.coachees 

def test_create_coach_coachee_relationship_adds_correct_coach(resource_create_coach_coachee_relationship):
	A,B = resource_create_coach_coachee_relationship
	assert A in B.coaches

def test_create_coach_coachee_relationship_doesnt_add_wrong_coachee(resource_create_coach_coachee_relationship):
	A,B = resource_create_coach_coachee_relationship
	assert B not in A.coaches

def test_create_coach_coachee_relationship_doesnt_add_wrong_coach(resource_create_coach_coachee_relationship):
	A,B = resource_create_coach_coachee_relationship
	assert A not in B.coachees

def test_save_and_load():
	graph = CoachingGraph()
	graph.init_semi_random(100)
	graph.save_as('save_and_load')
	graphB = CoachingGraph()
	graphB.load_from('save_and_load')

	assert len(graph.users) == len(graphB.users)


