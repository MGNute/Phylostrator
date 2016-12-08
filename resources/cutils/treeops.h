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
void findLeaves(int* topo, int numpts, int* is_leaf);
int rightTurn(double* a, double* b, double* c);
void printPts(double* pts, int size);
int grahamInPlaceScan(double* pts_away, int num_pts, int upper);
int grahamInPlaceHull(double* pts_away, int num_pts);
int compareRotationallyTo45DegLine(const void * a, const void * b);
void pivotPointsAround(double* pts, double* origin, double* deg45pt, int num_pts);
int getOuterConvexHull(double* pts_in_clade, int num_in_clade, double* sidept1, double* sidept2, double* origin);
double myatan2(double x, double y, int shiftneg);
double ptsRightTurnAngle(double* pts, int i1, int i2, int i3);
double arraysRightTurnAngle(double* p1, double* p2, double* p3);
void updateMinAngles(double currangle, double* minClockwiseAngle, double* minCounterClockwiseAngle);
double maxLengthToTip(double* lengths, int* topo, int index, int away_from);
int nearestBranchToPoint(double* pts, int* topo, int numpts, double x0, double y0, int* is_away);
int nearestBranchToNode(double* pts, int* topo, int numpts, int index, int* is_away);
void centerCladeRotationally(double* pts, int* topo, double* edge_angles, double* deflect_angles, double* lengths, 
                             int numpts, int node);
void getBranchesToSideLeaf(double* pts, int* topo, int startnode, int awayFromNode, int clockwise, double* branch_points);
int countBranchesToSideLeaf(double* pts, int* topo, int startnode, int awayFromNode, int clockwise);
int find45DegreeCutoffInSortedPoints(double* pts, int numpts, int below);
void zeroOutDoubleArray(double* pts, int numpts);
double maxLeafRotationRange(double* pts, int* topo, int numpts, int node, double* origin, double* lim_p1, double* lim_p2);
void angleSpreadExtension(double* pts, int* topo, int numpts, double* deflect_angles, double* container_wedges, 
    double* edge_angles, double* lengths, double* wedge_right_sides, int node);

#endif