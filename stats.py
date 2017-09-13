import json
from collections import Counter

DATA = json.load(open('stock.json'))

def attrget(item, key):
    keys = key.split('.')
    for key in keys:
        item = item.get(key,'')
        if item == None:
            return
    return item

def stats(key=None, attrget=attrget, limit=10, inception=False, data=None, label=None):
    data = data if data else DATA
    def flat(arr):
        for x in arr:
            if type(x) == type([]):
                yield from flat(x)
            elif type(x) == str:
                yield x.strip()
            else:
                yield x

    c = Counter(flat([attrget(el,key) for el in data]))

    count_all = len(data)
    count_distinct = len(c)
    print()
    print(label if label else key,"   -   ",count_all,"values,",count_distinct,"distincts")
    print('----')

    for el,n in c.most_common(limit):
        p = n/count_all*100
        print("{:.1f}% ({}) {}".format(p,n,el))
    print()

    if inception:
        stats(key="---> "+key+'-ception', attrget=lambda i, k: i, data=c.values())

stats("pays")
stats("categorieOrganisation.label")
stats("codePostal")
stats("departement", lambda item, key: item['codePostal'][:2])

secteurs = []
for item in DATA:
    secteurs += item['activites']['listSecteursActivites']

stats('label', data=secteurs, label='listSecteursActivites.label')

interventions = []
for item in DATA:
    interventions += item['activites']['listNiveauIntervention']

stats('label', data=interventions, label='listNiveauIntervention.label')