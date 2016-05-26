import pytest

import random

import utils
from coachingGraph import CoachingGraph
from infecter import Infecter
from logger import logger

@pytest.fixture()
def resource_num_test_iterations():
	return 20

@pytest.fixture()
def resource_sample_test_graphs():
	return utils.custom_single_use_graphs('sample_test_graphs', 5, 200)

@pytest.fixture()
def resource_persistent_test_graphs():
	return utils.default_persistent_test_graphs()

@pytest.fixture()
def resource_persistent_quick_test_graphs():
	return utils.quick_persistent_test_graphs()


def test_infect_limited_onehundred_quick(resource_persistent_quick_test_graphs, resource_num_test_iterations):
	numBadEdges = 0
	numInfected = 0
	for i in range(resource_num_test_iterations):
		for graph in resource_persistent_quick_test_graphs:
			edges, infected = infect_limmited_return_num_bad_edges(graph, 100)
			numBadEdges += edges
			numInfected += infected
			graph.clean()
	numInfected /= resource_num_test_iterations
	numBadEdges /= resource_num_test_iterations
	avgNumInfected = numInfected / len(resource_persistent_quick_test_graphs)
	avgNumBadEdges = numBadEdges / len(resource_persistent_quick_test_graphs)
	bestCase = 0
	logger.info("avg num users infected: {}".format(avgNumInfected) )
	logger.info("avg number of unmatched users: {}".format(avgNumBadEdges) )
	assert avgNumBadEdges == bestCase

def test_infect_limited_fifty_quick(resource_persistent_quick_test_graphs, resource_num_test_iterations):
	numBadEdges = 0
	numInfected = 0
	for i in range(resource_num_test_iterations):
		for graph in resource_persistent_quick_test_graphs:
			edges, infected = infect_limmited_return_num_bad_edges(graph, 50)
			numBadEdges += edges
			numInfected += infected
			graph.clean()
	numInfected /= resource_num_test_iterations
	numBadEdges /= resource_num_test_iterations
	avgNumInfected = numInfected / len(resource_persistent_quick_test_graphs)
	avgNumBadEdges = numBadEdges / len(resource_persistent_quick_test_graphs)
	bestCase = 0
	logger.info("avg num users infected: {}".format(avgNumInfected) )
	logger.info("avg number of unmatched users: {}".format(avgNumBadEdges) )
	assert avgNumBadEdges == bestCase

def test_infect_limited_twentyfive_quick(resource_persistent_quick_test_graphs, resource_num_test_iterations):
	numBadEdges = 0
	numInfected = 0
	for i in range(resource_num_test_iterations):
		for graph in resource_persistent_quick_test_graphs:
			edges, infected = infect_limmited_return_num_bad_edges(graph, 25)
			numBadEdges += edges
			numInfected += infected
			graph.clean()
	numInfected /= resource_num_test_iterations
	numBadEdges /= resource_num_test_iterations
	avgNumInfected = numInfected / len(resource_persistent_quick_test_graphs)
	avgNumBadEdges = numBadEdges / len(resource_persistent_quick_test_graphs)
	bestCase = 0
	logger.info("avg num users infected: {}".format(avgNumInfected) )
	logger.info("avg number of unmatched users: {}".format(avgNumBadEdges) )
	assert avgNumBadEdges == bestCase

@pytest.mark.skip()
def test_infect_limited_onehundred(resource_persistent_test_graphs, resource_num_test_iterations):
	numBadEdges = 0
	numInfected = 0
	for i in range(resource_num_test_iterations):
		for graph in resource_persistent_test_graphs:
			edges, infected = infect_limmited_return_num_bad_edges(graph, 100)
			numBadEdges += edges
			numInfected += infected
			graph.clean()
	numInfected /= resource_num_test_iterations
	numBadEdges /= resource_num_test_iterations
	avgNumInfected = numInfected / len(resource_persistent_test_graphs)
	avgNumBadEdges = numBadEdges / len(resource_persistent_test_graphs)
	bestCase = 0
	logger.info("avg num users infected: {}".format(avgNumInfected) )
	logger.info("avg number of unmatched users: {}".format(avgNumBadEdges) )
	assert avgNumBadEdges == bestCase

@pytest.mark.skip()
def test_infect_limited_fifty(resource_persistent_test_graphs, resource_num_test_iterations):
	numBadEdges = 0
	numInfected = 0
	for i in range(resource_num_test_iterations):
		for graph in resource_persistent_test_graphs:
			edges, infected = infect_limmited_return_num_bad_edges(graph, 50)
			numBadEdges += edges
			numInfected += infected
			graph.clean()
	numInfected /= resource_num_test_iterations
	numBadEdges /= resource_num_test_iterations
	avgNumInfected = numInfected / len(resource_persistent_test_graphs)
	avgNumBadEdges = numBadEdges / len(resource_persistent_test_graphs)
	bestCase = 0
	logger.info("avg num users infected: {}".format(avgNumInfected) )
	logger.info("avg number of unmatched users: {}".format(avgNumBadEdges) )
	assert avgNumBadEdges == bestCase

@pytest.mark.skip()
def test_infect_limited_twentyfive(resource_persistent_test_graphs, resource_num_test_iterations):
	numBadEdges = 0
	numInfected = 0
	for i in range(resource_num_test_iterations):
		for graph in resource_persistent_test_graphs:
			edges, infected = infect_limmited_return_num_bad_edges(graph, 25)
			numBadEdges += edges
			numInfected += infected
			graph.clean()
	numInfected /= resource_num_test_iterations
	numBadEdges /= resource_num_test_iterations
	avgNumInfected = numInfected / len(resource_persistent_test_graphs)
	avgNumBadEdges = numBadEdges / len(resource_persistent_test_graphs)
	bestCase = 0
	logger.info("avg num users infected: {}".format(avgNumInfected) )
	logger.info("avg number of unmatched users: {}".format(avgNumBadEdges) )
	assert avgNumBadEdges == bestCase

def infect_limmited_return_num_bad_edges(graph, numToInfect):
	infecter = Infecter()

	infecter.infect_limited(graph.users, numToInfect, 10)
	numInfected = infecter.get_num_infected(graph.users)

	return infecter.get_solution_quality(graph.users), numInfected

@pytest.mark.xfail()
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
	infecter.infect_limited_from(start, 25)

	return infecter.get_solution_quality(graph.users)

@pytest.mark.skip(reason='only for debug')
def test_show_sample_random_traversal_graphs(resource_sample_test_graphs):
	for graph in resource_sample_test_graphs:
		infecter = Infecter()
		start = random.choice(graph.users)
		infecter.infect_limited_from(start, 25)
		graph.draw()
	assert True

@pytest.mark.skip(reason='only for debug')
def test_show_sample_infect_limited_graphs(resource_sample_test_graphs):
	for graph in resource_sample_test_graphs:
		infecter = Infecter()
		infecter.infect_limited(graph.users, 25, 10)
		graph.draw()
	assert True