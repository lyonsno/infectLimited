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
	graph.init_semi_random(60)
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








