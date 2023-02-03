

import json





html1= """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>EAT EAD</title>    
  </head>
  <body>

  <table>
  <style>

  a{
  	color:black !important;
  	text-decoration: none !important;
  }
  .unittitle{
  font-weight:bold;
  }

  .postivematch{
  	display:inline-block;
  	background-color: aliceblue;
  	padding: 1em;
  }
  .a-positive-match{
  padding-bottom:2px;
  }

  .labelmatch{
  padding: 1em;
    background-color: #ffe7bc;
    display: inline-block;
    }

   .nomatch{
    padding: 1em;
    background-color: #ffc6bb;
    display: inline-block;
   
   }

  </style>

"""



all_elements = json.load(open('all_elements_with_semlab_qid_by_label.json'))
knowledge_score = json.load(open('knowledge_score.json'))
html2=""
for el in all_elements:

	content = ""

	if 'unittitle' in el:
		content=content+f"<div class=\"unittitle\">{el['unittitle']}</div>"
	if el['scopecontent'] != None:
		content=content+f"<div class=\"scopecontent\">{el['scopecontent']}</div>"



	if el['container'] != None:
		content = content + f"<div class=\"container\">{el['container']}</div>"    

	postivematch = ""
	if 'ner' in el:
		for e in el['ner']['entities']:
			if 'semlab' in e:
				postivematch = postivematch + f"<div class=\"a-positive-match\"><a target=\"_blank\" href=\"http://base.semlab.io/entity/{e['semlab']}\">{e['semlabLabel']} ({knowledge_score[e['semlab']]['count']})</a></div>"

	if len(postivematch) > 0:

		content=content + f"<div class=\"postivematch\">{postivematch}</div>"

	labelmatch = ""
	added=[]
	if 'ner' in el:
		for e in el['ner']['entities']:
			if 'label_match' in e:
				for label_match in e['label_match']:
					if label_match['qid'] in added:
						continue
					added.append(label_match['qid'])	
					labelmatch = labelmatch + f"<div class=\"a-label-match\"><a target=\"_blank\" href=\"http://base.semlab.io/entity/{label_match['qid']}\">{label_match['orginal']} ({knowledge_score[label_match['qid']]['count']})</a></div>"

	if len(labelmatch) > 0:

		content=content + f"<div class=\"labelmatch\">{labelmatch}</div>"

	nomatch = ""
	added=[]
	if 'ner' in el:
		for e in el['ner']['entities']:
			if 'unknown' in e:
				if e['unknown'] == True:
					nomatch = nomatch + f"<div class=\"a-label-match\">{e['name']}</div>"

	if len(nomatch) > 0:

		content=content + f"<div class=\"nomatch\">{nomatch}</div>"







	if el['level'] == 1:
		template = f'<tr><td colspan="5">{content}</td><td></td><td></td><td></td><td></td></tr>'
	elif el['level'] == 2:
		template = f'<tr><td></td><td>{content}</td><td></td><td></td><td></td></tr>'
	elif el['level'] == 3:
		template = f'<tr><td></td><td></td><td>{content}</td><td></td><td></td></tr>'
	elif el['level'] == 4:
		template = f'<tr><td></td><td></td><td></td><td>{content}</td><td></td></tr>'
	elif el['level'] == 5:
		template = f'<tr><td></td><td></td><td></td><td></td><td>{content}</td></tr>'
	else:
		print("SHIITITITI")

	html2 = html2 + template


with open('index.html','w') as htmlfile:

	htmlfile.write(html1)
	htmlfile.write(html2)
	htmlfile.write("</table></body></html>")
