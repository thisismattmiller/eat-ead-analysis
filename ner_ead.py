from google.cloud import language
from lxml import etree
import json


tree = etree.parse(open('940003.xml'))
root = tree.getroot()

# for child in root:
    # print(child.tag)


all_elements = []

for c01 in root.xpath("//c01"):

    c01_data = {
        'unittitle':None,
        'scopecontent': None,
        'id': c01.get('id'),
        'container': None,
        'level': 1
    }

    if (len(c01.xpath("did/unittitle"))>0):
        c01_data['unittitle'] =  c01.xpath("did/unittitle")[0].text

    if (len(c01.xpath("scopecontent"))>0):
        c01_data['scopecontent'] = ''.join(c01.xpath("scopecontent")[0].itertext()).strip()

    for container in c01.xpath("did/container"):
        if c01_data['container'] == None:
            c01_data['container'] = ''

        c01_data['container'] = c01_data['container'] + ' ' + container.get('type') + ' ' + container.text
        c01_data['container']=c01_data['container'].strip()
    
    all_elements.append(c01_data)


    for c02 in c01.xpath("c02"):

        c02_data = {
            'unittitle':None,
            'scopecontent': None,
            'id': c02.get('id'),
            'container': None,
            'level': 2
        }

        if (len(c02.xpath("did/unittitle"))>0):
            c02_data['unittitle'] =  c02.xpath("did/unittitle")[0].text

        if (len(c02.xpath("scopecontent"))>0):
            c02_data['scopecontent'] = ''.join(c02.xpath("scopecontent")[0].itertext()).strip()

        for container in c02.xpath("did/container"):
            if c02_data['container'] == None:
                c02_data['container'] = ''

            c02_data['container'] = c02_data['container'] + ' ' + container.get('type') + ' ' + container.text
            c02_data['container']=c02_data['container'].strip()
        
        all_elements.append(c02_data)


        for c03 in c02.xpath("c03"):

            c03_data = {
                'unittitle':None,
                'scopecontent': None,
                'id': c03.get('id'),
                'container': None,
                'level': 3
            }

            if (len(c03.xpath("did/unittitle"))>0):
                c03_data['unittitle'] =  c03.xpath("did/unittitle")[0].text

            if (len(c03.xpath("scopecontent"))>0):
                c03_data['scopecontent'] = ''.join(c03.xpath("scopecontent")[0].itertext()).strip()

            for container in c03.xpath("did/container"):
                if c03_data['container'] == None:
                    c03_data['container'] = ''

                c03_data['container'] = c03_data['container'] + ' ' + container.get('type') + ' ' + container.text
                c03_data['container']=c03_data['container'].strip()
            
            all_elements.append(c03_data)

            


            for c04 in c03.xpath("c04"):

                c04_data = {
                    'unittitle':None,
                    'scopecontent': None,
                    'id': c04.get('id'),
                    'container': None,
                    'level': 4
                }

                if (len(c04.xpath("did/unittitle"))>0):
                    c04_data['unittitle'] =  c04.xpath("did/unittitle")[0].text

                if (len(c04.xpath("scopecontent"))>0):
                    c04_data['scopecontent'] = ''.join(c04.xpath("scopecontent")[0].itertext()).strip()

                for container in c04.xpath("did/container"):
                    if c04_data['container'] == None:
                        c04_data['container'] = ''

                    c04_data['container'] = c04_data['container'] + ' ' + container.get('type') + ' ' + container.text
                    c04_data['container']=c04_data['container'].strip()
                
                all_elements.append(c04_data)
        

                for c05 in c04.xpath("c05"):

                    c05_data = {
                        'unittitle':None,
                        'scopecontent': None,
                        'id': c05.get('id'),
                        'container': None,
                        'level': 5
                    }

                    if (len(c05.xpath("did/unittitle"))>0):
                        c05_data['unittitle'] =  c05.xpath("did/unittitle")[0].text

                    if (len(c05.xpath("scopecontent"))>0):
                        c05_data['scopecontent'] = ''.join(c05.xpath("scopecontent")[0].itertext()).strip()

                    for container in c05.xpath("did/container"):
                        if c05_data['container'] == None:
                            c05_data['container'] = ''

                        c05_data['container'] = c05_data['container'] + ' ' + container.get('type') + ' ' + container.text
                        c05_data['container']=c05_data['container'].strip()
                    
                    all_elements.append(c05_data)





print(all_elements)
already_done = {}





#####export GOOGLE_APPLICATION_CREDENTIALS=/Users/m/git/eat-ead-analysis/GOOGLE_APPLICATION_CREDENTIALS.json
client = language.LanguageServiceClient()

counter = 0
for el in all_elements:

    counter=counter+1
    print(counter,'/',len(all_elements))

    # if 'ner' in el:
    #     print('skip')
    #     continue


    text = ''
    if el['unittitle'] != None:
        text = text + ' ' + el['unittitle']
    if el['scopecontent'] != None:
        text = text + ' ' + el['scopecontent']

    text = text.strip()

    if text in already_done:
        el['ner'] = already_done[text]
        print('already done skip')
        json.dump(all_elements, open('all_elements.json','w'),indent=2)
        continue

    



    try:
        document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
        response = client.analyze_entities(document=document)
    except:

        print('error ner')
        continue

    # for entity in response.entities:
    #     print("=" * 80)
    #     results = dict(
    #         name=entity.name,
    #         type=entity.type_.name,
    #         salience=f"{entity.salience:.1%}",
    #         wikipedia_url=entity.metadata.get("wikipedia_url", "-"),
    #         mid=entity.metadata.get("mid", "-"),
    #     )
    #     print(entity)

    el['ner'] = json.loads(response.__class__.to_json(response))

    already_done[text] = el['ner']


    json.dump(all_elements, open('all_elements.json','w'),indent=2)





