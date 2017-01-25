#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include "utils.h"
// #include<time.h>
// #include<stdatomic.h>

#define TREEOPS_API __declspec(dllexport)

#include "treeops.h"

void computeEdgeDeflectionAngle(double* deflect, double* edge_angles, double* pts, int* topo, int num_nodes, int index)
{
    double adef, apared, parx, pary, myx, myy;
    int parent, c1, c2;
    if (index==0) {
        deflect[0]=0.0;
        edge_angles[0]=0.0;
        c1 = topo[(index*3)+1];
        c2 = topo[(index*3)+2];
        parent = topo[(index*3)];
        if (parent != -1) {
            computeEdgeDeflectionAngle(deflect, edge_angles, pts, topo, num_nodes, parent);
        }
    } else {
        parent = topo[(index*3)];
        c1 = topo[(index*3)+1];
        c2 = topo[(index*3)+2];
        parx = pts[(parent*2)];
        pary = pts[(parent*2)+1];
        myx = pts[(index*2)];
        myy = pts[(index*2)+1];
        apared = edge_angles[parent];
        // compute the values:
        edge_angles[index] = atan2(myy-pary,myx-parx);
        deflect[index] = edge_angles[index]-apared;
        // printf("%d\t%f\t%f\n",index,edge_angles[index],deflect[index]);
    }
    if (c1 != -1) computeEdgeDeflectionAngle(deflect, edge_angles, pts, topo, num_nodes, c1);
    if (c2 != -1) computeEdgeDeflectionAngle(deflect, edge_angles, pts, topo, num_nodes, c2);
}

void computeLengths(double* lengths, double* pts, int* topo, int num_nodes, int index)
{
    double parx, pary, myx, myy;
    int parent, c1, c2;
    if (index==0) {
        lengths[0]=0.0;
        c1 = topo[(index*3)+1];
        c2 = topo[(index*3)+2];
        parent = topo[(index*3)];
        if (parent != -1) {
            computeLengths(lengths, pts, topo, num_nodes, parent);
        }
    } else {
        parent = topo[(index*3)];
        c1 = topo[(index*3)+1];
        c2 = topo[(index*3)+2];
        parx = pts[(parent*2)];
        pary = pts[(parent*2)+1];
        myx = pts[(index*2)];
        myy = pts[(index*2)+1];
        // compute the values:
        lengths[index] = sqrt(sq(myx-parx)+sq(myy-pary));
        // printf("%d\t%f\t%f\n",index,edge_angles[index],deflect[index]);
    }
    if (c1 != -1) computeLengths(lengths, pts, topo, num_nodes, c1);
    if (c2 != -1) computeLengths(lengths, pts, topo, num_nodes, c2);
}

void relocateSubtreeByDeflectionAngles(double* deflect, double* edge_angles, double* lengths, double* pts, int* topo, int num_nodes, int index)
{
    double adef, apared, parx, pary, myx, myy;
    int parent, c1, c2;
    if (index==0)
    {
        pts[0]=0.0;
        pts[1]=0.0;
        c1 = topo[(index*3)+1];
        c2 = topo[(index*3)+2];
        parent = topo[(index*3)];
        if (parent != -1) {
            relocateSubtreeByDeflectionAngles(deflect, edge_angles, lengths, pts, topo, num_nodes, parent);
        }
    } else {
        parent = topo[(index*3)];
        c1 = topo[(index*3)+1];
        c2 = topo[(index*3)+2];
        parx = pts[(parent*2)];
        pary = pts[(parent*2)+1];
        apared = edge_angles[parent];

        // fix edge angle and point
        edge_angles[index] = edge_angles[parent]+deflect[index];
        pts[index*2] = parx + cos(edge_angles[index])*lengths[index];
        pts[index*2+1] = pary + sin(edge_angles[index])*lengths[index];
    }
    if (c1 != -1) relocateSubtreeByDeflectionAngles(deflect, edge_angles, lengths, pts, topo, num_nodes, c1);
    if (c2 != -1) relocateSubtreeByDeflectionAngles(deflect, edge_angles, lengths, pts, topo, num_nodes, c2);
}

void computeNodesBelow(int* nodesbelow, int* topo, int num_nodes, int index)
{
    int c1, c2;
    c1 = topo[(index*3)+1];
    c2 = topo[(index*3)+2];
    if (c1 ==-1 && c2==-1) 
    {
        nodesbelow[index]=0;
    } else if (c1 == -1 && c2 != -1) {
        computeNodesBelow(nodesbelow, topo, num_nodes, c2);
        nodesbelow[index] = nodesbelow[c2]+1;
    } else if (c2 == -1 && c1 != -1) {
        computeNodesBelow(nodesbelow, topo, num_nodes, c1);
        nodesbelow[index] = nodesbelow[c1]+1;
    } else {
        computeNodesBelow(nodesbelow, topo, num_nodes, c1);
        computeNodesBelow(nodesbelow, topo, num_nodes, c2);
        nodesbelow[index] = nodesbelow[c1]+nodesbelow[c2]+2;
    }
}

void traverseAwayFromClade(double* pts, int* topo, int* is_away, int index, int called_from)
{
    is_away[index] = 1;
    int c1, c2;
    if (topo[(index*3)]==called_from) {
        c1 = topo[(index*3)+1];
        c2 = topo[(index*3)+2];
    } else if (topo[(index*3)+1]==called_from) {
        c1 = topo[(index*3)];
        c2 = topo[(index*3)+2];
    } else {
        c1 = topo[(index*3)];
        c2 = topo[(index*3)+1];
    }
    if (c1!=-1) traverseAwayFromClade(pts, topo, is_away, c1, index);
    if (c2!=-1) traverseAwayFromClade(pts, topo, is_away, c2, index);
}

double maxLengthToTip(double* lengths, int* topo, int index, int away_from)
{
    // returns the longest distance from (away_from) to tip going through (index)
    int c1, c2;
    double res, l1, l2, lmax, mylen;
    if (topo[(index*3)]==away_from) {
        c1 = topo[(index*3)+1];
        c2 = topo[(index*3)+2];
        mylen = lengths[index];
    } else if (topo[(index*3)+1]==away_from) {
        c1 = topo[(index*3)];
        c2 = topo[(index*3)+2];
        mylen = lengths[away_from];
    } else {
        c1 = topo[(index*3)];
        c2 = topo[(index*3)+1];
        mylen = lengths[away_from];
    }
    l1=0; l2=0;
    if (c1!=-1) l1 = maxLengthToTip(lengths, topo, c1, index);
    if (c2!=-1) l2 = maxLengthToTip(lengths, topo, c2, index);
    lmax = (l1 > l2 ? l1 : l2);
    return mylen + lmax;
}

void findLeaves(int* topo, int numpts, int* is_leaf)
{
    int i;
    for (i=0; i<numpts; i++)
    {
        is_leaf[i] = ((topo[i*3+1]==-1 && topo[i*3+2]==-1) ? 1 : 0);
    }
}

double* getPtsAwayFromClade(double* pts, int* topo, int num_nodes, int from_index, int in_direction_of, int* is_away)
{
    //
    // makes an array of all the points in the clade "above" the from_index
    //
    int i;
    for (i=0; i<num_nodes; i++) {is_away[i]=0;}
    
    // get which nodes are included, then count how many
    traverseAwayFromClade(pts, topo, is_away, in_direction_of, from_index);
    int num_away = 0;
    for (i=0; i<num_nodes; i++) {num_away+=is_away[i];}
    
    double *pts_away = (double *)malloc(num_away * 2 * sizeof(double));
    int ct = 0;
    for (i=0; i<num_nodes; i++) {
        if (is_away[i]==1) {
            pts_away[ct*2]=pts[i*2];
            pts_away[ct*2+1]=pts[i*2+1];
            ct++;
        }
    }
    
    return pts_away;    
}

