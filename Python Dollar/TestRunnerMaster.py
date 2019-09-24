from PointCloudRecognizer import PointCloudRecognizer
PointCloudRecognizer = PointCloudRecognizer();
from Point import Point
from Gesture import Gesture
import random
import xml.etree.ElementTree as ET
import time

gestureInputfile = "Edit/EditedData.xml"
#Processes input
tree = ET.parse(gestureInputfile)
root = tree.getroot()

#helper methods
def GetPoints (gesture):
    points = []
    strokeID = 0;
    for stroke in gesture[0]:
        for point in stroke[0]:
            points.append(Point(point.attrib["x"], point.attrib["y"], strokeID))
        strokeID += 1

    return points;

#main test method
def DoTesting(dataSet, traSampleCount, samplingRes, TesterMethod, gestureRepCount = 30, trials = 10):
    totalTrialCount = 0;
    totalMatchCount = 0;

    oneTrialCount = 0;
    minMatchCount = len(dataSet)*gestureRepCount;
    maxMatchCount = 0;

    totalCheckTime = 0;
    minCheckTime = 10;
    maxCheckTime = 0;

    totalExecTime = 0;

    #Setting up
    allGestures = []
    # import all gestures into an Array of Arrays
    for gesSet in dataSet:
        allGestures.append ([])
        for n in range (gestureRepCount):
            allGestures[len (allGestures) - 1].append (Gesture (GetPoints (gesSet[0][n]), gesSet.attrib["GroupName"], samplingRes))

    randIndex = []
    for n in range (gestureRepCount): randIndex.append (n);

    # training data
    trainingSet = []
    # data to check
    checkSet = []

    for gesSetId in range (len (allGestures)):
        for repId in range (gestureRepCount):
            if repId < traSampleCount:
                trainingSet.append (None)
            else:
                checkSet.append (None)
    #/Setting up

    for trial in range(trials):
        triStart = time.time ()
        print("trial: " + str(trial))

        traCounter = 0
        checkCounter = 0
        for gesSetId in range(len(allGestures)):
            # random list to choose the training samples randomly
            random.shuffle (randIndex);
            for repId in range(gestureRepCount):
                if repId < traSampleCount:
                    trainingSet[traCounter] = (allGestures[gesSetId][randIndex[repId]])
                    traCounter += 1
                else:
                    checkSet[checkCounter] = (allGestures[gesSetId][randIndex[repId]])
                    checkCounter += 1

        oneTrialCount = len(checkSet)
        curMatchCount = 0;
        for gesId in range(len(checkSet)):
            if(gesId % min( int( (len(checkSet) / 5) + 1), 50) == 0):
                print("tra sampl #:" + str(traSampleCount) + " - re sampl #:" + str(samplingRes) + " - trial id:" + str(trial) + " - gesture id: " + str(gesId) + "/" + str(len(checkSet)))
            start = time.time ()
            matchName = TesterMethod(checkSet[gesId],trainingSet)
            end = time.time ()
            #if (gesId % 50 == 0): print("Average time:" + str(end-start))
            checkTime = end-start;
            totalCheckTime += checkTime
            minCheckTime = min(minCheckTime, checkTime)
            maxCheckTime = max(maxCheckTime, checkTime)
            #print(matchName + " - " + checkSet[gesId].Name)
            if( matchName == checkSet[gesId].Name):
                curMatchCount += 1;
            #else:
                #print (matchName + " - " + checkSet[gesId].Name)

        totalTrialCount += oneTrialCount;
        totalMatchCount += curMatchCount;
        minMatchCount = min(minMatchCount,curMatchCount);
        maxMatchCount = max(maxMatchCount,curMatchCount);
        triEnd = time.time ()
        trialTime = triEnd-triStart
        totalExecTime += trialTime
        print("Est Time Remaining: " + "{:.3f}".format(trialTime*(trials-trial-1)) + " - trial time: " + "{:.3f}".format(trialTime))
    findings = {"traSampleCount": traSampleCount, "samplingRes": samplingRes, "trialCount": trials, "gestureRepCount":gestureRepCount,
                "totalTrialCount":totalTrialCount, "oneTrialCount":oneTrialCount,
                "totalMatchCount":totalMatchCount, "maxMatchCount": maxMatchCount, "minMatchCount":minMatchCount,
                "totalCheckTime":totalCheckTime, "totalExecTime":totalExecTime, "minCheckTime":minCheckTime, "maxCheckTime":maxCheckTime
                }
    return findings;


