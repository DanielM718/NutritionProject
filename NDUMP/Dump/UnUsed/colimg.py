import cv2
import numpy as np
def imageC():
    
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            # img = frame.copy()
            img = cv2.imencode('.jpeg', frame)
            print(type(img))
            #this function below creates an img but how would we store it in a variable
            #cv2.imwrite(img_name, img)

            #print("{} written!".format(img_name))
            img_counter += 1
            break

    print(type(img))

    cam.release()

    cv2.destroyAllWindows()

    return(img, img_name)