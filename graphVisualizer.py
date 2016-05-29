from operator import itemgetter
import networkx as nx
from logger import logger
import matplotlib.pyplot as plt

from user import User

class GraphVisualizer():

	def __init__(self, users):
		self.users = users
		self.visualGraph = nx.DiGraph(name="users")
		self.pos = None
		self.process_graph()
		self.numInfected = 0
		self.numNodes = 0

	def update(self, updatedUsers):
		if set(tuple(updatedUsers)) == set(tuple(self.users)):
			self.update_nodes()
			return
		logger.debug("updating visualizer: {} old users replaced with {} new users".format(len(self.users), len(updatedUsers)))
		self.users = updatedUsers
		self.process_graph()

	def update_nodes(self):
		self.numNodes = 0
		self.numInfected = 0
		for user in self.users:
			self.numNodes += 1
			color = self.get_color(user)
			self.visualGraph.add_node(user, category=color)
			for coach in user.coaches:
				if not (user,coach) in self.visualGraph.edges():
					self.visualGraph.add_edge(user, coach, arrows=False)
			for coachee in user.coachees:
				if not (user,coachee) in self.visualGraph.edges():
					self.visualGraph.add_edge(user, coachee, arrows=True)

	def process_graph(self):
		# add nodes to graph and set their colors
		self.update_nodes()
		# generate node positions
		self.pos = nx.spring_layout(self.visualGraph, scale=1, k=0.025, iterations=40)

	def get_color(self, user):
		self.numInfected += 1
		if user.epicenter:
			return 'red'
		elif user.infected:
			return 'green'
		else:
			self.numInfected -= 1
			return 'black'

	def draw(self, numUnmatched):

		# draw edges with arrows
		coachEdges = [(n[0], n[1]) for n in self.visualGraph.edges(data=True) if n[2]['arrows'] == True]
		nx.draw_networkx_edges(self.visualGraph, self.pos, edgelist=coachEdges, arrows=True)

		# draw rest of graph
		colorMap = {'green':'#12e8b9', 'black':'black', 'red':'red'}
		nx.draw(self.visualGraph, self.pos, arrows=False, node_color=[colorMap[self.visualGraph.node[node]['category']] for node in self.visualGraph], node_size=30)

		# place a text box in upper left in axes coords
		textstr = self.get_txt_string(numUnmatched)

		plt.figtext(0.02, 0.98, textstr, fontsize=14, verticalalignment='top')

		plt.show()

	def get_txt_string(self, numUnmatched):
		string = ""
		string += "{} users in graph\n".format(self.numNodes)
		string += "{} users infected\n".format(self.numInfected)
		string += "{} connections between infected users and other users".format(numUnmatched)
		return string
