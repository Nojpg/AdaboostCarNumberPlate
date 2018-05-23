import os

import argparse
from requests import RequestException, HTTPError, Timeout, get
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True, help="search query to search Bind Image API for")
ap.add_argument("-o", "--output", required=True, help="path to output directory of images")
ap.add_argument("-r", "--resize", required=False,
                help="will downloaded images be resized to 100, 100 can be true or false, default false")
args = vars(ap.parse_args())

API_KEY = "7bf3b4c2f54040dd9d5f88249217c52e"
MAX_RESULTS = 200
GROUP_SIZE = 50

URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

EXCEPTIONS = {IOError, FileNotFoundError, RequestException, HTTPError, ConnectionError, Timeout}

term = args["query"]
headers = {"Ocp-Apim-Subscription-Key": API_KEY}
params = {"q": term, "offset": 0, "count": GROUP_SIZE}

print("[INFO] searching Bing API for '{}'".format(term))
search = get(URL, headers=headers, params=params)
search.raise_for_status()

results = search.json()
estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
print("[INFO] {} total results for '{}'".format(estNumResults, term))

total = 0

if not os.path.exists(args["output"]):
    os.makedirs(args["output"])

for offset in range(0, estNumResults, GROUP_SIZE):
    print("[INFO] making request for group {}--{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))
    params["offset"] = offset
    search = get(URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()
    print("[INFO] saving images for group {}--{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))

    for v in results["value"]:
        try:

            print("[INFO] fetching: {}".format(v["contentUrl"]))
            r = get(v["contentUrl"], timeout=30)

            ext = v["contentUrl"][v["contentUrl"].rfind("."):]
            p: str = os.path.sep.join([args["output"], "{}{}".format(str(total).zfill(8), ext)])

            f = open(p, "wb")
            f.write(r.content)
            f.close()

            if args["resize"] == "true":
                image = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
                resized_image = cv2.resize(image, (100, 100))
                cv2.imwrite(p, resized_image)

            image = cv2.imread(p)

            if image is None:
                print("[INFO] deleting: {}".format(p))
                os.remove(p)
                continue
            total += 1

        except Exception as e:
            if type(e) in EXCEPTIONS:
                print("[INFO] skipping: {}".format(v["contentUrl"]))
                continue

# os._exit(0)
