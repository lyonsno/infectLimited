import pytest

import random

import utils
from coachingGraph import CoachingGraph
from infecter import Infecter

@pytest.fixture()
def resource_sample_test_graphs():
	return utils.custom_single_use_test_graphs('sample_test_graphs', 10, 200)

# @pytest.mark.skip(reason='only for debug')
def test_show_sample_infect_limited_graphs(resource_sample_test_graphs):
	for graph in resource_sample_test_graphs:
		infecter = Infecter()
		infecter.infect_limited(graph.users, 30, 10)
		graph.draw()
	assert True