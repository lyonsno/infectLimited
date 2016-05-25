from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt

from user import User

class GraphVisualizer():

	def __init__(self, users):
		self.users = users
		self.visualGraph = nx.DiGraph(name="users")
		self.pos = None
		self.process_graph()

	def update(self, updatedUsers):
		if set(tuple(updatedUsers)) == set(tuple(self.users)):
			return

		self.users = updatedUsers
		self.process_graph()

	def process_graph(self):
		for user in self.users:
			color = self.get_color(user)
			self.visualGraph.add_node(user, category=color)
			for coach in user.coaches:
				if not (user,coach) in self.visualGraph.edges():
					self.visualGraph.add_edge(user, coach, arrows=False)
			for coachee in user.coachees:
				if not (user,coachee) in self.visualGraph.edges():
					self.visualGraph.add_edge(user, coachee, arrows=True)
		# generate node positions
		self.pos = nx.spring_layout(self.visualGraph, scale=1, k=0.025, iterations=40)

	def get_color(self, user):
		if user.epicenter:
			return 'red'
		elif user.infected:
			return 'green'
		else:
			return 'black'

	def draw(self):

		# draw edges with arrows
		coachEdges = [(n[0], n[1]) for n in self.visualGraph.edges(data=True) if n[2]['arrows'] == True]
		nx.draw_networkx_edges(self.visualGraph, self.pos, edgelist=coachEdges, arrows=True)

		# draw rest of graph
		colorMap = {'green':'#12e8b9', 'black':'black', 'red':'red'}
		nx.draw(self.visualGraph, self.pos, arrows=False, node_color=[colorMap[self.visualGraph.node[node]['category']] for node in self.visualGraph], node_size=30)
		plt.show()


# g = CoachingGraph()
# A = User()
# B = User()
# C = User()
# D = User()
# E = User()

# g.add_user(A)
# g.add_user(B)
# g.add_user(C)
# g.add_user(D)
# g.add_user(E)
# g.start_coaching(A, C)
# g.start_coaching(B, A)
# g.start_coaching(C, D)
# g.start_coaching(B, D)
# g.start_coaching(E, D)

# g.init_semi_random(40)
# g.infect()
# viz = GraphVisualizer(g)
# viz.process_graph()
# viz.draw()