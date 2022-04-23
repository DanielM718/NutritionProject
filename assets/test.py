#Import the requests library so we can send post requests to the FoodAI API
from tkinter import Image
from PIL import Image
import numpy as np
import requests
import colimg


#Set a variable with the URL just to make life easier
siteURL = "https://api.foodai.org/v4.1/classify"

Rawdata = colimg.imageC()

binaryImage = Rawdata[0].tobytes()
print(binaryImage)
print(type(binaryImage))
print(len(binaryImage))
#We open the image as a binary text using the with open statement which will close the image after the statement is done
#'rb' allows us to read as a binary text, we set binaryImage = image.read() reading the image as a binary data

#no longer neeeded below
# with open(img, 'rb') as image:
#     binaryImage = image.read()

#We create a tuple which will hold all the data to be sent as a multipart post
data = {
    #Content-Disposition: form-data; name="image_data"; filename="banana.jpg" (binaryImage would be raw binary data)
    'image_data': (Rawdata[1], binaryImage),
    #These will be parse similarly but with no filename, num_tag is how many results we want
    'num_tag': (None, "4"),
    'api_key': (None, 'a7d8d68cc247de3a93deda11fe437ca2a5a2ab6e')
}
#We create a response 
response = requests.Request('POST',siteURL,files=data)
res = response.prepare()
session = requests.Session()
result = session.send(res);



print(result.text)