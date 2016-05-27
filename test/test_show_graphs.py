import pytest

import random

import utils
from coachingGraph import CoachingGraph
from infecter import Infecter

@pytest.fixture()
def resource_sample_test_graphs():
	return utils.custom_single_use_test_graphs('sample_test_graphs', 5, 200)

@pytest.mark.skip(reason='only for debug')
def test_show_sample_random_traversal_graphs(resource_sample_test_graphs):
	for graph in resource_sample_test_graphs:
		infecter = Infecter()
		start = random.choice(graph.users)
		infecter.infect_limited_from(start, 25)
		graph.draw()
	assert True

# @pytest.mark.skip(reason='only for debug')
def test_show_sample_infect_limited_graphs(resource_sample_test_graphs):
	for graph in resource_sample_test_graphs:
		infecter = Infecter()
		infecter.infect_limited(graph.users, 25, 10)
		graph.draw()
	assert True