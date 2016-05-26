import pytest

from graphVisualizer import GraphVisualizer
from user import User
from coachingGraph import CoachingGraph
import graphTraverser

@pytest.fixture()
def resource_user_and_subgraph_list():
	graph = CoachingGraph()
	A = User()
	B = User()
	C = User()
	D = User()
	E = User()

	F = User()
	coachee1 = User()
	coachee2 = User()
	coachee3 = User()
	coachee4 = User()

	G = User()
	H = User()
	I = User()
	J = User()
	K = User()

	graph.add_users([A, B, C, D, E, F, coachee1, coachee2, coachee3, coachee4, G, H, I, J, K])
	graph.create_coach_coachee_relationship(A, B)
	graph.create_coach_coachee_relationship(B, C)
	graph.create_coach_coachee_relationship(C, A)
	graph.create_coach_coachee_relationship(C, D)
	graph.create_coach_coachee_relationship(D, E)
	subgraph1 = [A, B, C, D, E]

	graph.create_coach_coachee_relationship(F, coachee1)
	graph.create_coach_coachee_relationship(F, coachee2)
	graph.create_coach_coachee_relationship(F, coachee3)
	graph.create_coach_coachee_relationship(F, coachee4)
	subgraph2 = [F, coachee1, coachee2, coachee3, coachee4]

	graph.create_coach_coachee_relationship(G, H)
	graph.create_coach_coachee_relationship(H, I)
	graph.create_coach_coachee_relationship(I, G)
	graph.create_coach_coachee_relationship(J, G)
	graph.create_coach_coachee_relationship(J, I)
	graph.create_coach_coachee_relationship(K, G)
	graph.create_coach_coachee_relationship(K, H)
	subgraph3 = [G, H, I, J, K]	

	return graph.users, [subgraph1, subgraph2, subgraph3]

def test_get_subgraphs(resource_user_and_subgraph_list):
	graph, controlSubgraphs = resource_user_and_subgraph_list

	controlSubgraphSets = tuple([frozenset(subgraph) for subgraph in controlSubgraphs])

	test_subgraphs = graphTraverser.get_subgraphs(graph)
	testSubgraphSets = tuple([frozenset(subgraph) for subgraph in test_subgraphs])


	assert set(controlSubgraphSets) == set(testSubgraphSets)

def test_are_connected(resource_user_and_subgraph_list):
	graph, subgraphs = resource_user_and_subgraph_list
	subgraph = set(tuple(list(subgraphs[0])))
	userA = subgraph.pop()
	userB = subgraph.pop()

	assert(graphTraverser.are_connected(userA, userB))


def test_get_connected_network():
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
	graph.create_coach_coachee_relationship(C, A)
	graph.create_coach_coachee_relationship(C, D)
	graph.create_coach_coachee_relationship(D, E)


	network = graphTraverser.get_connected_network(A)

	assert set(network) == set([A, B, C, D, E])




