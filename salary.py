import json

data = json.load(open('declarations.json'))['declarations']["declaration"]

for guy in data:
    details = guy["general"]["declarant"]
    nom = "%s %s %s" % (details["civilite"], details["nom"], details["prenom"])
    salarys = guy["mandatElectifDto"].get('items', {})
    if salarys is None:
        salarys = {}
    salarys = salarys.get("items", [])
    if type(salarys) is dict:
        salarys = [salarys]
    print(nom)
    print(len(salarys), 'postes')
    print()
    print()