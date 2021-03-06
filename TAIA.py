#python
import requests
import json
from token import AUTH
import math
import os
import pdb, traceback, sys

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
		if type(contri) == type({}):
			acc_weeks = {"a":0,"c":0,"d":0}
			weeks = contri["weeks"]
			for w in weeks:
				acc_weeks["a"] += w["a"]
				acc_weeks["c"] += w["c"]
				acc_weeks["d"] += w["d"]
			contri["weeks"] = acc_weeks
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

count = 0;		

def git_json_request(request):
	global count
	#print(request);

	try:
		count  += 1;
		ret_request = requests.get(request+AUTH);
		return json.loads(ret_request.content);
	except:
		print "error at request number ",count,"\n";
		print "request = ",request,"\n";
		return {};

total_count = 0;
cache_count = 0;
cache_not_count = 0;
cache_last = None;
last_print = 0;

def git_json_cached_request_stauts(cache,print_=True):
	global cache_count;
	global cache_not_count;
	global cache_last;
	global total_count;
	global last_print;

	if type(cache) == type(True):
		cache_last = cache;
		total_count = total_count + 1;
		if cache:
			cache_count = cache_count + 1;
		else:
			cache_not_count = cache_not_count + 1;

	if cache != cache_last or cache == 'print' or (last_print + 100) < total_count:
		last_print = total_count;
		
		if print_ or cache == 'print':
			print '\n---'
			if cache:
				print 'cached'
			else:
				print 'not cached'
			print 'total_count = ', total_count
			print 'cache_not_count = ', cache_not_count
			print 'cache_count = ', cache_count
			print '---\n'

def git_json_cached_request(request):


	directory  = 'cache';

	#garantidno que a pasta cache exist
	if not os.path.exists(directory):
	    os.makedirs(directory);

	#abrindo index de cache
	try:
		f_index = open(directory + '/index.json','r');
		index = json.load(f_index);
   		f_index.close();
	except:
		f_index = None;
		index = {'count':0};
		
	#achando o request (get/cache)
   	if request in index: #cache
   		json_file_path_request = index[request];

   		try :
   			json_file_request = open(json_file_path_request,'r');
   			git_json_cached_request_stauts(True);
   			return json.load(json_file_request);
   		except:
   			json_file_request = None;
   			del index[request];

   	#get (Se else nao tem no dicionario, ou se tem mas nao abre o arquivo)
	git_json_cached_request_stauts(False);
	dict_request = git_json_request(request);

	if not dict_request:
		return dict_request;#se retornou vazio, nao salva no cache!
	
	# if 'contributors' in request:
	# 	dict_request = sum_weeks(dict_request)
	#dando nome ao novo request
	next_id = index['count'];
	index['count'] = next_id + 1;
	file_name = directory + '/' + str(next_id) + '.json';

	#salvando ele na pasta
	f_dict_request = open(file_name,'w');
	json.dump(dict_request,f_dict_request);
	f_dict_request.close();

	#adicionando no index e salvando na pasta
	index[request] = file_name;
	f_index = open(directory + '/index.json','w');
	json.dump(index,f_index);

	return dict_request;


def return_repo_owner_or_starred_list_antiga(user):
	""" retorna duas listas de dicionarios. A primeira sao os repositorios do usuario e a segunda a que ele deu estrela """
	
	repo = git_json_cached_request('https://api.github.com/users/'+user+'/repos');
	starred = git_json_cached_request('https://api.github.com/users/'+user+'/starred');


	list = []

	for i in repo:
		list.append(Repo(i['owner']['login'],i['name']));
	for i in starred:
		list.append(Repo(i['owner']['login'],i['name']));

	return list;

def return_repo_contributors_antiga(user,repo):
	contributors = git_json_cached_request('https://api.github.com/repos/' + user + '/' + repo + '/stats/contributors');
	list_contri = []
	if type(contributors) == type([]):
		for contributor in contributors:
			if contributor.__contains__('author'):
				if type(contributor['author']) == type({}) and contributor['author'].__contains__('login'):
					list_contri.append(contributor['author']['login'])
		return list_contri
	return []

def return_repo_owner_or_starred_list(user):
	""" retorna duas listas de dicionarios. A primeira sao os repositorios do usuario e a segunda a que ele deu estrela """
	
	repo = git_json_cached_request('https://api.github.com/users/'+user+'/repos');
	# starred = git_json_cached_request('https://api.github.com/users/'+user+'/starred');


	list = []

	for i in repo:
		list.append(Repo(i['owner']['login'],i['name']));
	# for i in starred:
	# 	list.append(Repo(i['owner']['login'],i['name']));

	return list;

def return_repo_contributors(user,repo):
	# contributors = git_json_cached_request('https://api.github.com/repos/' + user + '/' + repo + '/stats/contributors');
	contributors = git_json_cached_request('https://api.github.com/repos/' + user + '/' + repo + '/contributors');
	list_contri = []
	if type(contributors) == type([]):
		# print 'entrou if1'
		for contributor in contributors:
			# print 'for'
			list_contri.append(contributor['login'])
			# if contributor.__contains__('author'):
			# 	print 'entrou if2'
			# 	if type(contributor['author']) == type({}) and contributor['author'].__contains__('login'):
			# 		print 'entrou if3'
			# 		list_contri.append(contributor['author']['login'])
		return list_contri
	return []

def explore_repositories(N_iterations,repo_list=[],user_list=[],max_repo_num = float("inf"),max_user_num = float("inf")):
	explored_repositories = set();
	explored_users = set();

	for it in xrange(0,N_iterations):
		print 'it=',it;#DEBUG

		#Se nao tem nem usuarios nem repositorios a explorar, para
		if not user_list and not repo_list:
			break;


		print 'len user_list=',len(user_list);#DEBUG

		#explorando usuarios -> repo
		for i in user_list:
			if i not in explored_users:
				explored_users.add(i);
				
				if len(explored_users) > max_user_num:
					break;

				repo_list += return_repo_owner_or_starred_list(i);

		user_list = [];#todos ja foram explorados

		print 'len explored_users=',len(explored_users);#DEBUG
		print 'len repo_list=',len(repo_list);#DEBUG

		#explorando repo -> usuarios
		for i in repo_list:
			#import pdb; pdb.set_trace();
			if i.__str__() not in explored_repositories:
				explored_repositories.add(i.__str__());
				
				if len(explored_repositories) > max_repo_num:
					break;

				user_list += return_repo_contributors(i.owner,i.repo);
		
		repo_list = []#todos ja foram explorados

		print 'len explored_repositories=',len(explored_repositories),'\n';#DEBUG

		#raw_input('wait');#DEBUG

	return explored_repositories,explored_users


try:
	repo,user = explore_repositories(3,[Repo('nlohmann','json')],[],100,1000);
	
	with open('repo.json','w') as f:
		json.dump(list(repo),f,indent=4);

	with open('user.json','w') as f:
		json.dump(list(user),f,indent=4);
except:
	pass
	type, value, tb = sys.exc_info()
	traceback.print_exc()
	pdb.post_mortem(tb)


print '\n\n';
print "repo",repo;
print "user",user;
git_json_cached_request_stauts('print');
