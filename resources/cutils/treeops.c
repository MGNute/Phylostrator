#include<stdio.h>
#include<stdlib.h>
#include<math.h>
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


double sq(double x)
{
    return x*x;
}

double getRotationalAngleToSegment(double* origin, double* radial_pt, double* seg_p1, double* seg_p2)
{
    double rad, dp1, dp2;
    rad = sqrt(sq(origin[0]-radial_pt[0])+sq(origin[1]-radial_pt[1]));
    dp1 = sqrt(sq(origin[0]-seg_p1[0])+sq(origin[1]-seg_p1[1]));
    dp2 = sqrt(sq(origin[0]-seg_p2[0])+sq(origin[1]-seg_p2[1]));
    
    // if the radius does not intersect along the line segment, return NaN
    if (!(((dp1<=rad) &&(rad<=dp2)) || ((dp2<=rad) &&(rad<=dp1)))) 
    {
        // printf("radius does not intersect segment\n");
        // printf("dp1: %f\tdp2: %f\trad:\t%f\n",dp1,dp2,rad);
        return nan("");
    }

    // otherwise find the intersection point
    double t1, a0,b0, a1, b1, x0,y0, A,B,C, xnew, ynew, theta_cos;
    a0 = seg_p1[0]; b0 = seg_p1[1];
    a1 = seg_p2[0]; b1 = seg_p2[1];
    x0 = origin[0]; y0 = origin[0];
    A = sq(a0-a1)+sq(b0-b1);
    B = 2*((a0-a1)*(a1-x0) + (b0-b1)*(b1-y0)  );
    C = sq(a1-x0)+sq(b1-y0)-sq(rad);
    t1 = (-B + sqrt(sq(B)-4*A*C))/(2*A);
    if (t1>=0 && t1 <= 1.0)
    {
        xnew = a1+t1*(a0-a1);
        ynew = b1+t1*(b0-b1);
        theta_cos = ((radial_pt[0]-origin[0])*(xnew-origin[0])+(radial_pt[1]-origin[1])*(xnew-origin[1]))/sq(rad);
        // printf("theta_cos (t1): %f\n",theta_cos);
        return acos(theta_cos);
    } else {
        t1 = (-B - sqrt(sq(B)-4*A*C))/(2*A);
        if (t1>=0 && t1 <= 1.0)
        {
            xnew = a1+t1*(a0-a1);
            ynew = b1+t1*(b0-b1);
            theta_cos = ((radial_pt[0]-origin[0])*(xnew-origin[0])+(radial_pt[1]-origin[1])*(xnew-origin[1]))/sq(rad);
            // printf("theta_cos (t2): %f\n",theta_cos);
            return acos(theta_cos);
        }
    }
    return nan("");
}

// TREEOPS_API void centerCladeRotationally(double* pts, int* topo, double* edge_angles, double* deflect_angles, double* lengths, 
                             // int numpts, int node)