int compareLexicographically(const void * a, const void * b)
{
    double ax, ay, bx, by;
    double* adub = (double *) a;
    double* bdub = (double *) b;
    ax = adub[0];
    ay = adub[1];
    bx = bdub[0];
    by = bdub[1];
    // printf("ax: %f, ay: %f, bx: %f, by: %f", ax, ay, bx, by);
    
    if (ax > bx) return 1;
    if (ax == bx) 
    {
        if (ay > by)
        {
            return 1;
        } else if (ay==by) {
            return 0;
        } else {
            return -1;
        }
    }
    return -1;
}
int compareRotationallyTo45DegLine(const void * a, const void * b)
{
    // This is to be used by quicksort to compare points by their rotational offset from pi/4
    double ax, ay, bx, by, root2, atheta, btheta;
    root2 = 0.70710678118654746;
    double* adub = (double *) a;
    double* bdub = (double *) b;
    ax = root2*(adub[0]+adub[1]);
    ay = root2*(adub[1]-adub[0]);
    bx = root2*(bdub[0]+bdub[1]);
    by = root2*(bdub[1]-bdub[0]);
    atheta = atan2(ay,ax);
    btheta = atan2(by,bx);
    // printf("ax: %f, ay: %f, bx: %f, by: %f", ax, ay, bx, by);
    
    if (atheta > btheta)
    {
        return 1;
    } else {
        return (btheta > atheta ? -1 : 0);
    }
    return -1;
}

void reverseArray(double* pts_away, int numpts)
{
    int i, j;
    i=0;
    j=numpts-1;
    double tx, ty;
    while (i<j)
    {
        tx = pts_away[j*2];
        ty = pts_away[j*2+1];
        pts_away[j*2]=pts_away[i*2];
        pts_away[j*2+1]=pts_away[i*2+1];
        pts_away[i*2]=tx;
        pts_away[i*2+1]=ty;
        i++;
        j--;
    }
}

int rightTurn(double* a, double* b, double* c)
{
    double res;
    res = (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);
    // printf("\tRT: (%f,%f), (%f,%f), (%f,%f)\tres: %f\n", a[0], a[1], b[0], b[1], c[0],c[1], res);
    if (res < 0) return 1;
    return 0;
}

void printPts(double* pts, int size)
{
    int i;
    for (i=0;i<size;i++) {
        printf ("%f\t%f\n",pts[i*2],pts[i*2+1]);
    }
}

int grahamInPlaceScan(double* pts_away, int num_pts, int upper)
{
    qsort(pts_away,num_pts,2*sizeof(double),compareLexicographically);
    
    if (upper != 0) 
    {
        reverseArray(pts_away, num_pts);
    }
    // printPts(pts_away,num_pts);
    int h =1;
    int i;
    double tx, ty;
    
    for (i=1;i<num_pts;i++) 
    {
        // printf("i: %d\th: %d\n",i,h);
        while (h>1 && rightTurn(&pts_away[(h-2)*2], &pts_away[(h-1)*2], &pts_away[i*2]))
        {
            h--;
        }
        tx = pts_away[h*2];
        ty = pts_away[h*2+1];
        pts_away[h*2]=pts_away[i*2];
        pts_away[h*2+1]=pts_away[i*2+1];
        pts_away[i*2]=tx;
        pts_away[i*2+1]=ty;
        h++;
    }
    return h;
}

int grahamInPlaceHull(double* pts_away, int num_pts)
{
    int i, h0, h1, num_pts2;
    double tmpx, tmpy;
    h0 = grahamInPlaceScan(pts_away, num_pts, 1);
    for (i=0; i<h0-1; i++)
    {
        tmpx = pts_away[i*2];
        tmpy = pts_away[i*2+1];
        pts_away[i*2]=pts_away[(i+1)*2];
        pts_away[i*2+1]=pts_away[(i+1)*2+1];
        pts_away[(i+1)*2] = tmpx;
        pts_away[(i+1)*2+1] = tmpy;
    }
    num_pts2 = num_pts - h0 +1;
    h1 = grahamInPlaceScan(&pts_away[(h0-1)*2], num_pts2,0);
    return h0 + h1 - 1;
}


void pivotPointsAround(double* pts, double* origin, double* deg45pt, int num_pts)
{
    // TODO: should this be an in-place rotation? Currently it is.
    double pi=3.141592653589793;
    int i;
    double theta, theta_cos, theta_sin, x0, y0, xold, yold;
    theta = pi/4.0 - atan2((deg45pt[1]-origin[1]),(deg45pt[0]-origin[0]));
    theta_cos = cos(theta);
    theta_sin = sin(theta);
    x0=origin[0];
    y0=origin[1];
    for (i=0;i<num_pts; i++)
    {
        // first shift relative to the origin
        pts[i*2]=pts[i*2]-x0;
        pts[i*2+1]=pts[i*2+1]-y0;
        xold = pts[i*2]; yold = pts[i*2+1];

        //then rotate them:
        pts[i*2]=xold*theta_cos-yold*theta_sin;
        pts[i*2+1]=xold*theta_sin+yold*theta_cos;
    }
}

double ptsRightTurnAngle(double* pts, int i1, int i2, int i3)
{
    double x1, y1, x2, y2, x3, y3;
    x1 = pts[i1*2]; y1 = pts[i1*2+1];
    x2 = pts[i2*2]; y2 = pts[i2*2+1];
    x3 = pts[i3*2]; y3 = pts[i3*2+1];
    return rightTurnAngle(x1, y1, x2, y2, x3, y3);
}

double arraysRightTurnAngle(double* p1, double* p2, double* p3)
{
    return rightTurnAngle(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]);
}

void debugTestRightTurnAngle()
{
    double x1, y1, x2, y2, x3, y3, rta;
    x1 = 0.0;
    y1 = 5.0;
    x2 = 0.;
    y2 = 0.;
    x3 = 1.0;
    y3 = -5.0;
    rta = rightTurnAngle(x1,y1,x2,y2, x3,y3);
    printf("(%f,%f)\t(%f,%f)\t(%f,%f)\t%f\n",x1, y1, x2, y2, x3, y3, rta);
}

int countBranchesToSideLeaf(double* pts, int* topo, int startnode, int awayFromNode, int clockwise)
{
    // counts the number of branches between startnode and the (counter)-clockwise-most node in the subtree
    // directed away from awayFromNode. 
    // clockwise == 0: gets the counterclockwise-most length
    // clockwise != 0: gets the clockwise-most length
    double pi=3.141592653589793;
    int stop = 0;
    int ct = 0;
    int i1, i2, i3, c1, c2, last, curr;
    double p1x, p1y, atmp, a1, a2;
    last = awayFromNode;
    curr = startnode;

    while (stop == 0)
    {
        i1 = topo[curr*3];
        i2 = topo[curr*3+1];
        i3 = topo[curr*3+2];

        if (i1==last) {
            c1 = i2;
            c2 = i3;
        } else if (i2==last) {
            c1 = i1;
            c2 = i3;
        } else {
            c1 = i1;
            c2 = i2;
        }
        if (c1==-1 && c2==-1) {return ct;}
        p1x = pts[last*2]; p1y = pts[last*2+1];
        a1 = ptsRightTurnAngle(pts, last, curr, c1);
        a2 = ptsRightTurnAngle(pts, last, curr, c2);

        
        if (c1 == -1) {
                // if the node is a unifurcation, just add it to the list and keep going.
                last = curr;
                curr = c2;
        } else if (c2 == -1) {
                last = curr;
                curr = c1;
        } else { 
            if ((clockwise!=0 && a1>a2) || (clockwise==0 && a1<a2)) {
                last = curr;
                curr = c1;
            } else {
                last = curr;
                curr = c2;
            }
        }
        ct++;
    }
    return ct;
}

