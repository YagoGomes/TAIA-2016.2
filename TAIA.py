import requests
import json
from token import AUTH

def request_repository(repository):
	reque = requests.get('https://api.github.com/search/repositories?q='+repository)
	if(reque.ok):
		repoItem = json.loads(reque.text or reque.content)
		print 'entrou'
		import pdb;pdb.set_trace()
		for project in repoItem['items']:
			print 'repositorio: ' + project['full_name'],'\n'
			constributors_get = requests.get(project['contributors_url']+AUTH)
			constributors = json.loads(constributors_get.text or constributors_get.content)
			for contributor in constributors:
				print contributor['login'],contributor['contributions']
			print '\n'
	else:
		print 'fuu'
		# print "Django repository created: " + repoItem['created_at']
		


repository = raw_input('Digite o repositorio')
request_repository(repository)