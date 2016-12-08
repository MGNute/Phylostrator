#ifndef TREEOPS_UTILS_H
#define TREEOPS_UTILS_H

double distToLineSegment(double px, double py, double x1, double y1, double x2, double y2);
int doIntersect(double x1, double y1, double x2, double y2, double x3, double y3, double x4, double y4);
double dist(double x1, double y1, double x2, double y2);
void swapDoublePoints(double* p1, double* p2);
double rightTurnAngle(double x1, double y1, double x2, double y2, double x3, double y3);
double getRotationalAngleToSegment(double* origin, double* radial_pt, double* seg_p1, double* seg_p2);
double distPtToLine(double px, double py, double x1, double y1, double x2, double y2);
double sq(double x);

#endif