// double* getBranchesToSideLeaf(double* pts, int* topo, int startnode, int awayFromNode, int clockwise, int* num_pts_in_result)
void getBranchesToSideLeaf(double* pts, int* topo, int startnode, int awayFromNode, int clockwise, double* branch_points)
{
    // gets the branches between startnode and the (counter)-clockwise-most node in the subtree
    // directed away from awayFromNode. (does not include branch from away to start)
    // clockwise == 0: gets the counterclockwise-most length
    // clockwise != 0: gets the clockwise-most length

    double pi=3.141592653589793;
    int stop = 0;
    int ct = 0;
    int i1, i2, i3, c1, c2, last, curr;
    double a1, a2, atmp;
    last = awayFromNode;
    curr = startnode;

    // start with the starting node
    branch_points[ct*2]=pts[curr*2];
    branch_points[ct*2+1]=pts[curr*2+1];
    ct++;

    while (stop == 0)
    {
        i1 = topo[curr*3];
        i2 = topo[curr*3+1];
        i3 = topo[curr*3+2];

        if (i1==last) {
            c1 = i2;
            c2 = i3;
        } else if (i2==last) {
            c1 = i1;
            c2 = i3;
        } else {
            c1 = i1;
            c2 = i2;
        }
        if (c1==-1 && c2==-1) {
            branch_points[ct*2]=pts[curr*2];
            branch_points[ct*2+1]=pts[curr*2+1];
            // return branch_points;
            return;
        }
        a1 = ptsRightTurnAngle(pts, last, curr, c1);
        a2 = ptsRightTurnAngle(pts, last, curr, c2);

        
        if (c1 == -1) {
                last = curr;
                curr = c2;
        } else if (c2 == -1) {
                last = curr;
                curr = c1;
        } else { 
            if ((clockwise!=0 && a1>a2) || (clockwise==0 && a1<a2)) {
                last = curr;
                curr = c1;
            } else {
                last = curr;
                curr = c2;
            }
        }
        branch_points[ct*2]=pts[curr*2];
        branch_points[ct*2+1]=pts[curr*2+1];
        ct++;
    }
    // return branch_points;
    return;
}

int find45DegreeCutoffInSortedPoints(double* pts, int numpts, int below)
{
    // if below == 0, finds the last point that is not below the 45 degree line, otherwise finds thatl ast point that is
    int i;
    if (below ==0) {
        for (i=0; i<numpts; i++) {
            if (pts[i*2] - pts[i*2+1] > -.00000000000000000001) return i;
        } 
    } else {
        for (i=0; i<numpts; i++) {
            if (pts[i*2+1] - pts[i*2] > -.00000000000000000001) return i;
        }
    }
    return numpts;
}

void zeroOutDoubleArray(double* pts, int numpts)
{
    int i;
    for (i=0; i<numpts; i++)
    {
        pts[i]= 0.0;
    }
}

void updateMinAngles(double currangle, double* minClockwiseAngle, double* minCounterClockwiseAngle)
{
    // convention is that couterclockwise angles are positive and clockwise angles are negative
    if isnan(currangle) return;
    if (currangle>0 && (isnan(minCounterClockwiseAngle[0]) ||currangle<minCounterClockwiseAngle[0])) {
        minCounterClockwiseAngle[0]=currangle;
    } else if (currangle<0 && (isnan(minClockwiseAngle[0]) || currangle>minClockwiseAngle[0])) {
        minClockwiseAngle[0]=currangle;
    }
}

int nearestBranchToNode(double* pts, int* topo, int numpts, int index, int* is_away)
{
    double x0, y0;
    x0 = pts[index*2];
    y0 = pts[index*2+1];
    return nearestBranchToPoint(pts,topo,numpts,x0,y0, is_away);
}

int nearestBranchToPoint(double* pts, int* topo, int numpts, double x0, double y0, int* is_away)
{
    double d1, d2, dist, dnew, d_eps;
    d_eps = 1.0e-18;
    dist = 9.0e+99;
    int i, par, min_i;
    // x0 = pts[index*2];
    // y0 = pts[index*2+1];
    for (i=1; i<numpts; i++)
    {
        if (is_away[i]!=0)
        {
            par = topo[i*3];
            d1 = hypot(pts[i*2]-x0, pts[i*2+1]-y0);
            d2 = hypot(pts[par*2]-x0, pts[par*2+1]-y0);
            // if (i != index && par != index)
            if (d1 > d_eps && d2 > d_eps)
            {
                dnew=distToLineSegment(x0,y0,pts[par*2],pts[par*2+1],pts[i*2],pts[i*2+1]);
                // printf("i=%d\tdnew=%f\tdist=%f\n",i, dnew, dist);
                if (dnew < dist)
                {
                    dist = dnew;
                    min_i = i;
                }
                // dist = (dnew < dist ? dnew : dist);
                // min_i = (dnew < dist ? i : min_i);            
            }
        }
    }
    return min_i;
}

double myatan2(double x, double y, int shiftneg)
{   
    double a; 
    double pi=3.141592653589793;
    a = atan2(y,x);
    return ((shiftneg && signbit(a)) ? a + pi : a);
}

int getOuterConvexHull(double* pts_in_clade, int num_in_clade, double* sidept1, double* sidept2, double* origin)
{
    double dp1, dp2, ap1, ap2, anew, dnew, x0, y0, aconst, spa1, spa2, spa3, ahi, alo, w;
    double dhi, dlo;
    double pi=3.141592653589793;
    double eps = pi/1000000000;
    double d_eps = .00000000001;
    int shift;
    x0 = origin[0];
    y0 = origin[1];
    dp1 = sqrt(sq(sidept1[0]-x0)+sq(sidept1[1]-y0));
    dp2 = sqrt(sq(sidept2[0]-x0)+sq(sidept2[1]-y0));
    ap1 = atan2(sidept1[1]-y0,sidept1[0]-x0);
    ap2 = atan2(sidept2[1]-y0,sidept2[0]-x0);
    ahi = (ap1 > ap2 ? ap1 : ap2);
    alo = (ap1 > ap2 ? ap2 : ap1);
    dhi = (dp1 > dp2 ? dp1 : dp2);
    dlo = (dp1 > dp2 ? dp2 : dp1);
    
    if (num_in_clade<3) {
        return num_in_clade;
    } else {
        spa1 = atan2(pts_in_clade[2+1]-y0, pts_in_clade[2]-x0);
        spa2 = atan2(pts_in_clade[2*1+1]-y0, pts_in_clade[2*1]-x0);
        spa3 = atan2(pts_in_clade[2*2+1]-y0, pts_in_clade[2*2]-x0);
        shift = (spa1 > ahi+eps || spa2 > ahi+eps || spa3 > ahi+eps || spa1 < alo+eps || spa2 < alo + eps || spa3 < alo+eps);
    }
    // reset these values based on whether we need to 
    ap1 = myatan2(sidept1[1]-y0,sidept1[0]-x0,shift);
    ap2 = myatan2(sidept2[1]-y0,sidept2[0]-x0, shift);
    // ahi = (ap1 > ap2 ? ap1 : ap2);
    // alo = (ap1 > ap2 ? ap2 : ap1);
    // dhi = (ap1 > ap2 ? dp1 : dp2);
    // dlo = (ap1 > ap2 ? dp2 : dp1);

    // put all the values outside the arc of interest up to the front of the array.
    int i, outct;
    outct = 0;
    for (i=0; i<num_in_clade; i++)
    {
        dnew = sqrt(sq(pts_in_clade[i*2+1]-y0)+sq(pts_in_clade[i*2]-x0));
        if (dnew > dhi-d_eps) {
            swapDoublePoints(&pts_in_clade[i*2], &pts_in_clade[outct*2]);
            outct++;
        } else if (dnew+d_eps>dlo) {
            anew = myatan2(pts_in_clade[i*2+1]-y0, pts_in_clade[i*2]-x0, shift);
            w=(ap1-anew)/(ap1-ap2);
            if (dnew+d_eps > dp2*w+dp1*(1.0-w))
            {
                swapDoublePoints(&pts_in_clade[i*2], &pts_in_clade[outct*2]);
                outct++;
            }
        }
    }
    return grahamInPlaceHull(pts_in_clade, outct+1);
}

