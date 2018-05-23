foo = open("/home/sovereign/PycharmProjects/AdaboostCarNumberPlate/data/negative.txt", "r")
for test in foo.readlines():
    test.replace(old="negative", new="/home/sovereign/PycharmProjects/AdaboostCarNumberPlate/data/")