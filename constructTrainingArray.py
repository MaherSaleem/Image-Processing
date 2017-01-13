import cv2
from addPadding import *
from dividingImage import *
from pickleAndUnpickle import *
from testingAndTrainingPaths import *
from settings import *
from skimage.io import sift
from matplotlib import pyplot as plt






def constructTrainingArray(keyPointsFileName, partitioningType):
    print("Constructing the database:")
    fontsList=["AdvertisingBold", "andalus", "Arabic Transparent", "DecoType Naskh","DecoType Thuluth","Diwani Letter",
               "M Unicode Sara","Simplified Arabic"]
    trainingDataPathsForAllFonts = []
    for font in fontsList:
        trainingDataPathsForOneFont = getTrainingImagesPaths(Font=font)
        trainingDataPathsForAllFonts.append(trainingDataPathsForOneFont)
    listForAllFonts=[]
    i = 0
    for eachFont in trainingDataPathsForAllFonts:
        listForFont = []
        for eachChar in eachFont:
            j = 0
            listForChar = []
            for eachShape in eachChar:
                listForShape = []
                img = cv2.imread(eachShape, 0)
                # cv2.imshow('img'+str(i),img)
                # cv2.waitKey(0)
                paddedImage = addPadding(img, horizontalPadding, verticalPadding)
                # cv2.imshow('img'+str(i+1),paddedImage)
                # cv2.waitKey(0)
                if partitioningType=="constant":
                    parts = divideImage(paddedImage, n, m)
                # elif partitioningType == "sliding":
                #     parts = slidingWindow(paddedImage)

                ImagePartsKeyPoints_array = []
                for part in parts:
                    subImage = getSubImageData(paddedImage, part)
                    # Initiate SIFT detector
                    sift = cv2.xfeatures2d.SIFT_create()
                    kp1, des1 = sift.detectAndCompute(subImage, None)
                    temp = pickle_keypoints(kp1, des1)
                    listForShape.append(temp)
                    # listForShape.append([kp1,des1])
                    # Initiate ORB detector
                    # orb = cv2.ORB_create()
                    # find the keypoints and descriptors with ORB
                    # kp1, des1 = orb.detectAndCompute(subImage, None)
                listForChar.append(listForShape)
            listForFont.append(listForChar)
        listForAllFonts.append(listForFont)
    # print(listForAllFonts[0][1])
    storeToFile(keyPointsFileName, listForAllFonts)
    print("Database is successfully constructed")