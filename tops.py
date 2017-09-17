import json

data = json.load(open('declarations.json'))['declarations']["declaration"]

def force_list(items):
    if type(items) is dict:
        items = [items]
    return items

mandats = []

best_of = []

for guy in data:
    details = guy["general"]["declarant"]
    nom = "%s %s" % (details["nom"], details["prenom"])
    salarys = guy["mandatElectifDto"].get('items', {})
    if salarys is None:
        salarys = {}
    salarys = salarys.get("items", [])
    salarys = force_list(salarys)

    for salary in salarys:
        for item in force_list(salary['remuneration']['montant']['montant']):
            print(item['annee'], item['montant'])
            best_of.append(int(item['montant']))

    mandats.append([nom, salarys])

print('Cumul de mandat')
for nom, salarys in sorted(mandats, key=lambda it: len(it[1])):
    print(nom, len(salarys))

print(len(mandats))

print('Les meilleurs salaires')
print(sorted(best_of)[-5:])