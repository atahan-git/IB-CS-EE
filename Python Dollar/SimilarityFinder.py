from PointCloudRecognizer import PointCloudRecognizer
PointCloudRecognizer = PointCloudRecognizer();
from Point import Point
from Gesture import Gesture
import random
import xml.etree.ElementTree as ET
import time

gestureInputfile = "Edit/EditedData.xml"



#Experiment details
_gestureCount = 16
_trainingSampleCount = 3
_samplingResolution = 32
_greedyTrials = 0.5

#Processes input
tree = ET.parse(gestureInputfile)
root = tree.getroot()




#Actual Training



gestureCount = _gestureCount
trainingSampleCount = _trainingSampleCount
greedyTrials = _greedyTrials

def GetPoints (gesture):
    points = []
    strokeID = 0;
    for stroke in gesture[0]:
        for point in stroke[0]:
            points.append(Point(point.attrib["x"], point.attrib["y"], strokeID))
        strokeID += 1

    return points;


def InteralVarianceFinder(dataSet, samplingRes, DistanceMethod, gestureRepCount = 30, trials = 30):
    totalTrialCount = 0;
    totalDistance = 0;
    maxDistance = 0;

    #Setting up
    allGestures = []
    # import all gestures into an Array of Arrays
    for gesSet in dataSet:
        allGestures.append ([])
        for n in range (gestureRepCount):
            allGestures[len (allGestures) - 1].append (Gesture (GetPoints (gesSet[0][n]), gesSet.attrib["GroupName"], samplingRes))

    randIndex = []
    for n in range (gestureRepCount): randIndex.append (n);

    set1 = []
    set2 = []

    for n in range(int(gestureRepCount/2)):
        set1.append(None)
        set2.append(None)

    for trial in range(trials):
        print("trial: " + str(trial))

        for gesSetId in range(len(allGestures)):
            # random list to choose the training samples randomly
            random.shuffle (randIndex);
            for repId in range(gestureRepCount):
                if repId < gestureRepCount/2:
                    set1[repId] = (allGestures[gesSetId][randIndex[repId]])
                else:
                    set2[repId-int(gestureRepCount/2)] = (allGestures[gesSetId][randIndex[repId]])

        for gesId in range (len (set1)):
            distance = DistanceMethod(set1[gesId].Points, set2[gesId].Points,100)
            #print(matchName + " - " + checkSet[gesId].Name)
            totalTrialCount += 1
            totalDistance += distance
            maxDistance = max(maxDistance, distance)


    findings = {"samplingRes": samplingRes, "trialCount": trials, "gestureRepCount":gestureRepCount,
                "totalTrialCount":totalTrialCount, "totalDistance":totalDistance,  "maxDistance":maxDistance
                }
    return findings;

def InBetweenVarianceFinder(dataSet, samplingRes, DistanceMethod, gestureRepCount = 30, trials = 30):
    totalTrialCount = 0;
    totalDistance = 0;
    maxDistance = 0;

    #Setting up
    allGestures = []
    # import all gestures into an Array of Arrays
    for gesSet in dataSet:
        allGestures.append ([])
        for n in range (gestureRepCount):
            allGestures[len (allGestures) - 1].append (Gesture (GetPoints (gesSet[0][n]), gesSet.attrib["GroupName"], samplingRes))

    randIndex = []
    for n in range (gestureRepCount): randIndex.append (n);

    randIndexGesSet = []
    for n in range (len(allGestures)): randIndexGesSet.append (n);

    set1 = []
    set2 = []

    for n in range(int(gestureRepCount)):
        set1.append(None)
        set2.append(None)

    for trial in range(trials):
        print("trial: " + str(trial))

        for gesSetId in range(len(allGestures)):
            # random list to choose the training samples randomly
            random.shuffle (randIndex);
            for repId in range(gestureRepCount):
                set1[repId] = (allGestures[randIndexGesSet[repId % len(allGestures)]][randIndex[repId]])
                set2[repId] = (allGestures[randIndexGesSet[(repId+1) % len(allGestures)]][randIndex[repId]])

        for gesId in range (len (set1)):
            distance = DistanceMethod(set1[gesId].Points, set2[gesId].Points,100)
            #print(matchName + " - " + checkSet[gesId].Name)
            totalTrialCount += 1
            totalDistance += distance
            maxDistance = max(maxDistance, distance)


    findings = {"samplingRes": samplingRes, "trialCount": trials, "gestureRepCount":gestureRepCount,
                "totalTrialCount":totalTrialCount, "totalDistance":totalDistance,  "maxDistance":maxDistance
                }
    return findings;