void debugWriteSegments(double* pts, int* topo, int numpts)
{
    int i;  
    FILE *segs = fopen("/Users/michaelnute/Dropbox/Grad School/Phylogenetics/work/tree_ops/segs.tsv","w");
    for (i=1;i<numpts; i++) {
        fprintf(segs,"%f\t%f\t%f\t%f\t%d\t%d\n",pts[topo[i*3]*2],pts[topo[i*3]*2+1],pts[i*2],pts[i*2+1], topo[i*3],i);
    }
    fclose(segs);
}

void debugWriteTopology(int* topo, int numpts)
{
    int i;  
    FILE *top = fopen("/Users/michaelnute/Dropbox/Grad School/Phylogenetics/work/tree_ops/topology.tsv","w");
    for (i=0;i<numpts; i++) {
        fprintf(top,"%d\t%d\t%d\n",topo[i*3],topo[i*3+1],topo[i*3+2]);
    }
    fclose(top);
}



// TREEOPS_API void centerCladeRotationally(double* pts, int* topo, double* edge_angles, double* deflect_angles, double* lengths, 
                             // int numpts, int node)
void centerCladeRotationally(double* pts, int* topo, double* edge_angles, double* deflect_angles, double* lengths, 
                             int numpts, int node)
{
    // printf("numpts is %d\n",numpts);
    
    // int *is_away = (int *)malloc(numpts * sizeof(int));
    // int *is_leaf = (int *)malloc(numpts * sizeof(int));
    int is_away[numpts];
    int is_leaf[numpts];
    int parent = topo[node*3];
    double myx, myy, parx, pary;
    double pi=3.141592653589793;
    myx = pts[node*2];
    myy = pts[node*2+1];

    int num_out, num_in, i, j ;
    for (i=0; i<numpts; i++) {
        is_leaf[i]=0;
        is_away[i]=0;
    }

    // debugWriteSegments(pts, topo, numpts);
    // debugWriteTopology(topo, numpts);

    // get an array of indicators for whether the node is a leaf node
    findLeaves(topo, numpts, &is_leaf[0]);

    // get the points in the clade and external to the clade


    //DEBUG
    // FILE *dfile = fopen("resources/cutils/pts_nparr_fromc.txt","w");
    // for (i=0;i<numpts;i++)
    // {
    //     fprintf(dfile, "%f\t%f\n", pts[i*2], pts[i*2+1] );
    // }
    // fclose(dfile);   
    
    traverseAwayFromClade(pts, topo, &is_away[0], parent, node);
    num_out = 0; num_in = 0;
    for (i=0;i<numpts; i++) {
        // count the leaves
        if (is_leaf[i]==1) 
        {
            if (is_away[i]==1) 
            {
                num_out++;    
            } else {
                num_in++;
            }
        }
    }
    // double* pts_out_of_clade = (double *)malloc(2*num_out * sizeof(double));
    // double* pts_in_clade = (double *)malloc(2*num_in * sizeof(double)); 
    // double pts_out_of_clade[2*num_out];
    // double pts_in_clade[2*num_in];
    
    
    int inct, outct; //leaf counts, specifically
    // inct = 0; outct = 0;
    inct = num_in; outct = num_out;

    // for (i=0;i<numpts;i++)
    // {
    //     if (is_leaf[i]==1) 
    //     {
    //         if (is_away[i]==1) {
    //             pts_out_of_clade[outct*2] = pts[i*2];
    //             pts_out_of_clade[outct*2+1] = pts[i*2+1];
    //             outct++;
    //         } else {
    //             pts_in_clade[inct*2] = pts[i*2];
    //             pts_in_clade[inct*2+1] = pts[i*2+1];
    //             inct++;            
    //         }
    //     }
    // }
    // printf("inct: %d\toutct: %d\n", inct, outct);
    // double* origin = (double *)malloc(2 * sizeof(double));
    double origin[2];
    origin[0]=pts[parent*2];
    origin[1]=pts[parent*2+1];

    // double minClockwiseRotAngle = -pi;
    double minClockwiseRotAngle = nan("");
    // double minCounterClockwiseRotAngle = pi;
    double minCounterClockwiseRotAngle = nan("");
    double currangle = 0.0;

    // int num_sidepts_in_clockside;
    // int num_sidepts_in_counterside;
    // int num_sidepts_out_clockside;
    // int num_sidepts_out_counterside;
    // num_sidepts_in_clockside = countBranchesToSideLeaf(pts, topo, node, parent, 1);
    // num_sidepts_in_counterside = countBranchesToSideLeaf(pts, topo, node, parent, 0);
    // num_sidepts_out_clockside = countBranchesToSideLeaf(pts, topo, parent, node, 1);
    // num_sidepts_out_counterside = countBranchesToSideLeaf(pts, topo, parent, node, 0);

    //OLD: double* sidepts_in_clockside = (double *)malloc(2*(num_sidepts_in_clockside+2) * sizeof(double));
    //OLD: double* sidepts_in_counterside = (double *)malloc(2*(num_sidepts_in_counterside+2) * sizeof(double));
    //OLD: double* sidepts_out_clockside = (double *)malloc(2*(num_sidepts_out_clockside+2) * sizeof(double));
    //OLD: double* sidepts_out_counterside = (double *)malloc(2*(num_sidepts_out_counterside+2) * sizeof(double));
    // double sidepts_in_clockside[2*(num_sidepts_in_clockside+2)];
    // double sidepts_in_counterside[2*(num_sidepts_in_counterside+2)];
    // double sidepts_out_clockside[2*(num_sidepts_out_clockside+2)];
    // double sidepts_out_counterside[2*(num_sidepts_out_counterside+2)];
    //OLD: sidepts_in_clockside = getBranchesToSideLeaf(pts, topo, node, parent, 1, &num_sidepts_in_clockside);
    //OLD: sidepts_in_counterside = getBranchesToSideLeaf(pts, topo, node, parent, 0, &num_sidepts_in_counterside);
    //OLD: sidepts_out_clockside = getBranchesToSideLeaf(pts, topo, parent, node, 1, &num_sidepts_out_clockside);
    //OLD: sidepts_out_counterside = getBranchesToSideLeaf(pts, topo, parent, node, 0, &num_sidepts_out_counterside);
    // getBranchesToSideLeaf(pts, topo, node, parent, 1, sidepts_in_clockside);
    // getBranchesToSideLeaf(pts, topo, node, parent, 0, sidepts_in_counterside);
    // getBranchesToSideLeaf(pts, topo, parent, node, 1, sidepts_out_clockside);
    // getBranchesToSideLeaf(pts, topo, parent, node, 0, sidepts_out_counterside);

    // int in_chull_ct, out_chull_ct;
    // in_chull_ct = getOuterConvexHull(&pts_in_clade[0], inct, &sidepts_in_clockside[num_sidepts_in_clockside*2],
    //                                     &sidepts_in_counterside[num_sidepts_in_counterside*2],&origin[0]);
    // out_chull_ct = getOuterConvexHull(&pts_out_of_clade[0], outct, &sidepts_out_clockside[num_sidepts_out_clockside*2],
    //                                     &sidepts_out_counterside[num_sidepts_out_counterside*2],&origin[0]);

    // FILE *sideendpts = fopen("/Users/michaelnute/Dropbox/Grad School/Phylogenetics/work/tree_ops/sideendpts.tsv","w");
    // fprintf(sideendpts, "%f\t%f\n", sidepts_out_clockside[num_sidepts_out_clockside*2],sidepts_out_clockside[num_sidepts_out_clockside*2+1] );
    // fprintf(sideendpts, "%f\t%f\n", sidepts_out_counterside[num_sidepts_out_counterside*2],sidepts_out_counterside[num_sidepts_out_counterside*2+1] );
    // fclose(sideendpts);

    // FILE *allpts = fopen("/Users/michaelnute/Dropbox/Grad School/Phylogenetics/work/tree_ops/debugpts.tsv","w");
    // struct timespec tim, tim2;
    // tim.tv_sec = 0;
    // tim.tv_nsec = 1000000;

    
    int par, mypar;
    for (j=0; j<numpts; j++)
    {
        if (is_leaf[j]==1 && is_away[j]==0) {
            mypar = topo[j*3];
            for (i=1; i<numpts; i++)
            {
                if (is_away[i]==1)
                {
                    par = topo[i*3];
                    currangle = getRotationalAngleToSegment(&origin[0],&pts[j*2],
                                                            &pts[i*2],&pts[par*2]);
                    updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
                    currangle = -getRotationalAngleToSegment(&origin[0],&pts[i*2],&pts[j*2], &pts[mypar*2]);
                    updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
                    currangle = -getRotationalAngleToSegment(&origin[0],&pts[par*2],&pts[j*2], &pts[mypar*2]);
                    updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
                    // fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], pts_in_clade[j*2],
                    // pts_in_clade[j*2+1],pts[i*2],pts[i*2+1],pts[par*2], pts[par*2+1],
                    // currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,par);
                }
            }            
        }
    }

    // start with inner clockside points
    // printf("num_sidepts_in_clockside: %d\n", num_sidepts_in_clockside);
    // for (j=0; j<num_sidepts_in_clockside; j++)
    // {
    //     // compare with outer clockside segments
    //     printf("sidepts_out_clockside: %d\n",num_sidepts_out_clockside);
    //     for (i=0; i<num_sidepts_out_clockside; i++)
    //     {
    //         currangle = getRotationalAngleToSegment(&origin[0],&sidepts_in_clockside[j*2],
    //                                                 &sidepts_out_clockside[i*2],&sidepts_out_clockside[(i+1)*2]);
    //         updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //         fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], sidepts_in_clockside[j*2],
    //             sidepts_in_clockside[j*2+1],sidepts_out_clockside[i*2],sidepts_out_clockside[i*2+1],sidepts_out_clockside[(i+1)*2],
    //             sidepts_out_clockside[(i+1)*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,1);
    //         // printf("i: %d\tj: %d\n",i,j);
    //         // nanosleep(&tim, &tim2);
    //     }

    //     // compare with outer couterside segments
    //     printf("sidepts_out_counterside: %d\n",num_sidepts_out_counterside);
    //     for (i=0; i<num_sidepts_out_counterside; i++)
    //     {
    //         currangle = getRotationalAngleToSegment(&origin[0],&sidepts_in_clockside[j*2],
    //                                                 &sidepts_out_counterside[i*2],&sidepts_out_counterside[(i+1)*2]);
    //         updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //         fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], sidepts_in_clockside[j*2],
    //             sidepts_in_clockside[j*2+1],sidepts_out_counterside[i*2],sidepts_out_counterside[i*2+1],sidepts_out_counterside[(i+1)*2],
    //             sidepts_out_counterside[(i+1)*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,1);
    //         // printf("i: %d\tj: %d\n",i,j);
    //         // nanosleep(&tim, &tim2);
    //     }

    //     printf("out_chull_ct: %d\n",out_chull_ct);
    //     // compare with segments from convex hull
    //     for (i=0; i<out_chull_ct; i++)
    //     {
    //         currangle = getRotationalAngleToSegment(&origin[0],&sidepts_in_clockside[j*2],
    //                                                 &pts_out_of_clade[i*2],&pts_out_of_clade[((i+1) % out_chull_ct)*2]);
    //         updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //         fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], sidepts_in_clockside[j*2],
    //             sidepts_in_clockside[j*2+1],pts_out_of_clade[i*2],pts_out_of_clade[i*2+1],pts_out_of_clade[((i+1) % out_chull_ct)*2],
    //             pts_out_of_clade[((i+1) % out_chull_ct)*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,1);
    //         // printf("i: %d\tj: %d\n",i,j);
    //         // nanosleep(&tim, &tim2);
    //     }

    //     nearest = nearestBranchToPoint(pts, topo, numpts,sidepts_in_clockside[j*2],sidepts_in_clockside[j*2+1], is_away);
    //     printf("nearest %d\n",nearest);
    //     currangle = getRotationalAngleToSegment(&origin[0],&sidepts_in_clockside[j*2],
    //                                                 &pts[nearest*2],&pts[topo[nearest*3]*2]);
    //     updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //     fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], sidepts_in_clockside[j*2],
    //             sidepts_in_clockside[j*2+1],pts[nearest*2],pts[nearest*2+1],pts[topo[nearest*3]*2],
    //             pts[topo[nearest*3]*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,41);
    // }
    
    // // then inner counterside points
    // printf("num_sidepts_in_counterside: %d\n",num_sidepts_in_counterside);
    // for (j=0; j<num_sidepts_in_counterside; j++)
    // {
    //     // compare with outer clockside segments
    //     for (i=0; i<num_sidepts_out_clockside; i++)
    //     {
    //         currangle = getRotationalAngleToSegment(&origin[0],&sidepts_in_counterside[j*2],
    //                                                 &sidepts_out_clockside[i*2],&sidepts_out_clockside[(i+1)*2]);
    //         updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //         fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], sidepts_in_counterside[j*2],
    //             sidepts_in_counterside[j*2+1],sidepts_out_clockside[i*2],sidepts_out_clockside[i*2+1],sidepts_out_clockside[(i+1)*2],
    //             sidepts_out_clockside[(i+1)*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,2);
    //         // printf("i: %d\tj: %d\n",i,j);
    //         // nanosleep(&tim, &tim2);
    //     }

    //     // compare with outer couterside segments
    //     for (i=0; i<num_sidepts_out_counterside; i++)
    //     {
    //         currangle = getRotationalAngleToSegment(&origin[0],&sidepts_in_counterside[j*2],
    //                                                 &sidepts_out_counterside[i*2],&sidepts_out_counterside[(i+1)*2]);
    //         updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //         fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], sidepts_in_counterside[j*2],
    //             sidepts_in_counterside[j*2+1],sidepts_out_counterside[i*2],sidepts_out_counterside[i*2+1],sidepts_out_counterside[(i+1)*2],
    //             sidepts_out_counterside[(i+1)*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,2);
    //         // printf("i: %d\tj: %d\n",i,j);
    //         // nanosleep(&tim, &tim2);
    //     }

    //     // compare with segments from convex hull
    //     for (i=0; i<out_chull_ct; i++)
    //     {
    //         currangle = getRotationalAngleToSegment(&origin[0],&sidepts_in_counterside[j*2],
    //                                                 &pts_out_of_clade[i*2],&pts_out_of_clade[((i+1) % out_chull_ct)*2]);
    //         updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //         fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], sidepts_in_counterside[j*2],
    //             sidepts_in_counterside[j*2+1],pts_out_of_clade[i*2],pts_out_of_clade[i*2+1],pts_out_of_clade[((i+1) % out_chull_ct)*2],
    //             pts_out_of_clade[((i+1) % out_chull_ct)*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,2);
    //         // printf("i: %d\tj: %d\n",i,j);
    //         // nanosleep(&tim, &tim2);
    //     }
    //     nearest = nearestBranchToPoint(pts, topo, numpts,sidepts_in_counterside[j*2],sidepts_in_counterside[j*2+1], is_away);
    //     currangle = getRotationalAngleToSegment(&origin[0],&sidepts_in_counterside[j*2],
    //                                                 &pts[nearest*2],&pts[topo[nearest*3]*2]);
    //     updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //     fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], sidepts_in_counterside[j*2],
    //             sidepts_in_counterside[j*2+1],pts[nearest*2],pts[nearest*2+1],pts[topo[nearest*3]*2],
    //             pts[topo[nearest*3]*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,42);
    // }

    // // then inner chull points
    // printf("in_chull_ct: %d\n", in_chull_ct);
    // for (j=0; j<in_chull_ct; j++)
    // {
    //     // compare with outer clockside segments
    //     for (i=0; i<num_sidepts_out_clockside; i++)
    //     {
    //         currangle = getRotationalAngleToSegment(&origin[0],&pts_in_clade[j*2],
    //                                                 &sidepts_out_clockside[i*2],&sidepts_out_clockside[(i+1)*2]);
    //         updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //         fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], pts_in_clade[j*2],
    //             pts_in_clade[j*2+1],sidepts_out_clockside[i*2],sidepts_out_clockside[i*2+1],sidepts_out_clockside[(i+1)*2],
    //             sidepts_out_clockside[(i+1)*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,3);
    //         // printf("i: %d\tj: %d\n",i,j);
    //         // nanosleep(&tim, &tim2);
    //     }

    //     // compare with outer couterside segments
    //     for (i=0; i<num_sidepts_out_counterside; i++)
    //     {
    //         currangle = getRotationalAngleToSegment(&origin[0],&pts_in_clade[j*2],
    //                                                 &sidepts_out_counterside[i*2],&sidepts_out_counterside[(i+1)*2]);
    //         updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //         fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], pts_in_clade[j*2],
    //             pts_in_clade[j*2+1],sidepts_out_counterside[i*2],sidepts_out_counterside[i*2+1],sidepts_out_counterside[(i+1)*2],
    //             sidepts_out_counterside[(i+1)*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,3);
    //         // printf("i: %d\tj: %d\n",i,j);
    //         // nanosleep(&tim, &tim2);
    //     }

    //     // compare with segments from convex hull
    //     // printf("out_chull_ct: %d\n",out_chull_ct);
    //     for (i=0; i<out_chull_ct; i++)
    //     {
    //         currangle = getRotationalAngleToSegment(&origin[0],&pts_in_clade[j*2],
    //                                                 &pts_out_of_clade[i*2],&pts_out_of_clade[((i+1) % out_chull_ct)*2]);
    //         updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //         fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], pts_in_clade[j*2],
    //             pts_in_clade[j*2+1],pts_out_of_clade[i*2],pts_out_of_clade[i*2+1],pts_out_of_clade[((i+1) % out_chull_ct)*2],
    //             pts_out_of_clade[((i+1) % out_chull_ct)*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,3);
    //         // printf("i: %d\tj: %d\n",i,j);
    //         // nanosleep(&tim, &tim2);
    //     }
    //     nearest = nearestBranchToPoint(pts, topo, numpts,pts_in_clade[j*2],pts_in_clade[j*2+1], is_away);
    //     currangle = getRotationalAngleToSegment(&origin[0],&pts_in_clade[j*2],
    //                                                 &pts[nearest*2],&pts[topo[nearest*3]*2]);
    //     updateMinAngles(currangle, &minClockwiseRotAngle, &minCounterClockwiseRotAngle);
    //     fprintf(allpts, "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n", origin[0], origin[1], pts_in_clade[j*2],
    //             pts_in_clade[j*2+1],pts[nearest*2],pts[nearest*2+1],pts[topo[nearest*3]*2],
    //             pts[topo[nearest*3]*2+1], currangle, minClockwiseRotAngle, minCounterClockwiseRotAngle,i,j,43);
    // }
    // fprintf(allpts, "\t\t\t\t\t\t\t\t\t\t\t\t\t\n" );
    // fprintf(allpts, "\n" );
    // fclose(allpts);

    // FILE *ochpts = fopen("/Users/michaelnute/Dropbox/Grad School/Phylogenetics/work/tree_ops/out_chull_pts.tsv","w");
    // for (i=0; i<out_chull_ct+1; i++)
    // {
    //     fprintf(ochpts, "%f\t%f\n",pts_out_of_clade[i*2],pts_out_of_clade[i*2+1] );
    // }
    // fclose(ochpts);



    //DEBUG
    // FILE *debfile = fopen("resources/cutils/debug.txt","w");
    // fprintf(debfile,"origin\t%f\t%f\n",pts[parent*2],pts[parent*2+1]);
    // fprintf(debfile,"pivot\t%f\t%f\n",pts[node*2],pts[node*2+1]);
    // fprintf(debfile,"points out:\tout_cutoff\t%d\tout_ctrclock_chull_ct\t%d\tout_clock_chull_ct\t%d\n", out_cutoff,out_ctrclock_chull_ct,out_clock_chull_ct);
    // for (i=0; i<num_out; i++)
    // {
    //     fprintf(debfile, "%f\t%f\n", pts_out_of_clade[i*2], pts_out_of_clade[i*2+1]);
    // }
    // fprintf(debfile,"points in:\tin_cutoff\t%d\tin_ctrclock_chull_ct\t%d\tin_clock_chull_ct\t%d\n", in_cutoff,in_ctrclock_chull_ct,in_clock_chull_ct);
    // for (i=0; i<num_in; i++)
    // {
    //     fprintf(debfile, "%f\t%f\n", pts_in_clade[i*2], pts_in_clade[i*2+1]);
    // }
    // fprintf(debfile, "\n\nupper hull\n");

        // 
    // printf("clockwise: %f\tcounter: %f\n", minClockwiseRotAngle, minCounterClockwiseRotAngle);
    

    if (!(isnan(minClockwiseRotAngle)) && !(isnan(minCounterClockwiseRotAngle)))
    {
        deflect_angles[node]+=(minCounterClockwiseRotAngle + minClockwiseRotAngle) / 2;
        relocateSubtreeByDeflectionAngles(deflect_angles,edge_angles, lengths,pts,topo,numpts,0);
    }

    
    
    // free(is_away);
    // free(is_leaf);
    // free(pts_out_of_clade);
    // free(pts_in_clade);
    // free(origin);
    // free(sidepts_in_clockside);
    // free(sidepts_in_counterside);
    // free(sidepts_out_clockside);
    // free(sidepts_out_counterside);
    
}

