import requests
import json



all_elements = json.load(open('all_elements.json'))
try:
	already_done = json.load(open('already_done.json'))
except:
	already_done={}

counter = 0

for el in all_elements:

	counter=counter+1
	print(counter,'/',len(all_elements))

	if 'ner' in el:

		for e in el['ner']['entities']:

			if 'metadata' in e:

				if 'wikipedia_url' in e['metadata']:

					if 'qid' not in e:
						e['qid']  =[]

					print(e['metadata']['wikipedia_url'])

					if e['metadata']['wikipedia_url'] in already_done:

						e['qid'].append(already_done[e['metadata']['wikipedia_url']])
						print('skipping already_done')

					else:

						slug = e['metadata']['wikipedia_url'].split('/')[-1]
						url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&format=json&titles={slug}"


						r = requests.get(url)
						data = r.json()

						if 'query' in data:
							if 'pages' in data['query']:
								for k in data['query']['pages']:

									try:
										already_done[e['metadata']['wikipedia_url']] = data['query']['pages'][k]['pageprops']['wikibase_item']
										e['qid'].append(data['query']['pages'][k]['pageprops']['wikibase_item'])
										already_done
										json.dump(already_done,open('already_done.json','w'),indent=2)																		


									except:
										continue



json.dump(all_elements,open('all_elements_with_qid.json','w'),indent=2)																		
	