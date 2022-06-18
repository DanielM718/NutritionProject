import json

from numpy import append

response = open('response.json')

raw = json.load(response)

data = raw['foods']
i = 0
brand = 0
h=0
Kcal = []
Kjoules = []

while brand < len(data):
    nutrients = data[brand]['foodNutrients']
    for i in nutrients:
        if i['nutrientId'] == 1008:
            Kcal.append(i['value'])
        elif i['nutrientId'] == 1062:
            conversion = (i['value'])/(4.184)
            Kjoules.append(round(conversion))
    brand+=1


for cal in Kcal:
    print(cal)
for calk in Kjoules:
    print(calk)