double maxLeafRotationRange(double* pts, int* topo, int numpts, int node, double* origin, double* lim_p1, double* lim_p2)
{
    int c1, c2, par;
    c1 = topo[node*3+1]; c2 = topo[node*3+2]; par = topo[node*3];
    double pi=3.141592653589793;

    double rotAng1, rotAng2;
    if (c1==-1 && c2==-1) 
    {
        FILE *expandpts2 = fopen("/Users/michaelnute/Dropbox/Grad School/Phylogenetics/work/tree_ops/expandpts2.tsv","a");
        rotAng1 = getRotationalAngleToSegment(origin, &pts[node*2], lim_p1, lim_p2);
        fprintf(expandpts2,"%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%d\n", origin[0], origin[1], pts[node*2], pts[node*2+1],
                                                            lim_p1[0], lim_p1[1], lim_p2[0],lim_p2[1], rotAng1, node);
        fclose(expandpts2);
        // struct timespec tim, tim2;
        // tim.tv_sec = 0;
        // tim.tv_nsec = 100000000;
        // nanosleep(&tim, &tim2);

        if isnan(rotAng1) rotAng1=pi;
        return fabs(rotAng1);
    } else if (c1 != -1 && c2==-1) {
        return maxLeafRotationRange(pts, topo, numpts, c1, origin, lim_p1, lim_p2);
    } else if (c2 != -1 && c1==-1) {
        return maxLeafRotationRange(pts, topo, numpts, c2, origin, lim_p1, lim_p2);
    } else {
        rotAng1 = maxLeafRotationRange(pts, topo, numpts, c1, origin, lim_p1, lim_p2);
        rotAng2 = maxLeafRotationRange(pts, topo, numpts, c2, origin, lim_p1, lim_p2);
        return (rotAng1 > rotAng2 ? rotAng2 : rotAng1);
    }
}

