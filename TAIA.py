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

def return_repo_owner_or_starred_list(user):
	""" retorna duas listas de dicionarios. A primeira sao os repositorios do usuario e a segunda a que ele deu estrela """
	repo = requests.get('https://api.github.com/users/'+user+'/repos' + AUTH)
	starred = requests.get('https://api.github.com/users/'+user+'/starred' + AUTH)
	return json.loads(repo.content), json.loads(starred.content)

def explore_repositories(N_iterations,repo_lis=[],user_list=[],max_repo_num = math.inf,max_user_num = math.inf):
	explored_repositories = {}
	explored_users = {}

	for it in xrange(0,N_iterations):
		#Se não tem nem usuarios nem repositorios a explorar, para
		if not user_list and not repo_lis
			break;

		#explorando usuarios
		for i in user_list:
			if not explored_users.__contains__(i):
				explored_users[i] = None;
				repo_lis += return_repo(i);
		user_list = [];#todos ja foram explorados

		#explorando repo
		for i in repo_lis:
			if not explored_repositories.__contains__(i.owner) or not explored_repositories[i.owner].__contains__(i.repo):				
				explored_repositories[i.owner][i.repo] = None;
				user_list += return_contri(i.owner,i.repo);
		repo_lis = []#todos ja foram explorados


	return explored_repositories,explored_users

# getGraph(['tetris'])
# repository('nlohmann','json');
# return_repo('nlohmann')
# repository = raw_input('Digite o repositorio')
# request_repository(repository)
