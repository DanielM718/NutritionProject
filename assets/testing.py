import json
import numpy as np
# from numpy import append

response = open('response.json')

raw = json.load(response)

datas = raw['foods']
i = 0
x = 0
h=0
Kcal = []
Kcal =  np.array(Kcal)
Kjoules = []
Kjoules =  np.array(Kjoules)
nutrients = []
nutrients =  np.array(nutrients)

while x < len(datas):
    np.append(nutrients, datas[x]['foodNutrients'])
    print(nutrients(0))
    while i < len(nutrients[x]):
        while h < len(nutrients[x][i]):
            if nutrients[x][i]['nutrientId'] == 1008:
                np.append(Kcal, nutrients[i][h]['value'])
                print(Kcal)
            elif nutrients[x][i]['nutrientId'] == 1062:
                np.append(Kjoules, nutrients[i][h]['value'])
                print(Kjoules)
            h+=1
        i+=1
    x+=1


Kcal = np.array(Kcal)


for cal in Kcal:
    print(cal)
for calk in Kjoules:
    print(calk)