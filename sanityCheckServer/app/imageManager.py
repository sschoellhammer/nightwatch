import os

def makeList(l):
    if not isinstance(l, list):
        l = list(l)
    return l

def filterByFiletype(files,exts):
    exts = makeList(exts)
    for i in range(len(exts)):
        exts[i] = exts[i].lower()
    filteredFiles = []

    for filename in files:
        filenameNoExt, ext = os.path.splitext(filename)
        ext = ext[1:]
        if ext.lower() in exts:
            filteredFiles.append(filename)
    return filteredFiles


class ScreenShot(object):
    def __init__(self, buildNumber, sceneName, deviceName, filename):
        self.buildNumber = buildNumber
        self.sceneName = sceneName
        self.deviceName = deviceName
        self.filename = filename
    def __repr__(self):
        return "Screenshot \nBuildnumber: {0}\nSceneName: {1}\nDeviceName: {2}\nFilename: {3}\n".format(self.buildNumber, self.sceneName,self.deviceName,self.filename)



def getScreenShotFromFilename(filename):
    filenameNoExt = os.path.splitext(filename)[0]
    bits = filenameNoExt.split("_")
    buildNumber = bits[1]
    deviceName = bits[2]
    sceneName = "_".join(bits[3:])
    print sceneName
    #x, buildNumber, deviceName, sceneName = filenameNoExt.split("_")
    screenShot = ScreenShot(int(buildNumber), sceneName, deviceName, filename)
    return screenShot


class ImageManager(object):
    def __init__(self, folder):
        self.latestBuildNumber = 0
        self.sceneNames = []
        self.readImages(folder)



    def readImages(self, folder):
        self.screenShotDict = {}
        self.screenShots = []
        if not os.path.isdir(folder):
            return []
        filenames = filterByFiletype(os.listdir(folder), ["png"])

        deviceNames = set()

        for filename in filenames:
            screenShot = getScreenShotFromFilename(filename)
            deviceNames.add(screenShot.deviceName)
            self.screenShotDict["{0}_{1}_{2}".format(screenShot.buildNumber, screenShot.deviceName, screenShot.sceneName)] = screenShot
            self.screenShots.append(screenShot)
            if screenShot.sceneName not in self.sceneNames:
                self.sceneNames.append(screenShot.sceneName)

            if screenShot.buildNumber > self.latestBuildNumber:
                self.latestBuildNumber = screenShot.buildNumber
        self.deviceNames = list(deviceNames)



    def getScreenShotFromValues(self, buildNumber, deviceName, sceneName):
        hash = "{0}_{1}_{2}".format(buildNumber, deviceName, sceneName)
        return self.screenShotDict.get(hash, None)


    def getPreviousImage(self, filename):
        screenShot = getScreenShotFromFilename(filename)
        previousBuildNumber = -1
        previousScreenShot = None;
        for otherScreenShot in self.screenShots:
            if (otherScreenShot.sceneName == screenShot.sceneName) and  otherScreenShot.deviceName == screenShot.deviceName and otherScreenShot.buildNumber < screenShot.buildNumber:
                if otherScreenShot.buildNumber > previousBuildNumber:
                    previousBuildNumber = otherScreenShot.buildNumber
                    previousScreenShot = otherScreenShot

        if previousBuildNumber == -1:
            return None

        return previousScreenShot

    def getRenderData(self, numBuilds, sceneName):
        class RenderData(object):
            def __init__(self ):
                self.buildNumbers = []
                self.images = []  # table
                self.deviceNames = []


        images = []
        buildNumbers = []
        for i in range(self.latestBuildNumber, max(0, self.latestBuildNumber-numBuilds)-1, -1):

            buildNumbers.append(i)

            row = []
            for j in range(len(self.deviceNames)):
                screenShot = self.getScreenShotFromValues(i, self.deviceNames[j], sceneName)
                if screenShot is None:
                    row.append("missing.jpg")
                else:
                    row.append(screenShot.filename)
            images.append(row)

        data = RenderData()
        data.images = images
        data.deviceNames = self.deviceNames
        data.buildNumbers = buildNumbers
        return data


import PIL
from PIL import Image,ImageChops
import operator
import math


def hasShaderError(filename):
    img = Image.open(filename)
    pixels = list(img.getdata())
    cnt = 0
    for i in range(len(pixels)):
        if pixels[i] == (255,0,255,255):
            cnt += 1

        if cnt > 5:
            return True
    return False


def compareImages(filename1, filename2):
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)

    h = ImageChops.difference(img1, img2).histogram()

    sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(img1.size[0] * img1.size[1]))

    return rms





#im = ImageManager("/Users/sebastianschoellhammer/Documents/PyCharmProjects/SanitySuit/app/static/imageUploads")
#print im.getRenderData(2, "TestScene1")

#print hasShaderError("/Users/sebastianschoellhammer/Documents/PyCharmProjects/SanitySuit/app/static/imageUploads/screenShot_6_SebsMac_TestScene1.png")

#compareImages("/Users/sebastianschoellhammer/Documents/PyCharmProjects/SanitySuit/app/static/imageUploads/screenShot_0_SebsMac_TestScene1.png",
 #             "/Users/sebastianschoellhammer/Documents/PyCharmProjects/SanitySuit/app/static/imageUploads/screenShot_7_SebsMac_TestScene1.png")