void centerCladeRotationally(double* pts, int* topo, double* edge_angles, double* deflect_angles, double* lengths, 
                             int numpts, int node)
{
    printf("numpts is %d\n",numpts);
    int *is_away = (int *)malloc(numpts * sizeof(int));
    int parent = topo[node*3];
    double myx, myy, parx, pary;
    double pi=3.141592653589793;
    myx = pts[node*2];
    myy = pts[node*2+1];

    // get the points in the clade and external to the clade
    int num_out, num_out_chull, num_in, num_in_chull, i, j ;
    
    // pts_out_of_clade = getPtsAwayFromClade(pts, topo, numpts, node, parent, is_away);
    traverseAwayFromClade(pts, topo, is_away, parent, node);
    num_out = 0; num_in = 0;
    for (i=0;i<numpts; i++) {
        // count the points
        if (is_away[i]==1) {
            num_out++;    
        } else {
            num_in++;
        }
    }
    double* pts_out_of_clade = (double *)malloc(2*num_out * sizeof(double));
    double* pts_in_clade = (double *)malloc(2*num_in * sizeof(double)); 
    int inct, outct;
    inct = 0; outct = 0;
    for (i=0;i<numpts;i++)
    {
        if (is_away[i]==1) {
            pts_out_of_clade[outct*2] = pts[i*2];
            pts_out_of_clade[outct*2+1] = pts[i*2+1];
            outct++;
        } else {
            pts_in_clade[inct*2] = pts[i*2];
            pts_in_clade[inct*2+1] = pts[i*2+1];
            inct++;            
        }
    }
    double* origin = (double *)malloc(2 * sizeof(double));
    origin[0]=0.0;
    origin[1]=0.0;
    pivotPointsAround(pts_out_of_clade,&pts[parent*2],&pts[node*2],num_out);

    
    // pts_in_clade = getPtsAwayFromClade(pts, topo, numpts, parent, node, is_away);
    // for (i=0;i<numpts;i++) {
        // num_in++;
    // }
    pivotPointsAround(pts_in_clade,&pts[parent*2],&pts[node*2],num_in);

    // get counterclockwise ("upper") angle of rotation:
    num_out_chull = grahamInPlaceScan(pts_out_of_clade,num_out,1);
    num_in_chull = grahamInPlaceScan(pts_in_clade,num_in,1);
    double minClockwiseRotAngle = pi;
    double minCounterClockwiseRotAngle = pi;
    double currangle = 0.0;

    for (i=0; i < num_out_chull-1; i++)
    {
        for (j=0; j < num_in_chull; j++)
        {
            currangle = getRotationalAngleToSegment(&origin[0], &pts_in_clade[j*2],&pts_out_of_clade[i*2], &pts_out_of_clade[(i+1)*2] );
            // currangle = getRotationalAngleToSegment(&pts[parent*2], &pts_in_clade[j*2],&pts_out_of_clade[i*2], &pts_out_of_clade[(i+1)*2] );
            if (!(isnan(currangle)) && currangle < minCounterClockwiseRotAngle) {
                minCounterClockwiseRotAngle = currangle;
            }
        }
    }
    for (j=0; j < num_in_chull; j++)
    {
        currangle = getRotationalAngleToSegment(&origin[0], &pts_in_clade[j*2],&pts_out_of_clade[num_out_chull*2], &pts_out_of_clade[0] );
        // currangle = getRotationalAngleToSegment(&pts[parent*2], &pts_in_clade[j*2],&pts_out_of_clade[num_out_chull*2], &pts_out_of_clade[0] );
        if (!(isnan(currangle)) && currangle < minCounterClockwiseRotAngle) {
            minCounterClockwiseRotAngle = currangle;
        }
    }

    // get clockwise ("lower") angle of rotation
    currangle = 0.0;
    num_out_chull = grahamInPlaceScan(pts_out_of_clade,num_out,0);
    num_in_chull = grahamInPlaceScan(pts_in_clade,num_in,0);
    for (i=0; i < num_out_chull-1; i++)
    {
        for (j=0; j < num_in_chull; j++)
        {
            currangle = getRotationalAngleToSegment(&origin[0], &pts_in_clade[j*2],&pts_out_of_clade[i*2], &pts_out_of_clade[(i+1)*2] );
            // currangle = getRotationalAngleToSegment(&pts[parent*2], &pts_in_clade[j*2],&pts_out_of_clade[i*2], &pts_out_of_clade[(i+1)*2] );
            if (!(isnan(currangle)) && currangle < minClockwiseRotAngle) {
                minClockwiseRotAngle = currangle;
            }
        }
    }
    for (j=0; j < num_in_chull; j++)
    {
        currangle = getRotationalAngleToSegment(&origin[0], &pts_in_clade[j*2],&pts_out_of_clade[num_out_chull*2], &pts_out_of_clade[0] );
        // currangle = getRotationalAngleToSegment(&pts[parent*2], &pts_in_clade[j*2],&pts_out_of_clade[num_out_chull*2], &pts_out_of_clade[0] );
        if (!(isnan(currangle)) && currangle < minClockwiseRotAngle) {
            minClockwiseRotAngle = currangle;
        }
    }
    printf("clockwise: %f\tcounter: %f\n", minClockwiseRotAngle, minCounterClockwiseRotAngle);

    if (!(isnan(minClockwiseRotAngle)) && !(isnan(minCounterClockwiseRotAngle)))
    {
        deflect_angles[node]+=(minCounterClockwiseRotAngle - minClockwiseRotAngle) / 2;
        relocateSubtreeByDeflectionAngles(deflect_angles,edge_angles, lengths,pts,topo,numpts,0);
    }


    
    free(is_away);
    free(pts_out_of_clade);
    free(pts_in_clade);
    free(origin);


}

