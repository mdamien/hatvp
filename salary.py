import json

data = json.load(open('declarations.json'))['declarations']["declaration"]

mandats = []

for guy in data:
    details = guy["general"]["declarant"]
    nom = "%s %s" % (details["nom"], details["prenom"])
    salarys = guy["mandatElectifDto"].get('items', {})
    if salarys is None:
        salarys = {}
    salarys = salarys.get("items", [])
    if type(salarys) is dict:
        salarys = [salarys]
    mandats.append([nom, salarys])

print('Cumul de mandat')
for nom, salarys in sorted(mandats, key=lambda it: -len(it[1])):
    print(nom, len(salarys))