def printResults(results):
    avgTestTime = results["totalCheckTime"] / results["totalTrialCount"];
    print ("Test Name: " + str(results["testName"]) + "\n" +
            "Training Sample Count: " + str (results["traSampleCount"]) + " - Resampling Resolution: " + str (results["samplingRes"]) +
           " - Trial Count: " + str (results["trialCount"]) + " - Gesture Repetition Count: " + str (results["gestureRepCount"])+ "\n" +
           "Accuracy: " + "{:.3f}".format((results["totalMatchCount"] / results["totalTrialCount"]) * 100) + "%" + "\n" +
           "minMatchCount: " + str(results["minMatchCount"]) + "/" + str(results["oneTrialCount"]) + " - maxMatchCount: " + str(results["maxMatchCount"]) + "/" + str(results["oneTrialCount"]) + "\n" +
           "Time Per Check: " + "{:.3f}".format(avgTestTime) + "s - Total Test Time: " + "{:.3f}".format(results["totalExecTime"]) + "\n" +
           "minCheckTime: " + "{:.3f}".format(results["minCheckTime"])+ "/" + "{:.3f}".format(avgTestTime) + " - maxCheckTime: " + "{:.3f}".format(results["maxCheckTime"])+ "/" + "{:.3f}".format(avgTestTime) + "\n")


import datetime
def WriteToFile (allResults):
    date = datetime.datetime.now ();
    dateStr = str (date.day) + "-" + str(date.month) + "-" + str(date.year) + " - " + str(date.hour) + "-" + str(date.minute);
    f = open ("data " + str(curCoreExecNum) + " - " + dateStr + ".txt", "w+")
    #f.write("Test Name, Training Sample Count, Resampling Resolution, Test Trial Count, Gesture Copies Count, Total Trial count, One Trial Count, Total Match Count, Max Match Count, Min Match Count, Total Check Time, Total Exec Time, Min Check Time, Max Check Time" + "\n")
    for results in allResults:
        f.write(str(results["testName"]) + "," +
                str(results["traSampleCount"]) + "," + str(results["samplingRes"]) + "," + str(results["trialCount"]) + "," + str(results["gestureRepCount"]) + "," +
                str(results["totalTrialCount"]) + "," + str(results["oneTrialCount"]) + "," +
                str (results["totalMatchCount"]) + "," + str(results["maxMatchCount"]) + "," + str(results["minMatchCount"]) + "," +
                str (results["totalCheckTime"]) + "," + str(results["totalExecTime"]) + "," + str(results["minCheckTime"]) + "," + str(results["maxCheckTime"])
                + "\n")

curCoreExecNum = 5
allResults = []


for n in range (1, 2):
    results = DoTesting (root[1][1:17], n, 8, PointCloudRecognizer.GreedyClassify, 10, 2);
    results["testName"] = "TestRun"
    print (results)
    printResults (results)
    allResults.append (results)

print ("The Results")
WriteToFile (allResults)
for results in allResults:
    printResults (results)


if curCoreExecNum == 0:
    #----------------------------------------------------------------------------------------------Main Set Tests
    allResults.clear ()
    for n in range(1, 9):
        results = DoTesting(root[1][1:16+1], n, 32, PointCloudRecognizer.GreedyClassify, 30, 10);
        results["testName"] = "Main Set - TraSamp 1-8"
        print (results)
        printResults(results)
        allResults.append(results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)


    allResults.clear()
    for n in range(1,7):
        results = DoTesting (root[1][1:16+1], 2, pow(2,n), PointCloudRecognizer.GreedyClassify, 30, 10);
        results["testName"] = "Main Set - ReSamp 1-6"
        print (results)
        printResults (results)
        allResults.append (results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)

    #----------------------------------------------------------------------------------------------High Variability set tests
    allResults.clear()
    for n in range(1, 9):
        results = DoTesting(root[1][44:53+1], n, 32, PointCloudRecognizer.GreedyClassify, 30, 10);
        results["testName"] = "HighVar Set - TraSamp 1-8"
        print (results)
        printResults(results)
        allResults.append(results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)


    allResults.clear()
    for n in range(1,8):
        results = DoTesting (root[1][44:53+1], 2, pow(2,n), PointCloudRecognizer.GreedyClassify, 30, 10);
        results["testName"] = "HighVar Set - ReSamp 1-7"
        print (results)
        printResults (results)
        allResults.append (results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)

if curCoreExecNum == 1:
    #----------------------------------------------------------------------------------------------Lines Set Tests
    allResults.clear ()
    for n in range(1, 11):
        results = DoTesting(root[1][54:56+1], n, 32, PointCloudRecognizer.GreedyClassify, 45, 15);
        results["testName"] = "Lines Set - TraSamp 1-10"
        print (results)
        printResults(results)
        allResults.append(results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)


    allResults.clear()
    for n in range(1,8):
        results = DoTesting (root[1][54:56+1], 2, pow(2,n), PointCloudRecognizer.GreedyClassify, 45, 15);
        results["testName"] = "Lines Set - ReSamp 1-7"
        print (results)
        printResults (results)
        allResults.append (results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)