void testCheckRotationAngle()
{
    double *origin = (double *)malloc(2 * sizeof(double));
    double *pivot = (double *)malloc(2 * sizeof(double));
    double *p1 = (double *)malloc(2 * sizeof(double));
    double *p2 = (double *)malloc(2 * sizeof(double));
    origin[0]=0.0;
    origin[1]=0.0;
    pivot[0]=0.0;
    pivot[1]=3.0;
    p1[0]=0.0;
    p1[1]=1.5;
    p2[0]=6.0;
    p2[1]=1.5;
    double rot;
    rot = getRotationalAngleToSegment(origin,pivot,p1,p2);
    double pi6=3.141592653589793/6.0;
    printf("angle is %f and should be %f\n",rot, pi6);
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
    printf("\n");

    double *edge_angles = (double *)malloc(num_nodes * sizeof(double));
    FILE *eafile = fopen("edge_angles.bin","rb");
    fread((void*)(edge_angles),sizeof(double),num_nodes,eafile);
    fclose(eafile);

    double *deflect_angles = (double *)malloc(num_nodes * sizeof(double));
    FILE *dafile = fopen("deflect_angles.bin","rb");
    fread((void*)(deflect_angles),sizeof(double),num_nodes,dafile);
    fclose(dafile);


    double *lengths = (double *)malloc(num_nodes * sizeof(double));
    FILE *lfile = fopen("lengths.bin","rb");
    fread((void*)(lengths),sizeof(double),num_nodes,lfile);
    fclose(lfile);
    
    // topology is laid out in an array where each row is (parent, child1, child2)
    int *topo = (int *)malloc(num_nodes*3 * sizeof(int));
    FILE *topofile = fopen("topo.bin","rb");
    fread((void*)(topo),sizeof(int),num_nodes * 3,topofile);
    fclose(topofile);
    printf("topology:\n");
    for (i=0;i<num_nodes;i++) { 
        printf("%d )\t%d\t%d\t%d\n",i,topo[i*3],topo[i*3+1],topo[i*3+2] );
    }
    
    double *deflect_angles2 = (double *)malloc(num_nodes * 1 * sizeof(double)); //deflection angles
    double *edge_angles2 = (double *)malloc(num_nodes * 1 * sizeof(double)); //actual edge angles
    computeEdgeDeflectionAngle(deflect_angles2, edge_angles2, pts, topo, num_nodes,0);
    double *lengths2 = (double *)malloc(num_nodes * 1 * sizeof(double)); //lengths
    computeLengths(lengths2, pts, topo, num_nodes, 0);
    
    // int *is_away = (int *)malloc(num_nodes * 1 * sizeof(int)); 
    double *ptscopy = (double *)malloc(num_nodes * 2 * sizeof(double));
    
    for (i=0;i<num_nodes*2;i++) {
        ptscopy[i]=pts[i];
    }
    for (i=0;i<num_nodes;i++) {
        printf("%d )\t%f\t%f\t\t%f\t%f\t\t%f\t%f\n",i,edge_angles[i], edge_angles2[i], deflect_angles[i], deflect_angles2[i],lengths[i],lengths2[i]);
    }
    printf("\n\n");

    centerCladeRotationally(pts, topo, edge_angles, deflect_angles, lengths, num_nodes, 1);
    
    for (i=0;i<num_nodes; i++){
        printf("%d )\t%f\t%f\t\t%f\t%f\n",i,pts[i*2],pts[i*2+1],ptscopy[i*2],ptscopy[i*2+1]);
    }
    */

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
    // i=grahamInPlaceScan(pts,100,0);
    // printPts(pts,100);
    // printf("first %d points\n",i);
    // for (i=0; i<num_away; i++) {
        // printf("%f\t%f\n",pts_away[i*2],pts_away[i*2+1]);
    // }
    
    
    return 0;
}

