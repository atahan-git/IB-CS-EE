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

from Point import Point;
from Geometry import Geometry;
Geometry = Geometry();

# / <summary>
# / Implements a gesture as a cloud of points (i.e., an unordered set of points).
# / Gestures are normalized with respect to scale, translated to origin, and resampled into a fixed number of 32 points.
# / </summary>
class Gesture:
    Points = [];            # gesture points (normalized):
    Name = "";                      # gesture class
    SAMPLING_RESOLUTION = 32

    # / <summary>
    # / Constructs a gesture from an array of points
    # / </summary>
    # / <param name="points"></param>
    def __init__(self, points, gestureName = "", samplingRes = 32):
        self.Name = gestureName

        self.SAMPLING_RESOLUTION = int(samplingRes)

        #  normalizes the array of points with respect to scale, origin, and number of points
        self.Points = self.Scale(points)
        self.Points = self.TranslateTo(self.Points, self.Centroid(self.Points))
        self.Points = self.Resample(self.Points, self.SAMPLING_RESOLUTION)

    #region gesture pre-processing steps: scale normalization, translation to origin, and resampling

    # / <summary>
    # / Performs scale normalization with shape preservation into [0..1]x[0..1]
    # / </summary>
    # / <param name="points"></param>
    # / <returns></returns>
    def Scale(self, points):
        minx = float("inf")
        miny = float("inf")
        maxx = float("-inf")
        maxy = float("-inf")
        for i in range(len(points)):
            if minx > points[i].X: minx = points[i].X;
            if miny > points[i].Y: miny = points[i].Y;
            if maxx < points[i].X: maxx = points[i].X;
            if maxy < points[i].Y: maxy = points[i].Y;

        newPoints = []
        scale = max(maxx - minx, maxy - miny)
        for i in range(len(points)):
            newPoints.append(Point((points[i].X - minx) / scale, (points[i].Y - miny) / scale, points[i].StrokeID))
        return newPoints

    # / <summary>
    # / Translates the array of points by p
    # / </summary>
    # / <param name="points"></param>
    # / <param name="p"></param>
    # / <returns></returns>
    def TranslateTo(self, points, p):
        newPoints = []
        for i in range(len(points)):
            newPoints.append(Point(points[i].X - p.X, points[i].Y - p.Y, points[i].StrokeID))
        return newPoints

    # / <summary>
    # / Computes the centroid for an array of points
    # / </summary>
    # / <param name="points"></param>
    # / <returns></returns>
    def Centroid(self, points):
        cx = 0
        cy = 0
        for i in range(len(points)):
            cx += points[i].X
            cy += points[i].Y
        return Point(cx / len(points), cy / len(points), 0)

    # / <summary>
    # / Resamples the array of points into n equally-distanced points
    # / </summary>
    # / <param name="points"></param>
    # / <param name="n"></param>
    # / <returns></returns>
    def Resample(self, points, n):
        newPoints = []
        newPoints.append(Point(points[0].X, points[0].Y, points[0].StrokeID))
        numPoints = 1

        I = self.PathLength(points) / (n - 1) #  computes interval length
        D = 0
        for  i in range(1,len(points)):
            if points[i].StrokeID == points[i - 1].StrokeID:
                d = Geometry.EuclideanDistance(points[i - 1], points[i])
                if D + d >= I:
                    firstPoint = points[i - 1]
                    while D + d >= I:
                        #  add interpolated point
                        t = min(max((I - D) / d, 0.0), 1.0);
                        if t is None: t = 0.5;
                        numPoints += 1;
                        newPoints.append(Point(
                            (1.0 - t) * firstPoint.X + t * points[i].X,
                            (1.0 - t) * firstPoint.Y + t * points[i].Y,
                            points[i].StrokeID
                        ))

                        #  update partial length
                        d = D + d - I
                        D = 0
                        firstPoint = newPoints[numPoints - 1]
                    D = d
                else: D += d

        if numPoints == n - 1: # sometimes we fall a rounding-error short of adding the last point, so add it if s:
            newPoints.append(Point(points[len(points) - 1].X, points[len(points) - 1].Y, points[len(points) - 1].StrokeID))
        return newPoints

    # / <summary>
    # / Computes the path length for an array of points
    # / </summary>
    # / <param name="points"></param>
    # / <returns></returns>
    def PathLength(self, points):
        length = 0
        for i in range(1, len(points)):
            if points[i].StrokeID == points[i - 1].StrokeID:
                length += Geometry.EuclideanDistance(points[i - 1], points[i])
        return length

    #endregion
