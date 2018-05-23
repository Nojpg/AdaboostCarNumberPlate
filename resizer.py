import argparse
import cv2
import os


def resizer(data_folder, folder, filename, type):
    for images in [data_folder + "/" + folder]:
        for image_name in os.listdir(images):

            if type == "pos":
                # for already created
                image_path = data_folder + "/" + folder + "/" + image_name

                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                resized_image = cv2.resize(image, (100, 100))
                cv2.imwrite(image_path, resized_image)

                line = folder + "/" + image_name + " 1 0 0 100 100\n"

                image = cv2.imread(image_path)
                if image is None:
                    print("[WARNING] image is empty: {}".format(image_name))
                    continue
            else:
                line = folder + "/" + image_name + "\n"

            if not os.path.exists(data_folder + "/" + filename):
                with open(data_folder + "/" + filename, "x") as file:
                    file.write(line)
            else:
                with open(data_folder + "/" + filename, "a") as file:
                    file.write(line)


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--data", required=True, help="data folder for both negative and positive data")
ap.add_argument("-f", "--folder", required=True, help="folder for data negative or positive")
ap.add_argument("-n", "--filename", required=True, help="file with coordinates")
ap.add_argument("-t", "--type", required=True, help="type of data: pos or neg")
args = vars(ap.parse_args())

resizer(args["data"], args["folder"], args["filename"], args["type"])

os._exit(0)
