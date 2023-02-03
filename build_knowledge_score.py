import requests
import json




headers ={
	'Accept': 'application/sparql-results+json'
}
r = requests.get('https://query.semlab.io/proxy/wdqs/bigdata/namespace/wdq/sparql?query=SELECT%20%3Fitem%20%3FitemLabel%20%3Fqid%0AWHERE%0A%7B%0A%20%20%3Fitem%20wdt%3AP1%20wd%3AQ1.%0A%20%20%3Fitem%20wdt%3AP11%20wd%3AQ19104.%0A%20%20%3Fitem%20rdfs%3Alabel%20%3FitemLabel.%20%0A%20%20OPTIONAL%7B%0A%20%20%20%20%3Fitem%20wdt%3AP8%20%3Fqid.%0A%20%20%7D%0A%0A%20%20%23FILTER%20not%20exists%20%7B%20%3Fitem%20wdt%3AP131%20wd%3AQ33788%20%7D%20%23%20excluding%20Koumac%2C%20New%20Caledonia...%0A%0A%20%20%0A%20%20%0A%20%20%0A%7D', headers=headers)
knowledge_score = {}
try:
	knowledge_score = json.load(open('knowledge_score.json'))
except:
	pass

semlab_data = r.json()

for item in semlab_data['results']['bindings']:


		
	qid = item['item']['value'].split('/')[-1]
	label = item['itemLabel']['value']

	if qid in knowledge_score:
		continue
	url = f"https://query.semlab.io/proxy/wdqs/bigdata/namespace/wdq/sparql?query=%0ASELECT%20(count(%3Fblock)%20as%20%3Fcount)%0AWHERE%0A%7B%0A%20%20%3Fblock%20wdt%3AP21%20wd%3A{qid}.%20%20%0A%7D%0A%0A"


	headers ={
		'Accept': 'application/sparql-results+json'
	}
	r2 = requests.get(url, headers=headers)

	count_data = r2.json()
		
	print(qid,label)
	print(count_data['results']['bindings'][0]['count']['value'])

	knowledge_score[qid] = {'label':label,'count':int(count_data['results']['bindings'][0]['count']['value'])}	

	json.dump(knowledge_score,open('knowledge_score.json','w'),indent=2)