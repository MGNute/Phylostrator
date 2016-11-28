#ifndef TREEOPS_H
#define TREEOPS_H

void computeEdgeDeflectionAngle(double* deflect, double* edge_angles, double* pts, int* topo, int num_nodes, int index);
void computeLengths(double* lengths, double* pts, int* topo, int num_nodes, int index);
void relocateSubtreeByDeflectionAngles(double* deflect, double* edge_angles, double* lengths, double* pts, int* topo, int num_nodes, int index);
void computeNodesBelow(int* nodesbelow, int* topo, int num_nodes, int index);
void traverseAwayFromClade(double* pts, int* topo, int* is_away, int index, int called_from);
double* getPtsAwayFromClade(double* pts, int* topo, int num_nodes, int from_index, int in_direction_of, int* is_away);
int compareLexicographically(const void * a, const void * b);
void reverseArray(double* pts_away, int numpts);
int rightTurn(double* a, double* b, double* c);
void printPts(double* pts, int size);
int grahamInPlaceScan(double* pts_away, int num_pts, int upper);
void pivotPointsAround(double* pts, double* origin, double* deg45pt, int num_pts);
double sq(double x);
double getRotationalAngleToSegment(double* origin, double* radial_pt, double* seg_p1, double* seg_p2);
void centerCladeRotationally(double* pts, int* topo, double* edge_angles, double* deflect_angles, double* lengths, 
                             int numpts, int node);

#endif