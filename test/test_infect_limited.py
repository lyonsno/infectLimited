import pytest

import random

import utils
from coachingGraph import CoachingGraph
from infecter import Infecter

@pytest.fixture()
def resource_num_test_iterations():
	return 20

@pytest.fixture()
def resource_sample_test_graphs():
	return utils.custom_persistent_test_graphs('sample_test_graphs', 3, 120)

@pytest.fixture()
def resource_persistent_test_graphs():
	return utils.default_persistent_test_graphs()

def test_infect_limited(resource_persistent_test_graphs, resource_num_test_iterations):
	numBadEdges = 0
	for i in range(resource_num_test_iterations):
		for graph in resource_persistent_test_graphs:
			numBadEdges += infect_limmited_return_num_bad_edges(graph, 25)
			graph.clean()
	numBadEdges /= resource_num_test_iterations
	avgNumBadEdges = numBadEdges / len(resource_persistent_test_graphs)
	assert avgNumBadEdges < 1

def infect_limmited_return_num_bad_edges(graph, numToInfect):
	infecter = Infecter()

	infecter.infect_limited(graph.users, numToInfect)

	return len(infecter.get_all_clean_neighbors(graph.users))

def test_infect_limited_traversal_algorithm(resource_persistent_test_graphs, resource_num_test_iterations):
	numBadEdges = 0
	for i in range(resource_num_test_iterations):
		for graph in resource_persistent_test_graphs:
			numBadEdges += infect_and_return_num_bad_edges(graph)
			graph.clean()
	numBadEdges /= resource_num_test_iterations
	avgNumBadEdges = numBadEdges / len(resource_persistent_test_graphs)
	assert avgNumBadEdges < 1

def infect_and_return_num_bad_edges(graph):
	infecter = Infecter()

	start = random.choice(graph.users)
	infecter.infect_limited_from(start, 25, 3)

	return len(infecter.get_all_clean_neighbors(graph.users))

@pytest.mark.skip(reason='only for debug')
def test_show_sample_random_traversal_graphs(resource_sample_test_graphs):
	for graph in resource_sample_test_graphs:
		infecter = Infecter()
		start = random.choice(graph.users)
		infecter.infect_limited_from(start, 25, 3)
		graph.draw()
	assert True

# @pytest.mark.skip(reason='only for debug')
def test_show_sample_infect_limited_graphs(resource_sample_test_graphs):
	for graph in resource_sample_test_graphs:
		infecter = Infecter()
		infecter.infect_limited(graph.users, 25)
		graph.draw()
	assert True