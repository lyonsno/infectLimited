from queue import *

def get_subgraphs(nodes):
	setOfNodes = set(nodes)
	
	subgraphs = []
	while(len(setOfNodes) > 0 ):
		node = setOfNodes.pop()
		nodeNetwork = get_connected_network(node)
		subgraphs.append(nodeNetwork)
		print(nodeNetwork)
		setOfNodes -= set(nodeNetwork)

	return subgraphs

def are_connected(nodeA, nodeB):
	areConnected = False
	is_in_graph = get_is_in_graph(nodeB)

	return breadth_first_apply_monad(nodeA, is_in_graph)

def get_is_in_graph(node_to_find):
	def is_in_graph(node):
		if node == node_to_find:
			return True
	return is_in_graph

def get_connected_network(node):
	network = []
	add_to = get_add_to(network)

	breadth_first_apply_monad(node, add_to)

	return network

def get_add_to(list):
	def add_to_network(node):
		list.append(node)
	return add_to_network

def breadth_first_apply_monad(node, monad):
	seen = Queue()
	seen.put(node)
	while not seen.empty():
		current = seen.get()
		neighbors = current.coaches + current.coachees
		for neighbor in neighbors:
			if not neighbor.visited:
				neighbor.visited = True
				seen.put(neighbor)
		result = monad(current)
		if result is not None:
			return result


