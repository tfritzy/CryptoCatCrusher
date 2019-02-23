import ExtractKittyData
import LearnPrices

#catNum = input("which cat would you like to check? ")
catNum = "1298868"
catDict = ExtractKittyData.getCatFromID(catNum)
print(LearnPrices.predictCatPrice(catDict))
