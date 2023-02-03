import requests
import json


headers ={
	'Accept': 'application/sparql-results+json'
}
r = requests.get('https://query.semlab.io/proxy/wdqs/bigdata/namespace/wdq/sparql?query=SELECT%20%3Fitem%20%3FitemLabel%20%3Fqid%0AWHERE%0A%7B%0A%20%20%3Fitem%20wdt%3AP1%20wd%3AQ1.%0A%20%20%3Fitem%20wdt%3AP11%20wd%3AQ19104.%0A%20%20%3Fitem%20rdfs%3Alabel%20%3FitemLabel.%20%0A%20%20OPTIONAL%7B%0A%20%20%20%20%3Fitem%20wdt%3AP8%20%3Fqid.%0A%20%20%7D%0A%0A%20%20%23FILTER%20not%20exists%20%7B%20%3Fitem%20wdt%3AP131%20wd%3AQ33788%20%7D%20%23%20excluding%20Koumac%2C%20New%20Caledonia...%0A%0A%20%20%0A%20%20%0A%20%20%0A%7D', headers=headers)

semlab_data = r.json()



all_elements = json.load(open('all_elements_with_qid.json'))

counter = 0
hits = 0
for el in all_elements:

	counter=counter+1
	print(counter,'/',len(all_elements))

	if 'ner' in el:

		for e in el['ner']['entities']:

			if 'qid' in e:

				for item in semlab_data['results']['bindings']:
					if 'qid' in item:
						if e['qid'] == item['qid']['value']:
							hits=hits+1

							e['semlab'] = item['item']['value'].split('/')[-1]
							e['semlabLabel'] = item['itemLabel']['value']
							print(item)



print('hits:',hits)
json.dump(all_elements,open('all_elements_with_semlab_qid.json','w'),indent=2)																		
	