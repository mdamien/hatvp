import json
from collections import Counter

DATA = json.load(open('declarations.json'))['declarations']['declaration']

def attrget(item, key):
    keys = [k for k in key.split('.') if k]
    for key in keys:
        if type(item) is str:
            return
        if type(item) is list:
            return
        item = item.get(key,'')
        if item == None:
            return
    return item

def stats(key=None, attrget=attrget, limit=40, inception=False, data=None, label=None):
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

    most_common = c.most_common(limit)
    most_common.sort(key=lambda x: (-x[1],str(x[0])))
    for el, n in most_common:
        p = n/count_all*100
        print("{:.1f}% ({}) {}".format(p,n,el))
    print()

    if inception:
        stats(key="---> "+key+'-ception', attrget=lambda i, k: i, data=c.values())

print('<pre>') # fancy hack to make it an html page
stats("origine")

ex = DATA[0]

def stats_dict(dic, prefix='', data=None, display_prefix=None):
    for key, item in sorted(dic.items()):
        fullkey = (prefix + '.' + key) if prefix else key
        if type(item) is dict:
            stats_dict(item, fullkey, data=data, display_prefix=display_prefix)
        elif type(item) is list:
            # TODO
            pass
        else:
            stats(fullkey, data=data, label=(display_prefix + ' / ' + fullkey) if display_prefix else None)

stats_dict(ex['general'], 'general')

dto_keys = ['activConsultantDto', 'activProfCinqDerniereDto', 'activProfConjointDto', 'activConsultantDto', 'fonctionBenevoleDto', 'mandatElectifDto', 'participationDirigeantDto', 'participationFinanciereDto', 'observationInteretDto', 'activCollaborateursDto']

def force_list(items):
    if not items:
        items = []
    if type(items) is dict:
        items = [items]
    return items

for key in dto_keys:
    all_items = []
    for item in DATA:
        all_items += force_list(attrget(item, key + '.items.items'))
    ex = all_items[0]
    stats_dict(ex, data=all_items, display_prefix=key)
