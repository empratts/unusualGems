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
    S = GemPrices[gem].get("Superior", 0.0)
    SW = GemWeights[gem].get("Superior", 0.0)
    D = GemPrices[gem].get("Divergent", 0.0)
    DW = GemWeights[gem].get("Divergent", 0.0)
    A = GemPrices[gem].get("Anomalous", 0.0)
    AW = GemWeights[gem].get("Anomalous", 0.0)
    P = GemPrices[gem].get("Phantasmal", 0.0)
    PW = GemWeights[gem].get("Phantasmal", 0.0)

    lensPrice = PrimeLens

    if support.search(gem):
        lensPrice = SecondaryLens

    if SW > 0:
        cost = S + lensPrice
        expectedReturn = (A*AW+D*DW+P*PW)/(AW+DW+PW)
        profit = expectedReturn - cost
        if profit > cutoff:
            results["Superior {}".format(gem)]=profit

    if AW > 0:
        cost = A + lensPrice
        expectedReturn = (S*SW+D*DW+P*PW)/(SW+DW+PW)
        profit = expectedReturn - cost
        if profit > cutoff:
            results["Anomalous {}".format(gem)]=profit

    if DW > 0:
        cost = D + lensPrice
        expectedReturn = (A*AW+S*SW+P*PW)/(AW+SW+PW)
        profit = expectedReturn - cost
        if profit > cutoff:
            results["Divergent {}".format(gem)]=profit

    if PW > 0:
        cost = P + lensPrice
        expectedReturn = (A*AW+D*DW+S*SW)/(AW+DW+SW)
        profit = expectedReturn - cost
        if profit > cutoff:
            results["Phantasmal {}".format(gem)]=profit

qualityRemove = re.compile("^(Superior|Divergent|Anomalous|Phantasmal) (.*)$")

for result in results:
    if not support.search(result):
        print(result + " - " + str(results[result]))
        # baseName = qualityRemove.search(result).group(2)
        # print(GemPrices[baseName])
        # print(GemWeights[baseName])

print("---------Supports---------")

for result in results:
    if support.search(result):
        print(result + " - " + str(results[result]))