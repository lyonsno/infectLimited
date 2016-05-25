import os
import shutil
import random
import pytest
from logger import logger
from user import User
from coachingGraph import CoachingGraph
import graphTraverser
from graphVisualizer import GraphVisualizer
from infecter import Infecter

NUM_TEST_GRAPHS = 2
TEST_GRAPH_DIRECTORY_NAME = 'testData'
TEST_GRAPH_SUFFIX = 'testGraph.pkl'

@pytest.fixture()
def resource_persistent_test_graphs():
	logger.info("fetching test graph resource")
	expectedTestGraphs = NUM_TEST_GRAPHS
	if not check_resources_exist(expectedTestGraphs):
			logger.info("generating new test graphs")
			generate_test_graphs(expectedTestGraphs)
	
	return load_test_graphs()

def load_test_graphs():
	testGraphs = []

	dirName = get_test_data_directory()
	fileNames = get_files_from_directory_with_suffix(dirName, TEST_GRAPH_SUFFIX)
	for file in fileNames:
		fullPath = os.path.join(dirName, file)
		graph = CoachingGraph()
		logger.info('loading test graph')
		graph.load_from(fullPath)

		testGraphs.append(graph)
		logger.info('drawing test graph')
		graph.draw()
	return testGraphs

def generate_test_graphs(numGraphs):
	folderPath = refresh_testData_folder()

	graph = CoachingGraph()

	for i in range(numGraphs):
		fileNumber = i + 1
		fileName = '{}_'.format(fileNumber) + TEST_GRAPH_SUFFIX

		randomSize = random.randint(10, 200)
		graph.init_semi_random(randomSize)

		filePath = os.path.join(folderPath, fileName)
		graph.save_as(filePath)

def refresh_testData_folder():
	remove_testData_folder()
	os.mkdir(TEST_GRAPH_DIRECTORY_NAME)
	return os.path.join(get_current_directory(), TEST_GRAPH_DIRECTORY_NAME)

def remove_testData_folder():
	try:
		pathToFolder = get_test_data_directory()
		logger.info('removing path: {}'.format(pathToFolder))
		shutil.rmtree(pathToFolder)
	except FileNotFoundError as e:
		logger.info('no testData folder to remove: ' + str(e))
	except Exception as e:
		logger.error('failed while removing testData folder: ', str(e))
	

def check_resources_exist(expectedNumResources):
	try:
		dataPath = get_test_data_directory()
	except FileNotFoundError as e:
		logger.error('test dir not found:' + str(e))
		return False

	resources = get_files_from_directory_with_suffix(dataPath, TEST_GRAPH_SUFFIX)
	return len(resources) == expectedNumResources

def get_files_from_directory_with_suffix(dirPath, suffix):
	files = [name for name in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, name))]
	files = [file for file in files if file.endswith(suffix)]
	return files

def get_test_data_directory():
	for path, directory in get_immediate_subdirectories():
		if directory == TEST_GRAPH_DIRECTORY_NAME:
			return os.path.join(path, directory)
	raise FileNotFoundError('No directory found matching name: {}'.format(TEST_GRAPH_DIRECTORY_NAME))

def get_immediate_subdirectories():
	a_dir = get_current_directory()
	return [(a_dir, name) for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

def get_current_directory():
	return os.path.dirname(os.path.realpath(__file__))

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

def test_infect_limited(resource_persistent_test_graphs):
	for graph in resource_persistent_test_graphs:
		assert get_performance_infect_limited(graph) > 0

def get_performance_infect_limited(graph):
	infecter = Infecter()

	start = random.choice(graph.users)
	infecter.infect_limited_from(start, 25, 3)
	graph.draw()


	return infecter.get_num_infected(graph.users)

def test_get_all_clean_neighbors():
	infecter = Infecter()
	graph = CoachingGraph()
	A = User()
	B = User()
	C = User()
	D = User()
	E = User()
	F = User()
	graph.add_users([A, B, C, D, E])
	graph.create_coach_coachee_relationship(A, B)
	graph.create_coach_coachee_relationship(B, C)
	graph.create_coach_coachee_relationship(B, D)
	graph.create_coach_coachee_relationship(D, E)
	graph.create_coach_coachee_relationship(F, C)
	B.infected = True
	D.infected = True

	cleanNeighbors = infecter.get_all_clean_neighbors(graph.users)

	assert set([A, C, E, F]) == cleanNeighbors


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





