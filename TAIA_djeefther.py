#python
import requests
import json
from token import AUTH

def request_repository(repository):
	reque = requests.get('https://api.github.com/search/repositories?q='+repository)
	if(reque.ok):
		repoItem = json.loads(reque.text or reque.content)
		for project in repoItem['items']:
			print 'repositorio: ' + project['full_name'],'\n'
			constributors_get = requests.get(project['contributors_url']+AUTH)
			if constributors_get.text:
				constributors = json.loads(constributors_get.text or constributors_get.content)
				import pdb;pdb.set_trace()
				# for contributor in constributors:
				# 	print contributor['login'],contributor['contributions']
				# print '\n'
	else:
		print 'fuu'
		# print "Django repository created: " + repoItem['created_at']
	

def sum_weeks(repoItem_list_contr):
	for contri in repoItem_list_contr:
		acc_weeks = {"a":0,"c":0,"d":0}
		weeks = contri["weeks"]
		for w in weeks:
			acc_weeks["a"] += w["a"]
			acc_weeks["c"] += w["c"]
			acc_weeks["d"] += w["d"]
		contri["weeks"] = acc_weeks;
	return 	repoItem_list_contr;

def getting_better_contributors(repoItem):
	list_contri = [] 
	for contri in repoItem:
		list_contri.append((contri['author']['login'],contri['author']['url'],contri['weeks']['a'] + contri['weeks']['d']))
	list_sorted = sorted(list_contri, key=lambda tup: tup[2], reverse=True)
	return list_sorted[:2]

def repository(owner,repo):
#	link = 'https://api.github.com/repos/' + owner + '/' + repo + AUTH;
#	print(link);
	#reque = requests.get('https://api.github.com/repos/' + owner + '/' + repo + AUTH)
	#reque = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/commits' + AUTH)
	#reque = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/contributors' + AUTH)
	dict_data = {}

	while 1:
		reque = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/stats/contributors' + AUTH)
		if reque.ok:
			repoItem = json.loads(reque.text);
			import pdb;pdb.set_trace()
			sum_weeks(repoItem);
			dict_data[owner+'/'+repo] = getting_better_contributors(repoItem)
			print(repoItem);
			print(json.dumps(repoItem,indent=4,sort_keys=True));

			#print(type(repoItem));
			#print(repoItem);	
		else:
			print('fail');

def getGraph(repo_list):
	for repo in repo_list:
		reque = requests.get('https://api.github.com/search/repositories?q='+repo)

# getGraph(['tetris'])
repository('nlohmann','json');
# repository = raw_input('Digite o repositorio')
# request_repository(repository)
