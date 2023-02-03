import requests
import json
from fold_to_ascii import fold



headers ={
	'Accept': 'application/sparql-results+json'
}
r = requests.get('https://query.semlab.io/proxy/wdqs/bigdata/namespace/wdq/sparql?query=SELECT%20%3Fitem%20%3FitemLabel%20%3Fqid%0AWHERE%0A%7B%0A%20%20%3Fitem%20wdt%3AP1%20wd%3AQ1.%0A%20%20%3Fitem%20wdt%3AP11%20wd%3AQ19104.%0A%20%20%3Fitem%20rdfs%3Alabel%20%3FitemLabel.%20%0A%20%20OPTIONAL%7B%0A%20%20%20%20%3Fitem%20wdt%3AP8%20%3Fqid.%0A%20%20%7D%0A%0A%20%20%23FILTER%20not%20exists%20%7B%20%3Fitem%20wdt%3AP131%20wd%3AQ33788%20%7D%20%23%20excluding%20Koumac%2C%20New%20Caledonia...%0A%0A%20%20%0A%20%20%0A%20%20%0A%7D', headers=headers)

semlab_data = r.json()
semlabl_labels = {}

for item in semlab_data['results']['bindings']:

	parts = item['itemLabel']['value'].split()
	useparts = []
	for p in parts:
		if len(p) > 3:
			useparts.append(p)

	if len(useparts) == 0:
		continue

	lookfor = fold(useparts[-1].lower())

	semlabl_labels[item['item']['value'].split('/')[-1]] = {
		'label': fold(item['itemLabel']['value']).lower(),
		'last_part': lookfor,
		'orginal': item['itemLabel']['value'],
		'qid': item['item']['value'].split('/')[-1]

	}



	





all_elements = json.load(open('all_elements_with_semlab_qid.json'))

counter = 0
hits = 0
for el in all_elements:

	counter=counter+1
	print(counter,'/',len(all_elements))

	if 'ner' in el:

		for e in el['ner']['entities']:

			
			if e['type'] == 1:


				found_qids = []
				label_match = []
				found_person = False
				is_person = False

				for mention in e['mentions']:
					if mention['type'] == 1:
						found_person = True

						mention['text']['content'] = fold(mention['text']['content'].lower())

						mention['text']['content'] = " ".join(mention['text']['content'].split())
						
						print("its this goning in:",mention['text']['content'])

						for qid in semlabl_labels:
							if semlabl_labels[qid]['label'] in mention['text']['content']:
								if qid not in found_qids:
									found_qids.append(qid)
									label_match.append(semlabl_labels[qid])
									print('found',semlabl_labels[qid]['label'])
									mention['text']['content'] = mention['text']['content'].replace(semlabl_labels[qid]['label'],'')



						for qid in semlabl_labels:
							if semlabl_labels[qid]['last_part'] in mention['text']['content']:
								if qid not in found_qids:
									found_qids.append(qid)
									label_match.append(semlabl_labels[qid])
									print('found',semlabl_labels[qid]['last_part'])


						print("AFTER :",mention['text']['content'])

				print(e['name'])
				print(label_match)

				if len(label_match) == 0 and found_person == True:
					print("No match found for this",e['name'])

				if found_person == True:
					e['label_match'] = label_match
				
				if found_person == True and len(label_match) == 0:
					e['unknown'] = True


for el in all_elements:

	if 'ner' in el:

		for e in el['ner']['entities']:

			if 'label_match' in e and 'semlabLabel' in e:
				e['label_match'] = []


print('hits:',hits)
json.dump(all_elements,open('all_elements_with_semlab_qid_by_label.json','w'),indent=2)																		
	