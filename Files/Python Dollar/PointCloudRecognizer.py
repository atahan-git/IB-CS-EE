"""*
 * The $P Point-Cloud Recognizer (.NET Framework 4.0 C# version)
 *
 *         Radu-Daniel Vatavu, Ph.D.
 *        University Stefan cel Mare of Suceava
 *        Suceava 720229, Romania
 *        vatavu@eed.usv.ro
 *
 *        Lisa Anthony, Ph.D.
 *      UMBC
 *      Information Systems Department
 *      1000 Hilltop Circle
 *      Baltimore, MD 21250
 *      lanthony@umbc.edu
 *
 *        Jacob O. Wobbrock, Ph.D.
 *         The Information School
 *        University of Washington
 *        Seattle, WA 98195-2840
 *        wobbrock@uw.edu
 *
 * The academic publication for the $P recognizer, and what should be 
 * used to cite it, is:
 *
 *    Vatavu, R.-D., Anthony, L. and Wobbrock, J.O. (2012).  
 *      Gestures as point clouds: A $P recognizer for user interface 
 *      prototypes. Proceedings of the ACM Int'l Conference on  
 *      Multimodal Interfaces (ICMI '12). Santa Monica, California  
 *      (October 22-26, 2012). New York: ACM Press, pp. 273-280.
 *
 * This software is distributed under the "New BSD License" agreement:
 *
 * Copyright (c) 2012, Radu-Daniel Vatavu, Lisa Anthony, and 
 * Jacob O. Wobbrock. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *    * Redistributions of source code must retain the above copyright
 *      notice, this list of conditions and the following disclaimer.
 *    * Redistributions in binary form must reproduce the above copyright
 *      notice, this list of conditions and the following disclaimer in the
 *      documentation and/or other materials provided with the distribution.
 *    * Neither the names of the University Stefan cel Mare of Suceava, 
 *        University of Washington, nor UMBC, nor the names of its contributors 
 *        may be used to endorse or promote products derived from this software 
 *        without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Radu-Daniel Vatavu OR Lisa Anthony
 * OR Jacob O. Wobbrock BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
*"""
from Gesture import Gesture;
# / <summary>
# / Implements the $P recognizer
# / </summary>
import math;
from Geometry import Geometry;
Geometry = Geometry();

class PointCloudRecognizer:
    # / <summary>
    # / Main function of the $P recognizer.
    # / Classifies a candidate gesture against a set of training samples.
    # / Returns the class of the closest neighbor in the training set.
    # / </summary>
    # / <param name="candidate"></param>
    # / <param name="trainingSet"></param>
    # / <returns></returns>
    def GreedyClassify(self, candidate,  trainingSet):
        minDistance = float("inf")
        gestureClass = ""
        for template in trainingSet:
            dist = self.GreedyCloudMatch(candidate.Points, template.Points, minDistance)
            if dist < minDistance:
                minDistance = dist
                gestureClass = template.Name
        return gestureClass

    def PlusClassify (self, candidate, trainingSet):
        print("implement plox")

    # / <summary>
    # / Implements greedy search for a minimum-distance matching between two point clouds
    # / </summary>
    # / <param name="points1"></param>
    # / <param name="points2"></param>
    # / <returns></returns>
    def GreedyCloudMatch(self, points1, points2, minFoundDist):
        n = len(points1) #  the two clouds should have the same number of points by now
        eps = 0.5;       # controls the number of greedy search trials (eps is in [0..1])
        step = int(math.floor(pow(n, 1.0 - eps)))
        minDistance = float("inf")
        for i in range (0, n, step):
            dist1 = self.CloudDistance(points1, points2, i, minFoundDist);   # match points1 --> points2 starting with index point i
            dist2 = self.CloudDistance(points2, points1, i, minFoundDist);   # match points2 --> points1 starting with index point i
            minDistance = min(minDistance, min(dist1, dist2))
        return minDistance

    # / <summary>
    # / Computes the distance between two point clouds by performing a minimum-distance greedy matching
    # / starting with point startIndex
    # / </summary>
    # / <param name="points1"></param>
    # / <param name="points2"></param>
    # / <param name="startIndex"></param>
    # / <returns></returns>
    def CloudDistance(self, points1, points2, startIndex, minFoundDist):
        n = len(points1);       # the two clouds should have the same number of points by now
        matched = [] #  matched[i] signals whether point i from the 2nd cloud has been already matched
        for i in range(n): matched.append(False),

        sum = 0;  # computes the sum of distances between matched points (i.e., the distance between the two clouds)
        i = startIndex + 1
        isFirst = True
        while i != startIndex:
            if sum > minFoundDist:
                break;

            if isFirst:
                isFirst = False
                i = startIndex;

            index = -1
            minDistance = float("inf")
            for j in range(n):
                if not matched[j]:
                    dist = Geometry.SqrEuclideanDistance(points1[i], points2[j]);  # use squared Euclidean distance to save some processing time
                    if dist < minDistance:
                        minDistance = dist
                        index = j
            matched[index] = True #  point index from the 2nd cloud is matched to point i from the 1st cloud
            weight = 1.0 - ((i - startIndex + n) % n) / (1.0 * n)
            sum += weight * minDistance #  weight each distance with a confidence coefficient that decreases from 1 to 0
            i = (i + 1) % n
        return sum
