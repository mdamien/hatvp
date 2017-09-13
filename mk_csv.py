import csv, json

writer = csv.writer(open('stock.csv', 'w'))

writer.writerow(['denomination', 'pays', 'ville', 'codePostal', 'addresse', 'identifiantNational',
        'datePremierePublication', 'secteurs', 'niveaux'])
for item in json.load(open('stock.json')):
    writer.writerow([
        item['denomination'],
        item['pays'],
        item['ville'],
        item['codePostal'],
        '%s %s %s' % (item['pays'], item['codePostal'], item['ville']),
        item['identifiantNational'],
        item['datePremierePublication'].split(' ')[0],
        ' | '.join(it['label'] for it in item['activites']['listSecteursActivites']),
        ' | '.join(it['label'] for it in item['activites']['listNiveauIntervention']),
    ])