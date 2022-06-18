import numpy as np
import requests
import cv2
import json


binaryImage = None
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) == ord('q'):
        binaryImage = cv2.imencode(".jpeg",frame)[1]
        binaryImage = np.array(binaryImage).tobytes()
        break

cap.release()
cv2.destroyAllWindows()

siteURL = "https://api.foodai.org/v4.1/classify"

data = {
    'image_data': ("banana.png", binaryImage),
    'num_tag': (None, "4"),
    'api_key': (None, 'a1e3760442d8a4125ad5a8f51542537bc0de167d')
}

response = requests.Request('POST',siteURL,files=data)
res = response.prepare()
session = requests.Session()
result = session.send(res)
Food = result.text
print(Food)

url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=XnRtjuAtuUfz6a43IFDUyLbcwdDJcUhkpRGKbY9N"

payload = json.dumps({
  "query": Food
})
headers = {
  'Content-Type': 'application/json'
}

responseFood = requests.request("POST", url, headers=headers, data=payload)

print(responseFood.text)