import random
import pytest
from user import User
from coachingGraph import CoachingGraph
import graphTraverser
from graphVisualizer import GraphVisualizer
from infecter import Infecter

@pytest.fixture()
def resource_semi_random_graph_users():
	graph = CoachingGraph()
	graph.init_semi_random(200)
	# viz = GraphVisualizer(graph)
	# viz.draw()

	return graph.users

def test_infect_from(resource_semi_random_graph_users):
	users = resource_semi_random_graph_users
	user = random.choice(users)
	infecter = Infecter()

	infecter.infect_from(user)

	subgraphs = graphTraverser.get_subgraphs(users)
	assert exactly_one_subgraph_infected(subgraphs)

def exactly_one_subgraph_infected(subgraphs):
	infectedSubgraphs = [subgraph for subgraph in subgraphs if all_are_infected(subgraph)]

	print(len(infectedSubgraphs))
	return len(infectedSubgraphs) == 1 

def all_are_infected(subgraph):
	for node in subgraph:
		if not node.infected:
			return False
	return True

def test_get_num_infected():
	graph = CoachingGraph()
	A = User()
	B = User()
	C = User()
	graph.add_users([A, B, C])

	A.infected = True
	B.infected = True

	infecter = Infecter()

	assert infecter.get_num_infected(graph.users) == 2

def test_infect_limited(resource_semi_random_graph_users):
	users = resource_semi_random_graph_users
	infecter = Infecter()

	start = random.choice(users)
	infecter.infect_limited_from(start, 25, 3)

	viz = GraphVisualizer(users)
	viz.draw()

	assert abs(infecter.get_num_infected(users) - 25) <= 3


def test_find_neighbor_with_fewest_connections():
	graph = CoachingGraph()
	A = User()
	B = User()
	C = User()
	D = User()
	E = User()
	F = User()
	graph.add_users([A, B, C, D, E, F])

	graph.create_coach_coachee_relationship(A, B)
	graph.create_coach_coachee_relationship(B, C)
	graph.create_coach_coachee_relationship(B, D)
	graph.create_coach_coachee_relationship(C, E)
	graph.create_coach_coachee_relationship(A, F)

	infecter = Infecter()
	infecter.infect_single_user(A)
	userWithFewest = infecter.find_neighbor_with_fewest_connections(A)

	assert userWithFewest == F

@pytest.fixture()
def resource_test_graph():
	subgraph = CoachingGraph()
	A = User()
	B = User()
	C = User()
	D = User()
	E = User()
	F = User()
	G = User()
	H = User()
	I = User()
	J = User()
	K = User()
	L = User()
	subgraph.add_users([A, B, C, D, E, F, G, H, I, J, K, L])
	subgraph.create_coach_coachee_relationship(A, B)
	subgraph.create_coach_coachee_relationship(B, C)
	subgraph.create_coach_coachee_relationship(B, D)
	subgraph.create_coach_coachee_relationship(C, E)
	subgraph.create_coach_coachee_relationship(A, F)
	subgraph.create_coach_coachee_relationship(E, H)
	subgraph.create_coach_coachee_relationship(E, G)
	subgraph.create_coach_coachee_relationship(G, I)
	subgraph.create_coach_coachee_relationship(G, J)
	subgraph.create_coach_coachee_relationship(F, K)
	subgraph.create_coach_coachee_relationship(F, L)

	return subgraph

# def test_get_num_paths_out(resource_test_graph):
# 	subgraph = CoachingGraph()
# 	A = User()
# 	B = User()
# 	C = User()
# 	D = User()
# 	E = User()
# 	F = User()
# 	G = User()
# 	H = User()
# 	I = User()
# 	J = User()
# 	K = User()
# 	L = User()
# 	M = User()
# 	subgraph.add_users([A, B, C, D, E, F, G, H, I, J, K, L, M])
# 	subgraph.create_coach_coachee_relationship(A, B)
# 	subgraph.create_coach_coachee_relationship(B, C)
# 	subgraph.create_coach_coachee_relationship(B, D)
# 	subgraph.create_coach_coachee_relationship(C, E)
# 	subgraph.create_coach_coachee_relationship(A, F)
# 	subgraph.create_coach_coachee_relationship(E, H)
# 	subgraph.create_coach_coachee_relationship(E, G)
# 	subgraph.create_coach_coachee_relationship(G, I)
# 	subgraph.create_coach_coachee_relationship(G, J)
# 	subgraph.create_coach_coachee_relationship(F, K)
# 	subgraph.create_coach_coachee_relationship(F, L)

# 	infecter = Infecter()

# 	numPathsOutC = infecter.get_num_paths_out(C)
# 	numPathsOutF = infecter.get_num_paths_out(F)
# 	numPathsOutM = infecter.get_num_paths_out(M)

# 	assert numPathsOutC == 2
# 	assert numPathsOutF == 1
# 	assert numPathsOutM == 0

# def test_find_most_isolated_hubs():
# 	graph = resource_test_graph
# 	infecter = Infecter()

# 	mostIsolatedHubs = infecter.find_most_isolated_hubs(graph.users)

# 	assert set(tuple(mostIsolatedHubs)) == set(G, F)





