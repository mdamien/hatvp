import xmltodict, json

data = xmltodict.parse(open('declarations.xml').read())

json.dump(data, open('declarations.json', 'w'), indent=2)