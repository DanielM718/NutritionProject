#Importing numpy so we can convert any frame into a numpy array then into a bytes 
import numpy as np
#Import the requests library so we can send post requests to the FoodAI API
import requests
import cv2

#Setting global variable binaryImage to None so we can update it 
binaryImage = None
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame

    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    

    #displaying the image onto the screen
    cv2.imshow('frame',frame)
    #We are using the key 'q' for capturing an image and it will also end the program
    if cv2.waitKey(1) == ord('q'):
        #we update our binaryImage with the frame encoded into a jpeg (jpeg as it compresses well)
        binaryImage = cv2.imencode(".jpeg",frame)[1]
        #we then convert this jpeg encoded image data and make it into a numpy array
        # we then use the .tobytes() function to convert it into binary data 
        binaryImage = np.array(binaryImage).tobytes()
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

#Set a variable with the URL just to make life easier
siteURL = "https://api.foodai.org/v4.1/classify"

#We open the image as a binary text using the with open statement which will close the image after the statement is done
#'rb' allows us to read as a binary text, we set binaryImage = image.read() reading the image as a binary data


print(len(binaryImage))
#We create a tuple which will hold all the data to be sent as a multipart post
data = {
    #Content-Disposition: form-data; name="image_data"; filename="banana.jpg" (binaryImage would be raw binary data)
    'image_data': ("banana.png", binaryImage),
    #These will be parse similarly but with no filename, num_tag is how many results we want
    'num_tag': (None, "4"),
    'api_key': (None, 'a7d8d68cc247de3a93deda11fe437ca2a5a2ab6e')
}


#We create a Request object that will hold our data tuple as files (and will parse it into multipart formating)
response = requests.Request('POST',siteURL,files=data)
#We then use the Request.prepare() method to create a prepared request object that we can then send 
res = response.prepare()
#We create a session where we can send our requests
session = requests.Session()
#We save the results of the Preparedrequest sent to the api
result = session.send(res)

#result.text allows us to see it as pure text
print(result.text)