from weights import GemWeights
import json
import re

GemPrices = {}

PrimeLens = 90
SecondaryLens = 290
cutoff = 40


f = open("ninja.json", "r")
ninjaJSON = json.load(f) 


for gem in GemWeights:
    GemPrices[gem] = {}
    for type in GemWeights[gem]:
        GemPrices[gem][type] = 0


# for attribute in ninjaJSON["lines"][0]:
#     print(attribute)

woke = re.compile('^Awakened')
qualityType = re.compile("^(Divergent|Anomalous|Phantasmal)")
support = re.compile(" Support$")

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

            if myQualType is not "Superior":
                myShortName = item['name'][len(myQualType) + 1:]
            else:
                myShortName = item['name']
            if GemPrices[myShortName][myQualType] is 0 or GemPrices[myShortName][myQualType] > item['chaosValue']:
                GemPrices[myShortName][myQualType] = item['chaosValue']


results = {}

for gem in GemWeights:
    # print("Calculating " + gem)
    sup = GemPrices[gem].get("Superior", 0.0)
    supWeight = GemWeights[gem].get("Superior", 0.0)
    div = GemPrices[gem].get("Divergent", 0.0)
    divWeight = GemWeights[gem].get("Divergent", 0.0)
    ano = GemPrices[gem].get("Anomalous", 0.0)
    anoWeight = GemWeights[gem].get("Anomalous", 0.0)
    pha = GemPrices[gem].get("Phantasmal", 0.0)
    phaWeight = GemWeights[gem].get("Phantasmal", 0.0)

    lensPrice = PrimeLens

    if support.search(gem):
        lensPrice = SecondaryLens

    if supWeight > 0:
        expectedValue = (div - sup) * (divWeight / (divWeight + anoWeight + phaWeight)) - lensPrice

        if expectedValue > cutoff:
            resultKey = "sup to div " + gem
            results[resultKey] = expectedValue

        expectedValue = (ano - sup) * (anoWeight / (divWeight + anoWeight + phaWeight)) - lensPrice

        if expectedValue > cutoff:
            resultKey = "sup to ano " + gem
            results[resultKey] = expectedValue

        expectedValue = (pha - sup) * (phaWeight / (divWeight + anoWeight + phaWeight)) - lensPrice

        if expectedValue > cutoff:
            resultKey = "sup to pha " + gem
            results[resultKey] = expectedValue

    
    if divWeight > 0:
        expectedValue = (pha - div) * (phaWeight / (supWeight + anoWeight + phaWeight)) - lensPrice

        if expectedValue > cutoff:
            resultKey = "div to pha " + gem
            results[resultKey] = expectedValue

        expectedValue = (ano - div) * (anoWeight / (supWeight + anoWeight + phaWeight)) - lensPrice

        if expectedValue > cutoff:
            resultKey = "div to ano " + gem
            results[resultKey] = expectedValue


    if anoWeight > 0:
        expectedValue = (div - ano) * (divWeight / (divWeight + supWeight + phaWeight)) - lensPrice

        if expectedValue > cutoff:
            resultKey = "ano to div " + gem
            results[resultKey] = expectedValue

        expectedValue = (pha - ano) * (phaWeight / (divWeight + supWeight + phaWeight)) - lensPrice

        if expectedValue > cutoff:
            resultKey = "ano to pha " + gem
            results[resultKey] = expectedValue


    if phaWeight > 0:
        expectedValue = (div - pha) * (divWeight / (divWeight + anoWeight + supWeight)) - lensPrice

        if expectedValue > cutoff:
            resultKey = "pha to div " + gem
            results[resultKey] = expectedValue

        expectedValue = (ano - pha) * (anoWeight / (divWeight + anoWeight + supWeight)) - lensPrice

        if expectedValue > cutoff:
            resultKey = "pha to ano " + gem
            results[resultKey] = expectedValue

for result in results:
    print(result + " - " + str(results[result]))