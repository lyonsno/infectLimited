import random
import os
import pytest
from logger import logger
from user import User
from coachingGraph import CoachingGraph
import graphTraverser
from graphVisualizer import GraphVisualizer
from infecter import Infecter

@pytest.fixture()
def resource_semi_random_graph_users():
	graph = CoachingGraph()
	graph.init_semi_random(200)

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

def test_find_user_with_fewest_connections():
	subgraph = CoachingGraph()
	A = User()
	B = User()
	C = User()
	D = User()
	subgraph.add_users([A, B, D, C])
	subgraph.create_coach_coachee_relationship(A, B)
	subgraph.create_coach_coachee_relationship(A, C)
	subgraph.create_coach_coachee_relationship(A, D)
	subgraph.create_coach_coachee_relationship(B, C)
	expected = D
	infecter = Infecter()

	actual = infecter.find_user_with_fewest_connections(subgraph.users)

	assert expected == actual
