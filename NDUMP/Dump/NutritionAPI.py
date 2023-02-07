import requests
import json

url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=XnRtjuAtuUfz6a43IFDUyLbcwdDJcUhkpRGKbY9N"

payload = json.dumps({
  "query": "Cheddar cheese"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
