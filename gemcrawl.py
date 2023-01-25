from weights import GemWeights
from newWeights import newGemWeights
import json
import re

def sum(weights):
    mySum = 0
    for w in weights:
        mySum += w

    return mySum


GemPrices = {}

PrimeLens = 90
SecondaryLens = 290
cutoff = 40
qual = {"Superior":0, "Anomalous":1, "Divergent":2, "Phantasmal":3}
qualLookup = ["Superior", "Anomalous", "Divergent", "Phantasmal"]

f = open("ninja.json", "r")
ninjaJSON = json.load(f) 

woke = re.compile('^Awakened')
qualityType = re.compile("^(Divergent|Anomalous|Phantasmal)")
support = re.compile(" Support$")

for gem in newGemWeights:
    GemPrices[gem] = [0.0,0.0,0.0,0.0]

#import prices from Ninja
for item in ninjaJSON["lines"]:
    if item.get("corrupted", False) is False:
        if not woke.search(item["name"]):
            REmatch = qualityType.search(item['name'])
            myQualType = ""
            myShortName = ""
            if not REmatch:
                myQualType = "Superior"
            else:
                myQualType = REmatch.group(1)

            if myQualType != "Superior":
                myShortName = item['name'][len(myQualType) + 1:]
            else:
                myShortName = item['name']
            
            if GemPrices[myShortName][qual[myQualType]] == 0 or GemPrices[myShortName][qual[myQualType]] > item['chaosValue']:
                GemPrices[myShortName][qual[myQualType]] = item['chaosValue']

results = {}

for gem in newGemWeights:
    lensPrice = PrimeLens

    if support.search(gem):
        lensPrice = SecondaryLens

    #calculate hits
    #a hit is any gem where the expected value of slamming a lens is above the cutoff
    for source in qual.values():
        for dest in qual.values():
            if source != dest and GemPrices[gem][dest] > lensPrice:
                cost = lensPrice + GemPrices[gem][source]
                probability = newGemWeights[gem][dest] / (sum(newGemWeights[gem]) - newGemWeights[gem][source])
                gross = probability * GemPrices[gem][dest]
                profit = gross - cost
                
                if profit > cutoff:
                    if results.get(gem) is None:
                        results[gem] = {}
                    results[gem][(source, dest)] = {"Profit":profit, "HitChance": probability, "SalvageChance":0.0}

    #calculate salvage rate
    for hit in results.get(gem, {}):
        for dest in qual.values():
            if hit[0] != dest and hit[1] != dest and results[gem].get((dest, hit[1])) != None:
                probability = newGemWeights[gem][dest] / (sum(newGemWeights[gem]) - newGemWeights[gem][hit[0]])
                results[gem][hit]["SalvageChance"] += probability

for gem in results:
    for hit, result in results[gem].items():
        print("{} {} to {} - Profit: {:.3f} Hit Rate: {:.2%} Salvage: {:.2%}".format(qualLookup[hit[0]], gem, qualLookup[hit[1]], result["Profit"], result["HitChance"], result["SalvageChance"]))
    print("--------------------------------------")
