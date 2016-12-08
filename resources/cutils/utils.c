#include<stdio.h>
#include<stdlib.h>
#include<math.h>

#include "utils.h"

double distToLineSegment(double px, double py, double x1, double y1, double x2, double y2)
{
    double diffx, diffy, v1x, v1y, v2x, v2y;
    diffx = x2 - x1;
    diffy = y2 - y1; 
    v1x = px - x1;
    v1y = py - y1;
    v2x = px - x2;
    v2y = py - y2;
    
    if ((v1x*diffx + v1y*diffy)*(v2x*diffx+v2y*diffy) <0)
    {
        return fabs((y2-y1)*px - (x2-x1)*py + x2*y1 - y2*x1)/hypot(x1-x2,y1-y2);
    } else {
        //recycling these doubles since they've been allocated
        // diffx = dist(px, py, x1, y1);
        diffx = hypot(px-x1, py- y1);
        // diffy = dist(px, py, x2, y2);
        diffy = hypot(px-x2, py- y2);
        return (diffx > diffy ? diffy : diffx);
    }
}

double distPtToLine(double px, double py, double x1, double y1, double x2, double y2)
{
    // similar to the function above but ignores special cases related to line segments
    double diffx, diffy, v1x, v1y, v2x, v2y;
    diffx = x2 - x1;
    diffy = y2 - y1; 
    v1x = px - x1;
    v1y = py - y1;
    v2x = px - x2;
    v2y = py - y2;
    
    return fabs((y2-y1)*px - (x2-x1)*py + x2*y1 - y2*x1)/hypot(x1-x2,y1-y2);
}

double dist(double x1, double y1, double x2, double y2)
{
    return hypot(x1-x2,y1-y2);
}

int doIntersect(double x1, double y1, double x2, double y2, double x3, double y3, double x4, double y4)
{
    // if either segment is actually just a point, return false
    double t1, t2, determ;
    // double zero = 0.0;
    // double one = 1.0;
    
    if ((x1-x2)==0.0 && (y1-y2)==0.0) {
        // printf("\tcase 8\t"); //DEBUG 
        return 0;
    }
    if ((x3-x4)==0.0 && (y3-y4)==0.0) {
        // printf("\tcase 9\t"); //DEBUG
        return 0;
    }
    
    determ = (x2-x1)*(y3-y4)-(x3-x4)*(y2-y1);
    // printf("determ: %f\n", determ);
    
    // if the lines are parallel, check cases:
    if (determ==0.0) 
    {
        if (x2-x1==0.0)   // lines are vertical
        {
            if (x3==x2)
            {
                t1 = (y3-y1) / (y2-y1);
                t2 = (y4-y1) / (y2-y1);
                // printf("\tcase 1\t"); //DEBUG
                return ((t1 > 0 && t1 < 1) || (t2 > 0 && t2 < 1));
            } else {
                // printf("\tcase 2\t"); //DEBUG
                return 0;
            }
        } else if (y2 - y1==0.0) {
            // lines are horizontal
            if (y3==y2)
            {
                t1 = (x3-x1) / (x2-x1);
                t2 = (x4-x1) / (x2-x1);
                // printf("\tcase 3\t"); //DEBUG
                return ((t1 > 0 && t1 < 0.9999999999999) || (t2 > 0 && t2 < 0.9999999999999));
            } else {
                // printf("\tcase 4\t"); //DEBUG
                return 0;
            }            
        } else {
            t1 = (x3-x1) / (x2-x1);
            t2 = (y3-y1) / (y2-y1);
            if (t1==t2 && t1 >0 && t2 > 0 && t1 < 0.9999999999999&& t2 < 0.9999999999999) {
                // printf("\tcase 5\t");  //DEBUG
                return 1;
            }
            t1 = (x4-x1) / (x2-x1);
            t2 = (y4-y1) / (y2-y1);
            if (t1==t2 && t1 >0 && t2 > 0 && t1 < 0.9999999999999 && t2 < 0.9999999999999) {
                // printf("\tcase 6\t");  //DEBUG
                return 1;
            } else {
                // printf("\tcase 7\t");  //DEBUG
                return 0;
            }
        }
    }
    
    t1 = ((y3-y4)*(x3-x1)+(x4-x3)*(y3-y1))/determ;
    t2 = ((y1-y2)*(x3-x1)+(x2-x1)*(y3-y1))/determ;
    // printf("\tt1: %e\tt2: %e\n", t1,t2); //DEBUG

    if (t1 > 0 && t1 < 0.9999999999999 && t2 > 0 && t2 < 0.9999999999999)
    {
        return 1;
    } else {
        return 0;
    }
}

void swapDoublePoints(double* p1, double* p2)
{
    double x, y;
    x=p1[0];
    y=p1[1];
    p1[0]=p2[0];
    p1[1]=p2[1];
    p2[0]=x;
    p2[1]=y;
}

double sq(double x)
{
    return x*x;
}

