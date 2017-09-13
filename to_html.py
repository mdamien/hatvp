import json, random

from lys import L, raw

KEYS_BLACKLIST = ('motif',)

def nice_dump(item, prev_key=None):
    if item is None:
        return '-'
    if type(item) is str:
        return item
    if type(item) is dict:
        # todo: mandat.label: dsasd
        if len(item.keys()) == 1:
            key = list(item.keys())[0]
            if key == prev_key:
                return nice_dump(item[prev_key])
        out = L.ul(style='list-style: none;padding-left:25px') / (
            (
                L.li / (
                    L.small / key,
                    ': ',
                    nice_dump(val, prev_key=key),
                )
            ) for key, val in sorted(item.items(), key=lambda it:it[0]) if key not in KEYS_BLACKLIST
        )
        return out
    if type(item) is list:
        out = L.ul(style='list-style: none;padding-left:25px') / (
            (
                L.li / (
                    '-',
                    nice_dump(val),
                )
            ) for val in item
        )
        return out
    return L.pre / json.dumps(item, indent=2, sort_keys=True, ensure_ascii=False)

DATA = json.load(open('declarations.json'))['declarations']['declaration']

random.seed(1)
random.shuffle(DATA)

decls = []
for decl in DATA:
    def get_gen(item):
        def get(key, item=item):
            keys = key.split('.')
            for key in keys:
                if type(item) is str:
                    return
                item = item.get(key,'')
                if item == None:
                    return
            return item
        return get


    get = get_gen(decl)

    def activ_consult():
        items = get('activConsultantDto.items.items')
        if type(items) is not list: items = [items]
        result = []
        for item in items:
            geta = get_gen(item)
            result.append((
                geta('nomEmployeur'),
                ', ',
                geta('commentaire'),
            ))
        return result

    i = 0
    def basic(key, title, no_item):
        global i
        color = ['#4caf50', '#689F38'][i % 2]
        i += 1
        return L.div(style='border-left:10px solid %s;padding-left:10px' % color) / (
            (
                L.h3 / title,
                nice_dump(get(key + '.items.items')),
            ) if get(key + '.items.items') else (
                L.h4 / no_item,
            )
        )

    decls.append(L.div / (
        L.hr(style="border: 10px solid #009688;"),
        L.h1(style="border: 6px solid #009688;padding: 11px;color: #009686;") / (
            get('general.declarant.nom'),
            ' ',
            get('general.declarant.prenom'),
        ),
        L.h4 / (
            'Mandat: ',
            get('general.mandat.label'),
        ),
        L.h3 / 'Général',
        L.div(style='border-left:10px solid #689F38;padding-left:10px') / nice_dump(get('general')),
        basic('activConsultantDto', 'Activité consultant', 'Pas d\'activité consultant'),
        basic('activProfCinqDerniereDto', 'Activité prof.', 'Pas d\'activité prof.'),
        basic('activProfConjointDto', 'Activité conjoint', 'Pas d\'activité conjoint'),
        basic('activConsultantDto', 'Activité consultant', 'Pas d\'activité consultant'),
        basic('fonctionBenevoleDto', 'Activité bénévole', 'Pas d\'activité bénévole'),
        basic('participationDirigeantDto', 'Mandat électif', 'Pas de mandat électif'),
        basic('participationFinanciereDto', 'Mandat électif', 'Pas de mandat électif'),
        basic('observationInteretDto', 'Mandat électif', 'Pas de mandat électif'),

    ))

print(
    L.body(style="""
    background: #cecece;
    color: #353535;
    font-size: 1.9rem;
    width: 900px;
    margin: auto;
    font-family: monospace;
    padding: 10px;
""") / (
        L.style / raw("a { color: inherit; }"),
        decls,
    )
)