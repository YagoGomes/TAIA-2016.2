import os
import json
import networkx as nx
from networkx.algorithms import bipartite
import operator
import matplotlib.pyplot as plt


def most_important_contributors(graph_list):
	contributors_by_contributions = {}
	contributors_by_edge = {}

	for key,contributor,contributions in graph_list:
		if contributor not in contributors_by_contributions:
			contributors_by_contributions[contributor] = contributions
		else:
			contributors_by_contributions[contributor] += contributions

		if contributor not in contributors_by_edge:
			contributors_by_edge[contributor] = 1
		else:
			contributors_by_edge[contributor] += 1

	return max(contributors_by_contributions.iteritems(), key=operator.itemgetter(1))[0], max(contributors_by_edge.iteritems(), key=operator.itemgetter(1))[0]
	

def create_format_graph(index):

	key_words = ['contributors', 'starred','count']
	is_repo = True
	projects = {}

	error = 0

	for key in index:
		for word in key_words:
			if word in key:
				is_repo = False

		if not is_repo:
			is_repo = True
			continue


		repos_json = open(index[key],'r')
		repos = json.load(repos_json)

		for repo in repos:
			if repo['url'] not in projects:
				contributors_url = repo['contributors_url']

				try:
					contributors_json = open(index[contributors_url],'r')
				except KeyError:
					# import pdb;pdb.set_trace()
					print contributors_url
					error +=1
					continue
				projects[repo['url']] = []
				contributors_json = open(index[contributors_url],'r')
				contributors = json.load(contributors_json)
				for contributor in contributors:
					projects[repo['url']].append((contributor['login'],contributor['contributions']))
	print error

	return projects


directory  = 'cache';

#garantidno que a pasta cache exist
if not os.path.exists(directory):
    os.makedirs(directory)

f_index = open(directory + '/index.json','r')
index = json.load(f_index)
f_index.close()

graph_dict = create_format_graph(index)
graph_list = []
for key,lista in graph_dict.iteritems():
	for contributor,contributions in lista:
		graph_list.append((key,contributor,contributions))

contributor_by_contributions, contributor_by_edge = most_important_contributors(graph_list)

B = nx.Graph()
B.add_weighted_edges_from(graph_list)
X, Y = bipartite.sets(B)
pos = dict()
pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
nx.draw(B, pos=pos, with_labels = True)
plt.show()
# import pdb;pdb.set_trace()