// void longCladesToInterior(double* pts, int* topo, int numpts, double* deflect_angles, double* container_wedges, double* lengths, int node)
// {
//     double pi=3.141592653589793;
//     int c1, c2, par;
//     c1 = topo[node*3+1]; c2 = topo[node*3+2]; par = topo[node*3];
//     // TODO: finish this
// }

void angleSpreadExtension(double* pts, int* topo, int numpts, double* deflect_angles, double* container_wedges, 
    double* edge_angles, double* lengths, double* wedge_right_sides, int node)
{
    double pi=3.141592653589793;
    double maxspread = pi/2;
    int dbgct = 0;

    // debugWriteSegments(pts, topo, numpts);

    // get children and parent
    int c1, c2, par, sib;
    c1 = topo[node*3+1]; c2 = topo[node*3+2]; par = topo[node*3];
    if (node==topo[par*3+1]) 
    {
        sib = topo[par*3+2];
    } else {
        sib = topo[par*3+1];
    }
    

    if (!(c1==-1 || c2==-1)) //current node is not a leaf
    {
        // do children first
        angleSpreadExtension(pts, topo, numpts, deflect_angles, container_wedges, edge_angles, lengths, wedge_right_sides, c1);
        angleSpreadExtension(pts, topo, numpts, deflect_angles, container_wedges, edge_angles, lengths, wedge_right_sides, c2);
        if (node ==0 && par != -1) angleSpreadExtension(pts, topo, numpts, deflect_angles, container_wedges, edge_angles, lengths, wedge_right_sides, par);

        double parx, pary, x0, y0, edge_angle, maxlen, mlc1, mlc2, maxClockRot, maxCounterRot, cwsize, defl1, defl2, rightwedge, leftwedge;
        // TODO: add command here to flip the clades if the longer one is on the outside.
        
        parx = pts[par*2]; pary = pts[par*2+1];
        x0 = pts[node*2]; y0 = pts[node*2+1];
        maxlen = maxLengthToTip(lengths, topo, node, par);
        edge_angle = atan2(y0-pary, x0-parx);
        defl1 = deflect_angles[c1]; defl2 = deflect_angles[c2];

        double lim_p2[2];
        cwsize = container_wedges[node];

        FILE *expandpts = fopen("/Users/michaelnute/Dropbox/Grad School/Phylogenetics/work/tree_ops/expandpts.tsv","a");
        // do counterclockwise side first
        lim_p2[0] = parx+(2*maxlen)*cos(edge_angle+cwsize/2);
        lim_p2[1] = pary+(2*maxlen)*sin(edge_angle+cwsize/2); //TODO: make it so this can handle arbitrary edge placements within a wedge
        if (defl1>defl2) {
            maxCounterRot = maxLeafRotationRange(pts, topo, numpts, c1, &pts[node*2], &pts[par*2], &lim_p2[0]);
            fprintf(expandpts, "ctr\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n",node,c1, pts[node*2], pts[node*2+1],pts[par*2],pts[par*2+1], lim_p2[0], lim_p2[1],maxCounterRot );
            deflect_angles[c1]+=maxCounterRot;
        } else {
            maxCounterRot = maxLeafRotationRange(pts, topo, numpts, c2, &pts[node*2], &pts[par*2], &lim_p2[0]);
            fprintf(expandpts, "ctr\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n",node, c2, pts[node*2], pts[node*2+1],pts[par*2],pts[par*2+1], lim_p2[0], lim_p2[1], maxCounterRot );
            deflect_angles[c2]+=maxCounterRot;
        }

        // then clockwise side
        lim_p2[0] = parx+(2*maxlen)*cos(edge_angle-cwsize/2);
        lim_p2[1] = pary+(2*maxlen)*sin(edge_angle-cwsize/2);
        if (defl1>defl2) {
            maxClockRot = maxLeafRotationRange(pts, topo, numpts, c2, &pts[node*2], &pts[par*2], &lim_p2[0]);
            fprintf(expandpts, "clk\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n",node, c1, pts[node*2], pts[node*2+1],pts[par*2],pts[par*2+1], lim_p2[0], lim_p2[1], maxClockRot );
            deflect_angles[c2]-=maxClockRot;
        } else {
            maxClockRot = maxLeafRotationRange(pts, topo, numpts, c1, &pts[node*2], &pts[par*2], &lim_p2[0]);
            fprintf(expandpts, "clk\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n",node, c1, pts[node*2], pts[node*2+1],pts[par*2],pts[par*2+1], lim_p2[0], lim_p2[1], maxClockRot );
            deflect_angles[c1]-=maxClockRot;
        }

        fclose(expandpts);
        // struct timespec tim, tim2;
        // tim.tv_sec = 0;
        // tim.tv_nsec = 500000000;
        // nanosleep(&tim, &tim2); 
        
        // uncomment for mac
        // atomic_thread_fence(memory_order_acquire);
        // atomic_thread_fence(memory_order_release);

        relocateSubtreeByDeflectionAngles(deflect_angles, edge_angles, lengths, pts, topo, numpts, node);

        



    }
}

