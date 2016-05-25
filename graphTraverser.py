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

def traverse_from_collect_if_avoid_if(node, collectCondition, avoidCondition):
	collectedNodes = []
	markedNodes = []

	seen = Queue()
	seen.put(node)

	while not seen.empty():
		current = seen.get()
		neighbors = current.coaches + current.coachees
		for neighbor in neighbors:
			if not neighbor.visited and not avoidCondition(neighbor):
				neighbor.visited = True
				seen.put(neighbor)
		markedNodes.append(current)
		if collectCondition(current):
			collectedNodes.append(current)

	unmark_nodes(markedNodes)
	return collectedNodes	

def traverse_from_to_depth_collect_if_avoid_if(node, maxDepth, collectCondition, avoidCondition):
	collectedNodes = []
	markedNodes = []
	depth = 0
	pendingDepthIncrease = True
	timeToDepthIncrease = 1
	seen = Queue()
	seen.put(node)

	while not seen.empty():
		current = seen.get()
		timeToDepthIncrease -= 1
		if timeToDepthIncrease == 0:
			depth += 1
			pendingDepthIncrease = True
		if depth == maxDepth:
			break
		neighbors = current.coaches + current.coachees
		for neighbor in neighbors:
			if not neighbor.visited and not avoidCondition(neighbor):
				neighbor.visited = True
				if pendingDepthIncrease:
					timeToDepthIncrease = seen.qsize()
					pendingDepthIncrease = False
				seen.put(neighbor)
		markedNodes.append(current)
		if collectCondition(current):
			collectedNodes.append(current)

	unmark_nodes(markedNodes)
	return collectedNodes	

def unmark_nodes(nodes):
	for node in nodes:
		node.visited = False


