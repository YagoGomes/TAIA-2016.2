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

def return_repo(user):
	""" retorna uma lista de dicionarios dos repositorios do usuario """
	reque = requests.get('https://api.github.com/users/'+user+'/repos' + AUTH)
	return json.loads(reque.content)

def return_starred(user):
	""" retorna uma lista de dicionarios dos repositorios que o usuario deu estrela """
	reque = requests.get('https://api.github.com/users/'+user+'/starred' + AUTH)
	https://github.com/nlohmann?tab=stars
	return json.loads(reque.content)

def return_repo_starred(user):
	""" retorna duas listas de dicionarios. A primeira sao os repositorios do usuario e a segunda a que ele deu estrela """
	repo = requests.get('https://api.github.com/users/'+user+'/repos' + AUTH)
	starred = requests.get('https://api.github.com/users/'+user+'/starred' + AUTH)
	return json.loads(repo.content), json.loads(starred.content)

# getGraph(['tetris'])
# repository('nlohmann','json');
# return_repo('nlohmann')
# repository = raw_input('Digite o repositorio')
# request_repository(repository)
