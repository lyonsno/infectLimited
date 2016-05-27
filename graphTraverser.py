from queue import *

def get_subgraphs_sorted(nodes):
	subgraphs = get_subgraphs(nodes)
	subgraphs.sort(key=lambda subgraph: len(subgraph))
	return subgraphs

def get_subgraphs(nodes):
	setOfNodes = set(nodes)
	
	subgraphs = []
	while(len(setOfNodes) > 0 ):
		node = setOfNodes.pop()
		nodeNetwork = get_connected_network(node)
		subgraphs.append(nodeNetwork)
		setOfNodes -= set(nodeNetwork)

	return subgraphs

def are_connected(nodeA, nodeB):
	return traverse_from_collect_if(nodeA, lambda node: node == nodeB)

def get_connected_network(node):
	return traverse_from_collect_if(node, lambda node: True)

def breadth_first_apply_function(node, function):
	nodes = []
	seen = Queue()
	seen.put(node)
	while not seen.empty():
		current = seen.get()
		neighbors = current.coaches + current.coachees
		for neighbor in neighbors:
			if not neighbor.visited:
				neighbor.visited = True
				seen.put(neighbor)
		nodes.append(current)
		result = function(current)
		if result is not None:
			return result
	unmark_nodes(nodes)
	return True

def traverse_from_collect_if(node, condition):
	collectedNodes = []
	markedNodes = []

	seen = Queue()
	seen.put(node)

	while not seen.empty():
		current = seen.get()
		neighbors = current.coaches + current.coachees
		for neighbor in neighbors:
			if not neighbor.visited:
				neighbor.visited = True
				seen.put(neighbor)
		markedNodes.append(current)
		if condition(current):
			collectedNodes.append(current)

	unmark_nodes(markedNodes)
	return collectedNodes		

def unmark_nodes(nodes):
	for node in nodes:
		node.visited = False