import datetime
def WriteToFile (allResults):
    date = datetime.datetime.now ();
    dateStr = str (date.day) + "-" + str(date.month) + "-" + str(date.year) + " - " + str(date.hour) + "-" + str(date.minute);
    fNam = "Internal Variance Results"
    if curCoreExecNum == 1: fNam = "In Between Variance Results "
    f = open (fNam + str(curCoreExecNum) + " - " + dateStr + ".txt", "w+")
    #f.write("Test Name, Training Sample Count, Resampling Resolution, Test Trial Count, Gesture Copies Count, Total Trial count, One Trial Count, Total Match Count, Max Match Count, Min Match Count, Total Check Time, Total Exec Time, Min Check Time, Max Check Time" + "\n")
    for results in allResults:
        f.write(str(results["testName"]) + "," +
                str(results["samplingRes"]) + "," + str(results["trialCount"]) + "," + str(results["gestureRepCount"]) + "," +
                str(results["totalTrialCount"]) + "," + str(results["totalDistance"]) + "," + str(results["maxDistance"]) + "," +
                "\n")

curCoreExecNum = 1
allResults = []

if curCoreExecNum == 0:
    results = InteralVarianceFinder (root[1][1:17], 32, PointCloudRecognizer.GreedyCloudMatch, 46, 30);
    results["testName"] = "TestRun"
    print (results)
    allResults.append (results)
else:
    results = InBetweenVarianceFinder (root[1][1:17], 32, PointCloudRecognizer.GreedyCloudMatch, 46, 30);
    results["testName"] = "TestRun"
    print (results)
    allResults.append (results)

print ("The Results")
WriteToFile (allResults)

allResults.clear ()

if curCoreExecNum == 0:
    results = InteralVarianceFinder(root[1][1:16 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 46, 300);
    results["testName"] = "Basic Set"
    print (results)
    allResults.append(results)

    results = InteralVarianceFinder(root[1][44:53 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 46, 300);
    results["testName"] = "High Variability Set"
    print (results)
    allResults.append(results)

    results = InteralVarianceFinder(root[1][54:56 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 46, 300);
    results["testName"] = "Lines Set"
    print (results)
    allResults.append(results)

    results = InteralVarianceFinder(root[1][57:59 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 46, 300);
    results["testName"] = "Dash Set"
    print (results)
    allResults.append(results)

    results = InteralVarianceFinder(root[1][28:33 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 46, 300);
    results["testName"] = "Parenthesis Set"
    print (results)
    allResults.append(results)

    results = InteralVarianceFinder(root[1][34:36 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 46, 300);
    results["testName"] = "Tick Set"
    print (results)
    allResults.append(results)

    results = InteralVarianceFinder(root[1][10:11] + root[1][14:15] + root[1][88:89+1], 32, PointCloudRecognizer.GreedyCloudMatch, 46, 300);
    results["testName"] = "Star Set"
    print (results)
    allResults.append(results)

    results = InteralVarianceFinder(root[1][62:64+1] + root[1][66:67] + root[1][68:85+1], 32, PointCloudRecognizer.GreedyCloudMatch, 46, 300);
    results["testName"] = "Abstract Shapes Set"
    print (results)
    allResults.append(results)

    print ("The Results")
    WriteToFile (allResults)

if curCoreExecNum == 1:
    results = InBetweenVarianceFinder(root[1][1:16 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 30, 300);
    results["testName"] = "Basic Set"
    print (results)
    allResults.append(results)

    results = InBetweenVarianceFinder(root[1][44:53 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 30, 300);
    results["testName"] = "High Variability Set"
    print (results)
    allResults.append(results)

    results = InBetweenVarianceFinder(root[1][54:56 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 30, 300);
    results["testName"] = "Lines Set"
    print (results)
    allResults.append(results)

    results = InBetweenVarianceFinder(root[1][57:59 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 30, 300);
    results["testName"] = "Dash Set"
    print (results)
    allResults.append(results)

    results = InBetweenVarianceFinder(root[1][28:33 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 30, 300);
    results["testName"] = "Parenthesis Set"
    print (results)
    allResults.append(results)

    results = InBetweenVarianceFinder(root[1][34:36 + 1], 32, PointCloudRecognizer.GreedyCloudMatch, 30, 300);
    results["testName"] = "Tick Set"
    print (results)
    allResults.append(results)

    results = InBetweenVarianceFinder(root[1][10:11] + root[1][14:15] + root[1][88:89+1], 32, PointCloudRecognizer.GreedyCloudMatch, 30, 300);
    results["testName"] = "Star Set"
    print (results)
    allResults.append(results)

    results = InBetweenVarianceFinder(root[1][62:64+1] + root[1][66:67] + root[1][68:85+1], 32, PointCloudRecognizer.GreedyCloudMatch, 30, 300);
    results["testName"] = "Abstract Shapes Set"
    print (results)
    allResults.append(results)

    print ("The Results")
    WriteToFile (allResults)