if curCoreExecNum == 2:
    # ----------------------------------------------------------------------------------------------Dash Set Tests
    allResults.clear ()
    for n in range (1, 11):
        results = DoTesting (root[1][57:59 + 1], n, 32, PointCloudRecognizer.GreedyClassify, 45, 15);
        results["testName"] = "Dash Set - TraSamp 1-10"
        print (results)
        printResults (results)
        allResults.append (results)

    print ("The Results")
    WriteToFile (allResults)
    for results in allResults:
        printResults (results)

    allResults.clear ()
    for n in range (1, 8):
        results = DoTesting (root[1][57:59 + 1], 2, pow (2, n), PointCloudRecognizer.GreedyClassify, 45, 15);
        results["testName"] = "Dash Set - ReSamp 1-7"
        print (results)
        printResults (results)
        allResults.append (results)

    print ("The Results")
    WriteToFile (allResults)
    for results in allResults:
        printResults (results)

if curCoreExecNum == 3:
    #----------------------------------------------------------------------------------------------Parenthesis Set Tests
    allResults.clear ()
    for n in range(1, 9):
        results = DoTesting(root[1][28:33+1], n, 32, PointCloudRecognizer.GreedyClassify, 30, 15);
        results["testName"] = "Parenthesis Set - TraSamp 1-8"
        print (results)
        printResults(results)
        allResults.append(results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)


    allResults.clear()
    for n in range(1,7):
        results = DoTesting (root[1][28:33+1], 2, pow(2,n), PointCloudRecognizer.GreedyClassify, 30, 15);
        results["testName"] = "Parenthesis Set - ReSamp 1-6"
        print (results)
        printResults (results)
        allResults.append (results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)

    # ----------------------------------------------------------------------------------------------Dashes Set Tests
    allResults.clear ()
    for n in range (1, 9):
        results = DoTesting (root[1][34:36 + 1], n, 16, PointCloudRecognizer.GreedyClassify, 45, 15);
        results["testName"] = "Dashes Set - TraSamp 1-8"
        print (results)
        printResults (results)
        allResults.append (results)

    print ("The Results")
    WriteToFile (allResults)
    for results in allResults:
        printResults (results)

    allResults.clear ()
    for n in range (1, 7):
        results = DoTesting (root[1][34:36 + 1], 2, pow (2, n), PointCloudRecognizer.GreedyClassify, 45, 15);
        results["testName"] = "Dashes Set - ReSamp 1-6"
        print (results)
        printResults (results)
        allResults.append (results)

    print ("The Results")
    WriteToFile (allResults)
    for results in allResults:
        printResults (results)

if curCoreExecNum == 4:
    #----------------------------------------------------------------------------------------------Star Set Tests
    allResults.clear ()
    for n in range(1, 11):
        results = DoTesting(root[1][10:11] + root[1][14:15] + root[1][88:89+1], n, 32, PointCloudRecognizer.GreedyClassify, 45, 15);
        results["testName"] = "Star Set - TraSamp 1-10"
        print (results)
        printResults(results)
        allResults.append(results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)


    allResults.clear()
    for n in range(1,8):
        results = DoTesting (root[1][10:11] + root[1][14:15] + root[1][88:89+1], 2, pow(2,n), PointCloudRecognizer.GreedyClassify, 45, 15);
        results["testName"] = "Star Set - ReSamp 1-7"
        print (results)
        printResults (results)
        allResults.append (results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)

if curCoreExecNum == 5:
    #----------------------------------------------------------------------------------------------Abstract Shapes Set Tests
    allResults.clear ()
    for n in range(1, 11):
        results = DoTesting(root[1][62:64+1] + root[1][66:67] + root[1][68:85+1], n, 32, PointCloudRecognizer.GreedyClassify, 30, 10);
        results["testName"] = "Abstract Shapes Set - TraSamp 1-10"
        print (results)
        printResults(results)
        allResults.append(results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)


    allResults.clear()
    for n in range(1,7):
        results = DoTesting (root[1][62:64+1] + root[1][66:67] + root[1][68:85+1], 2, pow(2,n), PointCloudRecognizer.GreedyClassify, 30, 10);
        results["testName"] = "Abstract Shapes Set - ReSamp 1-6"
        print (results)
        printResults (results)
        allResults.append (results)

    print("The Results")
    WriteToFile(allResults)
    for results in allResults:
        printResults (results)
