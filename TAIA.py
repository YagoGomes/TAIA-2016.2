#python
import requests
import json
from token import AUTH
import math

def request_repository(repository):
	reque = requests.get('https://api.github.com/search/repositories?q='+repository)
	if(reque.ok):
		repoItem = json.loads(reque.text or reque.content)
		for project in repoItem['items']:
			print 'repositorio: ' + project['full_name'],'\n'
			constributors_get = requests.get(project['contributors_url']+AUTH)
			if constributors_get.text:
				constributors = json.loads(constributors_get.text or constributors_get.content)
				for contributor in constributors:
					print contributor['login'],contributor['contributions']
				print '\n'
	else:
		print 'ERROR invalid token'
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


def return_contri(owner,repo):
	""" recebe um usuario e um repositorio e retorna os contribuidores desse repositorio """
#	link = 'https://api.github.com/repos/' + owner + '/' + repo + AUTH;
#	print(link);
	#reque = requests.get('https://api.github.com/repos/' + owner + '/' + repo + AUTH)
	#reque = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/commits' + AUTH)
	#reque = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/contributors' + AUTH)
	reque = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/stats/contributors' + AUTH)
	if reque.ok:
		repoItem = json.loads(reque.text)
		sum_weeks(repoItem)
	return repoItem

def return_repo_owner(user):
	""" retorna uma lista de dicionarios dos repositorios do usuario """
	reque = requests.get('https://api.github.com/users/'+user+'/repos' + AUTH)
	return json.loads(reque.content)

def return_repo_starred(user):
	""" retorna uma lista de dicionarios dos repositorios que o usuario deu estrela """
	reque = requests.get('https://api.github.com/users/'+user+'/starred' + AUTH)
	return json.loads(reque.content)

class Repo:
	def __init__(self):
		self.owner = "";
		self.repo = "";
	def __init__(self,owner,repo):
		self.owner = owner;
		self.repo = repo;
	def __str__(self):
		return self.owner + '/' + self.repo;
	def __repr__(self):
		return self.owner + '/' + self.repo;

		

def return_repo_owner_or_starred_list(user):
	""" retorna duas listas de dicionarios. A primeira sao os repositorios do usuario e a segunda a que ele deu estrela """
	repo = json.loads(requests.get('https://api.github.com/users/'+user+'/repos' + AUTH).content);
	starred = json.loads(requests.get('https://api.github.com/users/'+user+'/starred' + AUTH).content);
	list = []

	for i in repo:
		list.append(Repo(i['owner']['login'],i['name']));
	for i in starred:
		list.append(Repo(i['owner']['login'],i['name']));

	return list;

def return_repo_contributors(user,repo):
	contributors = json.loads(requests.get('https://api.github.com/repos/' + user + '/' + repo + '/stats/contributors' + AUTH).content)
	list_contri = []
	for contributor in contributors:
		list_contri.append(contributor['author']['login'])
	return list_contri

def explore_repositories(N_iterations,repo_list=[],user_list=[],max_repo_num = float("inf"),max_user_num = float("inf")):
	explored_repositories = {}
	explored_users = {}

	for it in xrange(0,N_iterations):
		#Se nao tem nem usuarios nem repositorios a explorar, para
		if not user_list and not repo_list:
			break;

		#explorando usuarios
		for i in user_list:
			if not explored_users.__contains__(i):
				explored_users[i] = None;
				
				if len(explored_users) > max_user_num:
					return explored_repositories,explored_users 
				
				repo_list += return_repo_owner_or_starred_list(i);

		user_list = [];#todos ja foram explorados

		#explorando repo
		for i in repo_list:
			if not explored_repositories.__contains__(i.__str__())
				explored_repositories[i.__str__()] = None;
				if len(explored_repositories) > max_repo_num:
					return explored_repositories,explored_users 

				user_list += return_contri(i.owner,i.repo);
		repo_list = []#todos ja foram explorados


	return explored_repositories,explored_users

# getGraph(['tetris'])
# repository('nlohmann','json');
# return_repo('nlohmann')
# repository = raw_input('Digite o repositorio')
# request_repository(repository)
return_repo_contributors('nlohmann','json')
