import os
import shutil
import random
from logger import logger
from coachingGraph import CoachingGraph

NUM_TEST_GRAPHS = 20
TEST_GRAPH_DIRECTORY_NAME = 'testData'
TEST_GRAPH_SUFFIX = 'testGraph.pkl'
MAX_SIZE = 600

NUM_TEST_GRAPHS_QUICK = 12
TEST_GRAPH_DIRECTORY_NAME_QUICK = 'testDataQuick'
TEST_GRAPH_SUFFIX_QUICK = 'testGraph.pkl'
MAX_SIZE_QUICK = 160

def custom_single_use_test_graphs(folderName, numGraphs, maxSize):
	generate_test_graphs(folderName, numGraphs, maxSize)

	return load_test_graphs(folderName)

def default_persistent_test_graphs():
	expectedTestGraphs = NUM_TEST_GRAPHS
	if not check_resources_exist(TEST_GRAPH_DIRECTORY_NAME, expectedTestGraphs):
			logger.info("generating new test graphs")
			generate_test_graphs(TEST_GRAPH_DIRECTORY_NAME, expectedTestGraphs, MAX_SIZE)
	
	return load_test_graphs(TEST_GRAPH_DIRECTORY_NAME)

def quick_persistent_test_graphs():
	expectedTestGraphs = NUM_TEST_GRAPHS_QUICK
	if not check_resources_exist(TEST_GRAPH_DIRECTORY_NAME_QUICK, expectedTestGraphs):
			logger.info("generating new quick test graphs")
			generate_test_graphs(TEST_GRAPH_DIRECTORY_NAME_QUICK, expectedTestGraphs, MAX_SIZE_QUICK)
	
	return load_test_graphs(TEST_GRAPH_DIRECTORY_NAME_QUICK)

def load_test_graphs(folderName):
	testGraphs = []

	dirName = get_test_data_directory(folderName)
	fileNames = get_files_from_directory_with_suffix(dirName, TEST_GRAPH_SUFFIX)
	for file in fileNames:
		fullPath = os.path.join(dirName, file)
		graph = CoachingGraph()
		graph.load_from(fullPath)
		testGraphs.append(graph)
	return testGraphs

def generate_test_graphs(dirName, numGraphs, maxSize):
	logger.info("generating test graphs in directory: {}".format(dirName))
	folderPath = refresh_testData_folder(dirName)

	for i in range(numGraphs):
		graph = CoachingGraph()

		fileNumber = i + 1
		fileName = '{}_'.format(fileNumber) + TEST_GRAPH_SUFFIX

		randomSize = random.randint(40, maxSize)
		randomInternalConnections = random.randint(2, 12)
		randomCoacheesFactor = random.randint(2, 5)
		graph.init_semi_random(randomSize, randomInternalConnections, randomCoacheesFactor)

		filePath = os.path.join(folderPath, fileName)
		graph.save_as(filePath)

def refresh_testData_folder(dirName):
	remove_testData_folder(dirName)
	destinationPath = os.path.join(get_current_directory(), dirName)
	os.mkdir(destinationPath)
	return os.path.join(get_current_directory(), dirName)

def remove_testData_folder(dirName):
	try:
		pathToFolder = get_test_data_directory(dirName)
		logger.info('removing path: {}'.format(pathToFolder))
		shutil.rmtree(pathToFolder)
	except FileNotFoundError as e:
		logger.info('no testData folder to remove: ' + str(e))
	except Exception as e:
		logger.error('failed while removing testData folder: ', str(e))
	

def check_resources_exist(dirName, expectedNumResources):
	try:
		dataPath = get_test_data_directory(dirName)
	except FileNotFoundError as e:
		logger.error('test dir not found:' + str(e))
		return False

	resources = get_files_from_directory_with_suffix(dataPath, TEST_GRAPH_SUFFIX)
	return len(resources) == expectedNumResources

def get_files_from_directory_with_suffix(dirPath, suffix):
	files = [name for name in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, name))]
	files = [file for file in files if file.endswith(suffix)]
	return files

def get_test_data_directory(dirName):
	for path, directory in get_immediate_subdirectories():
		if directory == dirName:
			return os.path.join(path, directory)
	raise FileNotFoundError('No directory found matching name: {} in path {}'.format(dirName, get_current_directory()))

def get_immediate_subdirectories():
	a_dir = get_current_directory()
	return [(a_dir, name) for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

def get_current_directory():
	return os.path.dirname(os.path.realpath(__file__))