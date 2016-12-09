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
					# print contributors_url
					error +=1
					continue
				projects[repo['url']] = []
				contributors_json = open(index[contributors_url],'r')
				contributors = json.load(contributors_json)
				for contributor in contributors:
					projects[repo['url']].append((contributor['login'],contributor['contributions']))
	# print error

	return projects



def link_prediction(graph_dict,graph,repo):
	users = []
	for tupla in graph_dict[repo]:
		users.append(tupla[0])

	repos = []
	for key in graph_dict:
		if key != repo:
			repos.append(key)

	maybe_contri = []
	contri_list = []
	for repo_p in repos:
		for user in users:
			for contri,cont in graph_dict[repo_p]:
				if contri == user:
					user_stats = max(graph_dict[repo_p],key=operator.itemgetter(1))
					if user_stats[0] not in maybe_contri and user_stats[0] != user:
						maybe_contri.append(user_stats[0])
						contri_list.append(user_stats[1])


	import pdb;pdb.set_trace()

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
print "Contribuidor por contribuicao: " + contributor_by_contributions
print "Contribuiu para mais projetos: " + contributor_by_edge
B = nx.Graph()
B.add_weighted_edges_from(graph_list)
link_prediction(graph_dict,graph_list,'https://api.github.com/repos/nlohmann/json')
X, Y = bipartite.sets(B)
pos = dict()
pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
nx.draw(B, pos=pos, with_labels = True)
plt.show()
# import pdb;pdb.set_trace()