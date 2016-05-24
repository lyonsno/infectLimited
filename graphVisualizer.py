from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt

from coachingGraph import CoachingGraph
from user import User

class GraphVisualizer():

	def __init__(self, graph):
		self.graph = graph
		self.visualGraph = nx.Graph(name="users")

	def process_graph(self):
		for user in self.graph.users:
			# self.visualGraph.add_node(user, color="green")
			for coach in user.coaches:
				if not (user,coach) in self.visualGraph.edges():
					self.visualGraph.add_edge(user, coach, color="red", dir="forward")
			for coachee in user.coachees:
				if not (user,coachee) in self.visualGraph.edges():
					self.visualGraph.add_edge(user, coachee, color="red", dir="forward")

	def draw(self):
		pos = nx.spring_layout(self.visualGraph, scale=10, k=0.1, iterations=90)
		nx.draw(self.visualGraph, pos, node_size=20, with_labels=False)
		plt.show()


g = CoachingGraph()
A = User()
B = User()
C = User()
D = User()
E = User()

g.add_user(A)
g.add_user(B)
g.add_user(C)
g.add_user(D)
g.add_user(E)
g.start_coaching(A, C)
g.start_coaching(B, A)
g.start_coaching(C, D)
g.start_coaching(B, D)
g.start_coaching(E, D)

g.init_semi_random(50)
viz = GraphVisualizer(g)
viz.process_graph()
viz.draw()