double rightTurnAngle(double x1, double y1, double x2, double y2, double x3, double y3)
{
    // for points p1 = (x1, y1), ... , p3 = (x3,y3), returns the angle between p1p2 and p2p3. Negative means a right turn
    // (i.e. clockwise) positive means a left turn (counterclockwise).
    double d12, d23, xprod, dprod, theta;
    d12 = hypot(x2-x1,y2-y1);
    d23 = hypot(x3-x2,y3-y2);
    xprod = (x1-x2)*(y3-y2)-(y1-y2)*(x3-x2);
    dprod = ((x1-x2)*(x3-x2)+(y3-y2)*(y1-y2))/(d12*d23);
    // printf("xpr: %f\tdpr: %f\td12: %f\td23: %f\n",xprod, dprod, d12, d23);
    return (xprod<0 ? -acos(dprod) : acos(dprod));
}

double getRotationalAngleToSegment(double* origin, double* radial_pt, double* seg_p1, double* seg_p2)
{
    double rad, dp1, dp2;

    rad = hypot(origin[0]-radial_pt[0],origin[1]-radial_pt[1]);
    double d_eps = rad*1.0e-12;
    dp1 = hypot(origin[0]-seg_p1[0],origin[1]-seg_p1[1]);
    dp2 = hypot(origin[0]-seg_p2[0],origin[1]-seg_p2[1]);
    // printf("rad = %f\tdp1 = %f\tdp2 = %f\td_eps = %f\n",rad,dp1,dp2,d_eps);
    
    double t1, t2, a0,b0, a1, b1, x0,y0, A,B,C, xnew, ynew, ang1, ang2,dts;


    // if the origin happens to be one of the two segments, that is a special case:
    if (dp1<d_eps) {
        // printf("p1 = origin\n");
        return rightTurnAngle(radial_pt[0],radial_pt[1],origin[0], origin[1], seg_p2[0], seg_p2[1]);
    }
    if (dp2<d_eps) {
        // printf("p2 = origin\n");
        return rightTurnAngle(radial_pt[0],radial_pt[1],origin[0], origin[1], seg_p1[0], seg_p1[1]);
    } 

    

    // if the radius does not intersect along the line segment, return NaN unless it hits one of the endpoints.
    //    - this happens to also exclude cases where origin and rad pt are separated by the p12 segment
    // if (!(((dp1<=rad) &&(rad<=dp2)) || ((dp2<=rad) &&(rad<=dp1))))
    dts = distToLineSegment(origin[0],origin[1],seg_p1[0],seg_p1[1],seg_p2[0], seg_p2[1]);
    // printf("dts: %f\n",dts);
    if (rad < dts) 
    {
        a0 = nan(""); a1 = nan("");

        // check the endpoints:
        if (dp1<=rad) a0 = rightTurnAngle(radial_pt[0],radial_pt[1],origin[0], origin[1], seg_p1[0], seg_p1[1]);
        if (dp2<=rad) a1 = rightTurnAngle(radial_pt[0],radial_pt[1],origin[0], origin[1], seg_p2[0], seg_p2[1]);
        if (!isnan(a0) && !isnan(a1))
        {
            return (fabs(a0)>fabs(a1) ? a1 : a0);
        } else if (!isnan(a0)) {
            return a0;
        } else if (!isnan(a1)) {
            return a1;
        } else {
            return nan("");
        }
    }


    // otherwise find the intersection point
    
    a0 = seg_p1[0]; b0 = seg_p1[1];
    a1 = seg_p2[0]; b1 = seg_p2[1];
    x0 = origin[0]; y0 = origin[1];
    // printf("(a0,b0)=(%f,%f)\n",a0,b0);
    // printf("(a1,b1)=(%f,%f)\n",a1,b1);
    // printf("(x0,y0)=(%f,%f)\n",x0,y0);
    A = sq(a0-a1)+sq(b0-b1);
    B = 2*((a0-a1)*(a1-x0) + (b0-b1)*(b1-y0)  );
    C = sq(a1-x0)+sq(b1-y0)-sq(rad);
    // printf("A = %f\n",A);
    // printf("B = %f\n",B);
    // printf("C = %f\n",C);
    // printf("r = %f\n",rad);
    // printf("disc = %f",sq(B)-4*A*C);

    ang1 = nan("");
    ang2 = nan("");
    t1 = (-B + sqrt(sq(B)-4*A*C))/(2*A);
    t2 = (-B - sqrt(sq(B)-4*A*C))/(2*A);
    // printf("t1: %f\tt2: %f\n",t1,t2);
    if (t1>=0 && t1 <= 1.0)
    {
        xnew = a1+t1*(a0-a1);
        ynew = b1+t1*(b0-b1);
        // printf("t1: x=%f, y=%f\n", xnew,ynew);
        ang1 = rightTurnAngle(radial_pt[0],radial_pt[1],x0, y0, xnew, ynew);
    } 
    if (t2>=0 && t2 <= 1.0) 
    {
        xnew = a1+t2*(a0-a1);
        ynew = b1+t2*(b0-b1);
        ang2 = rightTurnAngle(radial_pt[0],radial_pt[1],x0, y0, xnew, ynew);
    }
    // printf("ang1: %f\tang2: %f\n",ang1, ang2);

    if (!isnan(ang1) && !isnan(ang2))
    {
        return (fabs(ang1)>fabs(ang2) ? ang2 : ang1);
    } else if (!isnan(ang1)) {
        return ang1;
    } else if (!isnan(ang2)) {
        return ang2;
    } else {
        return nan("");
    }
    
    return nan("");
}