import argparse
import cv2
import matplotlib.pyplot as plt
import pylab


def adaboost(path, type, classifier):

    if classifier is None:
        classifier = "haarcascade_russian_plate_number.xml"
    if type is None:
        type = "show"
    number_cascade = cv2.CascadeClassifier(classifier)
    color = (255, 255, 0)
    thickness = 2
    img_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    numbers = number_cascade.detectMultiScale(image=img_gray, scaleFactor=1.1, minNeighbors=4)

    for (x, y, w, h) in numbers:
        cv2.rectangle(img_bgr, (x, y), (x + w, y + h), color, thickness)

    if type == "show":
        plt.imshow(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
        pylab.show()
    else:
        cv2.imwrite(path, img_bgr)


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="path for image")
ap.add_argument("-t", "--type", required=False,
                help="type of operation, include keys as show or write, default is show")
ap.add_argument("-c", "--classifier", required=False, help="choose classifier for network, default "
                                                           "haarcascade_russian_plate_number.xml")
args = vars(ap.parse_args())


adaboost(args["path"], args["type"], args["classifier"])

# os._exit(0) for debug
