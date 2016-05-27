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
def resource_persistent_test_graphs():
	return utils.default_persistent_test_graphs()

@pytest.fixture()
def resource_persistent_quick_test_graphs():
	return utils.quick_persistent_test_graphs()


def infect_and_return_num_bad_edges(graph, numToInfect):
	infecter = Infecter()

	start = random.choice(graph.users)
	infecter.infect_limited_from(start, numToInfect)

	return infecter.get_solution_quality(graph.users)

def run_traversal_algorithm(numToInfect, graphs, iterations):
	numBadEdges = 0
	for i in range(iterations):
		for graph in graphs:
			numBadEdges += graphs(graph, numToInfect)
			graph.clean()
	numBadEdges /= iterations
	avgNumBadEdges = numBadEdges / len(graphs)
	logger.info("avg num users infected: {}".format(avgNumInfected) )
	logger.info("avg number of unmatched users: {}".format(avgNumBadEdges) )
	assert False

def test_traversal_algorithm(resource_persistent_test_graphs, resource_num_test_iterations):
	run_traversal_algorithm(25, resource_persistent_test_graphs, resource_num_test_iterations)
	assert False


def run_algorithm(numToInfect, graphs, iterations):
	numBadEdges = 0
	numInfected = 0
	for i in range(iterations):
		for graph in graphs:
			edges, infected = infect_limmited_return_num_bad_edges(graph, numToInfect)
			numBadEdges += edges
			numInfected += infected
			graph.clean()
	numInfected /= iterations
	numBadEdges /= iterations
	avgNumInfected = numInfected / len(graphs)
	avgNumBadEdges = numBadEdges / len(graphs)
	bestCase = 0
	logger.info("avg num users infected: {}".format(avgNumInfected) )
	logger.info("avg number of unmatched users: {}".format(avgNumBadEdges) )
	return avgNumBadEdges

def infect_limmited_return_num_bad_edges(graph, numToInfect):
	infecter = Infecter()

	infecter.infect_limited(graph.users, numToInfect, 10)
	numInfected = infecter.get_num_infected(graph.users)

	return infecter.get_solution_quality(graph.users), numInfected

# @pytest.mark.skip()
def test_infect_limited_onehundred(resource_persistent_test_graphs, resource_num_test_iterations):
	infection_quality = run_algorithm(100, resource_persistent_test_graphs, resource_num_test_iterations)
	assert False

# @pytest.mark.skip()
def test_infect_limited_fifty(resource_persistent_test_graphs, resource_num_test_iterations):
	infection_quality = run_algorithm(50, resource_persistent_test_graphs, resource_num_test_iterations)
	assert False

# @pytest.mark.skip()
def test_infect_limited_twentyfive(resource_persistent_test_graphs, resource_num_test_iterations):
	infection_quality = run_algorithm(25, resource_persistent_test_graphs, resource_num_test_iterations)
	assert False
