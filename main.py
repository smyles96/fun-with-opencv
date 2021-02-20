from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import cvutil

grayscale_active = False

subtractor_active = False
canny_active = False
gaussian_active = False
recognizer_active = False
lmfilter_active = False

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt",
	help="path to Caffe 'deploy' prototxt file", default = "models/deploy.prototxt")
ap.add_argument("-m", "--model",
	help="path to Caffe pre-trained model", default = "models/res10_300x300_ssd_iter_140000.caffemodel")
ap.add_argument("-c", "--confidence", type=float, default=0.88,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# Read in Caffe model, create subtractor, and load filter image
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
lm_image = cv2.imread("resources/laugh.png", -1)

vs = VideoStream(src=0).start()
time.sleep(2.0)

try:
    while(1):
        frame = vs.read()
        frame = imutils.resize(frame, width=600)

        if grayscale_active:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if subtractor_active:
            fgmask = fgbg.apply(frame)
            cv2.imshow('Frame',fgmask)
        elif canny_active:
            frame = cv2.Canny(frame, 50, 147)

            cv2.imshow('Frame', frame)
        elif gaussian_active:
            blur = cv2.GaussianBlur(frame,(7,7),0)
            lap = cv2.Laplacian(blur,cv2.CV_64F, ksize=7)
            cv2.imshow('Frame', lap)
        elif recognizer_active:
            # grab the frame dimensions and convert it to a blob
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                (300, 300), (104.0, 177.0, 123.0))
        
            # pass the blob through the network and obtain the detections and
            # predictions
            net.setInput(blob)
            detections = net.forward()

            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence < args["confidence"]:
                    continue

                # compute the (x, y)-coordinates of the bounding box for the
                # object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                if lmfilter_active:
                    # If the laughing filter is active, draw sprite over image
                    frame = cvutil.add_sprite(frame, lm_image, endY - startY, startX - 50, endY)
                else:
                    # Otherwise draw the bounding box of the face along with the associated probability
                    text = "{:.2f}%".format(confidence * 100)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                        (0, 0, 255), 2)
                    cv2.putText(frame, text, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

                # show the output frame
            cv2.imshow("Frame", frame)
        else:
            cv2.imshow('Frame',frame)

        key = cv2.waitKey(1) & 0xff

        # Press 'q' to quit 
        if key == ord('q'):
            break

        # Activate subtractor
        if key == ord('s'):
            # Disable other filters
            recognizer_active = False
            gaussian_active = False
            canny_active = False

            subtractor_active = not subtractor_active

        if key == ord('c'):
            recognizer_active = False
            subtractor_active = False
            gaussian_active = False

            canny_active = not canny_active

        # Activate laplacian of gaussian
        if key == ord('g'):
            recognizer_active = False
            subtractor_active = False
            canny_active = False

            gaussian_active = not gaussian_active

        # Apply median blur
        if key == ord('z'):
            grayscale_active = not grayscale_active

        # Activate recognizer
        if key == ord('r'):
            subtractor_active = False
            gaussian_active = False
            canny_active = False
            grayscale_active = False

            recognizer_active = not recognizer_active

            if lmfilter_active:
                lmfilter_active = False

        # Activate laughing filter
        if key == ord('l') and recognizer_active:
            lmfilter_active = not lmfilter_active

finally:
    vs.stop()
    cv2.destroyAllWindows()