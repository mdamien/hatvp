require 'its-it'
require 'json'

data = JSON.load(File.read('declarations.json'))

i = data["declarations"]["declaration"].map do |d|
    b = d["general"]["declarant"]
    name = "#{b["civilite"]} #{b["nom"]} #{b["prenom"]}"
    items = d["mandatElectifDto"].fetch("items", {}).fetch("items", {}) || {}
 
    s = items.map do |t|
        t.fetch("renumeration", {}).fetch("montant", {}).fetch("montant", 0)
    end
    
    [name, s]
end

i = i.sort_by(&:last)

puts i.map(&its.reverse.join(': '))
