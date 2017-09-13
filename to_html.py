import json, random

from lys import L, raw

def nice_dump(item):
    if item is None:
        return '-'
    if type(item) is str:
        return item
    if type(item) is dict:
        out = L.ul / (
            (
                L.li / (
                    key,
                    ': ',
                    nice_dump(val),
                )
            ) for key, val in sorted(item.items(), key=lambda it:it[0])
        )
        return out
    if type(item) is list:
        out = L.ul / (
            (
                L.li / (
                    nice_dump(val),
                )
            ) for val in item
        )
        return out
    return L.pre / json.dumps(item, indent=2, sort_keys=True, ensure_ascii=False)

DATA = json.load(open('declarations.json'))['declarations']['declaration']

# random.shuffle(DATA)

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

    def basic(key, title, no_item):
        return (
            L.h2 / title,
            nice_dump(get(key + '.items.items')),
        ) if get(key + '.items.items') else (
            L.h4 / no_item,
        ),

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
        L.h2 / 'Général',
        nice_dump(get('general')),
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
    width: 700px;
    margin: auto;
    font-family: monospace;
    padding: 10px;
""") / (
        L.style / raw("a { color: inherit; }"),
        decls,
    )
)