void testCheckRotationAngle()
{
    double *origin = (double *)malloc(2 * sizeof(double));
    double *pivot = (double *)malloc(2 * sizeof(double));
    double *p1 = (double *)malloc(2 * sizeof(double));
    double *p2 = (double *)malloc(2 * sizeof(double));
origin[0]=3.210524;
origin[1]=1.453977;
pivot[0]=3.757378;
pivot[1]=1.631661;
p1[0]=2.1981;
p1[1]=1.194031;
p2[0]=5.211057;
p2[1]=2.386945;
    double rot;
    rot = getRotationalAngleToSegment(origin,pivot,p1,p2);
    // double pi6=3.141592653589793/6.0;
    printf("angle is %f\n",rot);
    free(origin); free(pivot); free(p1); free(p2);
}

int main()
{
    testCheckRotationAngle();

    /*
    int i;

    int num_nodes;
    FILE *npfile = fopen("num_nodes.bin","rb");
    fread((void*)(&num_nodes),sizeof(int),1,npfile);
    fclose(npfile);
    printf("number of nodes: %d\n",num_nodes);
    
    double *pts = (double *)malloc(num_nodes * 2 * sizeof(double));
    FILE *xfile = fopen("pts_nparr.bin","rb");
    fread((void*)(pts),sizeof(double),num_nodes*2,xfile);
    fclose(xfile);
    for (i=0;i<5;i++) {
        printf("%f\t%f\n",pts[i*2],pts[i*2+1] );
    }
    printf("\n");*/

    // double *edge_angles = (double *)malloc(num_nodes * sizeof(double));
    // FILE *eafile = fopen("edge_angles.bin","rb");
    // fread((void*)(edge_angles),sizeof(double),num_nodes,eafile);
    // fclose(eafile);

    // double *deflect_angles = (double *)malloc(num_nodes * sizeof(double));
    // FILE *dafile = fopen("deflect_angles.bin","rb");
    // fread((void*)(deflect_angles),sizeof(double),num_nodes,dafile);
    // fclose(dafile);


    // double *lengths = (double *)malloc(num_nodes * sizeof(double));
    // FILE *lfile = fopen("lengths.bin","rb");
    // fread((void*)(lengths),sizeof(double),num_nodes,lfile);
    // fclose(lfile);
    
    // topology is laid out in an array where each row is (parent, child1, child2)
    /*int *topo = (int *)malloc(num_nodes*3 * sizeof(int));
    FILE *topofile = fopen("topo.bin","rb");
    fread((void*)(topo),sizeof(int),num_nodes * 3,topofile);
    fclose(topofile);
    printf("topology:\n");

    
    double *deflect_angles2 = (double *)malloc(num_nodes * 1 * sizeof(double)); //deflection angles
    double *edge_angles2 = (double *)malloc(num_nodes * 1 * sizeof(double)); //actual edge angles
    computeEdgeDeflectionAngle(deflect_angles2, edge_angles2, pts, topo, num_nodes,0);
    double *lengths2 = (double *)malloc(num_nodes * 1 * sizeof(double)); //lengths
    computeLengths(lengths2, pts, topo, num_nodes, 0);

    for (i=0;i<num_nodes;i++) { 
        printf("%d )\t%d\t%d\t%d\t%f\n",i,topo[i*3],topo[i*3+1],topo[i*3+2], deflect_angles2[i]);
    }
    
    FILE *segs = fopen("segs.tsv","w");
    for (i=1;i<num_nodes; i++) {
        fprintf(segs,"%f\t%f\t%f\t%f\n",pts[topo[i*3]*2],pts[topo[i*3]*2+1],pts[i*2],pts[i*2+1]);
    }
    fclose(segs);

    int startnode;
    int awayfrom;

    startnode = 0;
    awayfrom = 1;

    FILE *clockpts = fopen("clockpts.tsv","w");
    
    int num_branches;
    num_branches = countBranchesToSideLeaf(pts, topo, startnode, awayfrom, 1);
    double* brs = (double *)malloc((num_branches+2) * 2 * sizeof(double));
    getBranchesToSideLeaf(pts, topo, startnode, awayfrom, 1, brs);
    printf("num_branches = %d\n", num_branches);
    for (i=0;i<num_branches+1; i++) {
        fprintf(clockpts,"%f\t%f\n",brs[i*2],brs[i*2+1]);
    }
    fclose(clockpts);
    // free(brs);

    
    int num_branches2;
    FILE *cclockpts = fopen("counterclockpts.tsv","w");
    num_branches2 = countBranchesToSideLeaf(pts, topo, startnode, awayfrom, 0);
    double* brs2 = (double *)malloc((num_branches2+2) * 2 * sizeof(double));
    getBranchesToSideLeaf(pts, topo, startnode, awayfrom, 0, brs2);
    printf("num_branches = %d\n", num_branches2);
    for (i=0;i<num_branches2+1; i++) {
        fprintf(cclockpts,"%f\t%f\n",brs2[i*2],brs2[i*2+1]);
    }
    fclose(cclockpts);
    


    //get convex hull of leaves outside of this clade
    int *is_away = (int *)malloc(num_nodes * sizeof(int));
    int *is_leaf = (int *)malloc(num_nodes * sizeof(int));
    findLeaves(topo, num_nodes, is_leaf);
    traverseAwayFromClade(pts, topo, is_away, startnode, awayfrom);

    int ptct = 0;
    for (i=0; i<num_nodes; i++)
    {
        if (is_leaf[i]==1 && is_away[i]==1)
        {
            ptct++;
        }
    }
    double *pts_out_of_clade = (double *)malloc(ptct * 2 * sizeof(double));
    ptct=0;
    for (i=0; i<num_nodes; i++)
    {
        if (is_leaf[i]==1 && is_away[i]==1)
        {
            pts_out_of_clade[ptct*2]=pts[i*2];
            pts_out_of_clade[ptct*2+1]=pts[i*2+1];
            ptct++;
        }
    }
    int grahamcount;
    grahamcount = getOuterConvexHull(pts_out_of_clade, ptct, &brs[num_branches*2], &brs2[num_branches2], &pts[startnode*2]);

    
    FILE *midpts = fopen("midpts.tsv","w");
    for (i=0;i<grahamcount;i++)
    {
        fprintf(midpts, "%f\t%f\n", pts_out_of_clade[i*2], pts_out_of_clade[i*2+1] );
    }
    fclose(midpts);

    free(is_away);
    free(is_leaf);
    free(pts_out_of_clade);

    free(brs);
    free(brs2);

    debugTestRightTurnAngle();
*/
    // int *is_away = (int *)malloc(num_nodes * 1 * sizeof(int)); 
    // double *ptscopy = (double *)malloc(num_nodes * 2 * sizeof(double));
    
    // for (i=0;i<num_nodes*2;i++) {
    //     ptscopy[i]=pts[i];
    // }
    // for (i=0;i<num_nodes;i++) {
    //     printf("%d )\t%f\t%f\t\t%f\t%f\t\t%f\t%f\n",i,edge_angles[i], edge_angles2[i], deflect_angles[i], deflect_angles2[i],lengths[i],lengths2[i]);
    // }
    // printf("\n\n");

    // centerCladeRotationally(pts, topo, edge_angles, deflect_angles, lengths, num_nodes, 1);
    
    // for (i=0;i<num_nodes; i++){
    //     printf("%d )\t%f\t%f\t\t%f\t%f\n",i,pts[i*2],pts[i*2+1],ptscopy[i*2],ptscopy[i*2+1]);
    // }
    

    // int i;
    // for (i=0; i<num_nodes; i++) {
    //     nodesbelow[i] = -1;
    // }
    // computeNodesBelow(nodesbelow, topo, num_nodes,0);
    
    // double *pts_away;
    // pts_away = getPtsAwayFromClade(pts, topo, num_nodes,2,3, is_away);
    // int num_away = 0;
    // for (i=0; i<num_nodes; i++) {num_away+=is_away[i];}
    

    // double *pts = (double *)malloc(100 * 2 * sizeof(double));
    // FILE *xfile = fopen("grid.bin","rb");
    // fread((void*)(pts),sizeof(double),100*2,xfile);
    // fclose(xfile);
    // double *ptscopy = (double *)malloc(100 * 2 * sizeof(double));
    // for (j=0;j < 100; j++) {
    //     ptscopy[j*2]=pts[j*2];
    //     ptscopy[j*2+1] = pts[j*2+1];
    // }
    // qsort(pts,100,2*sizeof(double),compareRotationallyTo45DegLine);
    // printPts(pts,100);


    // i=compareLexicographically((void *)&pts_away[1*2], (void *) &pts_away[2*2]);
    // printf("%d\n",i);
    // for (i=0; i<num_away; i++) {
        // printf("%f\t%f\n",edge_angles[i],deflect_angles[i]);
        // printf("%d\t",nodesbelow[i]);
        // printf("%f\t%f\n",pts_away[i*2],pts_away[i*2+1]);
    // }
    
    // qsort(pts_away,5,2*sizeof(double),compareLexicographically);
    // reverseArray(pts_away,5);
    // int i;
    // i=grahamInPlaceHull(pts,100);
    // printPts(pts,100);
    // printf("first %d points\n",i);
    // for (i=0; i<num_away; i++) {
        // printf("%f\t%f\n",pts_away[i*2],pts_away[i*2+1]);
    // }
    
    
    return 0;
}

