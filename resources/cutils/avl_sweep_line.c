#include<stdio.h>
#include<stdlib.h>
#define FOO_API __declspec(dllexport)
// #include<stdbool.h>

/* Row-major order*/
#define pind(i,j) (i)*2+j
#define sind(i,j) (i)*4+j
 
// An AVL tree node
struct Node
{
    int key;
    struct Node *left;
    struct Node *right;
    int height;
    int seg_id;
};
 
// A utility function to get maximum of two integers
int mymax(int a, int b);
 
// A utility function to get height of the tree
int height(struct Node *N)
{
    if (N == NULL)
        return 0;
    return N->height;
}
 
// A utility function to get maximum of two integers
int mymax(int a, int b)
{
    return (a > b)? a : b;
}
 
/* Helper function that allocates a new node with the given key and
    NULL left and right pointers. */
struct Node* newNode(int key, int seg_id)
{
    struct Node* node = (struct Node*)
                        malloc(sizeof(struct Node));
    node->key   = key;
    node->left   = NULL;
    node->right  = NULL;
    node->height = 1;  // new node is initially added at leaf
    node->seg_id = seg_id;
    return(node);
}
 
// A utility function to right rotate subtree rooted with y
// See the diagram given above.
struct Node *rightRotate(struct Node *y)
{
    struct Node *x = y->left;
    struct Node *T2 = x->right;
 
    // Perform rotation
    x->right = y;
    y->left = T2;
 
    // Update heights
    y->height = mymax(height(y->left), height(y->right))+1;
    x->height = mymax(height(x->left), height(x->right))+1;
 
    // Return new root
    return x;
}
 
// A utility function to left rotate subtree rooted with x
// See the diagram given above.
struct Node *leftRotate(struct Node *x)
{
    struct Node *y = x->right;
    struct Node *T2 = y->left;
 
    // Perform rotation
    y->left = x;
    x->right = T2;
 
    //  Update heights
    x->height = mymax(height(x->left), height(x->right))+1;
    y->height = mymax(height(y->left), height(y->right))+1;
 
    // Return new root
    return y;
}
 
// Get Balance factor of node N
int getBalance(struct Node *N)
{
    if (N == NULL)
        return 0;
    return height(N->left) - height(N->right);
}
 
struct Node* insert(struct Node* node, int key, int seg_id)
{
    /* 1.  Perform the normal BST rotation */
    if (node == NULL)
        return(newNode(key, seg_id));
 
    if (key < node->key)
        node->left  = insert(node->left, key, seg_id);
    else if (key > node->key)
        node->right = insert(node->right, key, seg_id);
    else // Equal keys not allowed
        return node;
 
    /* 2. Update height of this ancestor node */
    node->height = 1 + mymax(height(node->left),
                           height(node->right));
 
    /* 3. Get the balance factor of this ancestor
          node to check whether this node became
          unbalanced */
    int balance = getBalance(node);
 
    // If this node becomes unbalanced, then there are 4 cases
 
    // Left Left Case
    if (balance > 1 && key < node->left->key)
        return rightRotate(node);
 
    // Right Right Case
    if (balance < -1 && key > node->right->key)
        return leftRotate(node);
 
    // Left Right Case
    if (balance > 1 && key > node->left->key)
    {
        node->left =  leftRotate(node->left);
        return rightRotate(node);
    }
 
    // Right Left Case
    if (balance < -1 && key < node->right->key)
    {
        node->right = rightRotate(node->right);
        return leftRotate(node);
    }
 
    /* return the (unchanged) node pointer */
    return node;
}
 
/* Given a non-empty binary search tree, return the
   node with minimum key value found in that tree.
   Note that the entire tree does not need to be
   searched. */
struct Node * minValueNode(struct Node* node)
{
    struct Node* current = node;
 
    /* loop down to find the leftmost leaf */
    while (current->left != NULL)
        current = current->left;
 
    return current;
}

struct Node * maxValueNode(struct Node* node)
{
    struct Node* current = node;
 
    /* loop down to find the leftmost leaf */
    while (current->right != NULL)
        current = current->right;
 
    return current;
}

/* Given a non-empty binary search tree, return the
   node with a specified key value found in that tree. */
struct Node * getNodeWithKey(struct Node* node, int key)
{
    if (node == NULL) return NULL;
    
    struct Node* current = node;
    if (current->key == key) return current;
    if (key < current->key) 
    { 
        current = current->left;
        return getNodeWithKey(current,key);
    } else {
        current = current->right;
        return getNodeWithKey(current,key);
    }
}

struct Node * getParentNode(struct Node* root, int key)
{
    if (root == NULL) return NULL;
    
    struct Node* current = root;
    if (current->key == key) return NULL;
    if (key < current->key) 
    { 
        if (key == current->left->key) 
        {
            return current;
        } else {
            current = current->left;
            return getParentNode(current,key);
        }
    } else {
        if (key == current->right->key) 
        {
            return current;
        } else {
            current = current->right;
            return getParentNode(current,key);
        }
    }
}
void printOneNode(struct Node* nd)
{
    printf("key %d, address: %x\n",nd->key,*nd);
}

struct Node * getPredecessorNode(struct Node* root, int key )
{
    struct Node* current = getNodeWithKey(root, key);
    struct Node* minnode = minValueNode(root);
    if (key == minnode->key) return NULL;

    // CASE 1: it has a left subtree (easy):
    if (current->left != NULL) return maxValueNode(current->left);
    
    
    // CASE 2: it does not (harder):
    struct Node* parent;
    parent = getParentNode(root, key);
    
    struct Node* x = current;
    struct Node* y = parent;
    
    while (y != NULL && x == y->left)
    {
        x = y;
        y = getParentNode(root, y->key);
    }
    
    return y;
}

struct Node * getSuccessorNode(struct Node* root, int key )
{
    struct Node* current = getNodeWithKey(root, key);
    struct Node* maxnode = maxValueNode(root);
    if (key == maxnode->key) return NULL;

    // CASE 1: it has a right subtree (easy):
    if (current->right != NULL) return minValueNode(current->right);
    
    
    // CASE 2: it does not (harder):
    struct Node* parent;
    parent = getParentNode(root, key);
    
    struct Node* x = current;
    struct Node* y = parent;
    
    while (y != NULL && x == y->right)
    {
        x = y;
        y = getParentNode(root, y->key);
    }
    
    return y;
}


void printNodes(struct Node* nd)
{
    if (nd != NULL)
    {
        printf("key %d, address: %x, right: ",nd->key,*nd);
        if (nd->right !=NULL) {
            printf("%d, left: ", nd->right->key);
        } else {
            printf("NULL, left: ");
        }
        if (nd->left != NULL) {
            printf("%d\n",nd->left->key);
        } else {
            printf("NULL\n");
        }
        printNodes(nd->left);
        printNodes(nd->right);
    }
}

// Recursive function to delete a node with given key
// from subtree with given root. It returns root of
// the modified subtree.
struct Node* deleteNode(struct Node* root, int key)
{
    // STEP 1: PERFORM STANDARD BST DELETE
 
    if (root == NULL)
        return root;
 
    // printf("key: %d, rkey: %d; ",key,root->key);
 
    // If the key to be deleted is smaller than the
    // root's key, then it lies in left subtree
    if ( key < root->key )
        root->left = deleteNode(root->left, key);
 
    // If the key to be deleted is greater than the
    // root's key, then it lies in right subtree
    else if( key > root->key )
        root->right = deleteNode(root->right, key);
 
    // if key is same as root's key, then This is
    // the node to be deleted
    else
    {
        // node with only one child or no child
        if( (root->left == NULL) || (root->right == NULL) )
        {
            struct Node *temp = root->left ? root->left :
                                             root->right;
 
            // No child case
            if (temp == NULL)
            {
                // printf("no child case\n"); // MN comment
                temp = root;
                root = NULL;
            }
            else { // One child case
                // printf("one child case\n"); // MN comment
                *root = *temp; // Copy the contents of
                            // the non-empty child
            }
            free(temp);
        }
        else
        {
            // node with two children: Get the inorder
            // successor (smallest in the right subtree)
            struct Node* temp = minValueNode(root->right);
 
            // Copy the inorder successor's data to this node
            root->key = temp->key;
 
            // Delete the inorder successor
            root->right = deleteNode(root->right, temp->key);
        }
    }
 
    // If the tree had only one node then return
    if (root == NULL)
    {
        // printf("tree had only one node case\n");
        return root;
    }
      
 
    // STEP 2: UPDATE HEIGHT OF THE CURRENT NODE
    root->height = 1 + mymax(height(root->left),
                           height(root->right));
 
    // STEP 3: GET THE BALANCE FACTOR OF THIS NODE (to
    // check whether this node became unbalanced)
    int balance = getBalance(root);
 
    // If this node becomes unbalanced, then there are 4 cases
 
    // Left Left Case
    if (balance > 1 && getBalance(root->left) >= 0)
        return rightRotate(root);
 
    // Left Right Case
    if (balance > 1 && getBalance(root->left) < 0)
    {
        root->left =  leftRotate(root->left);
        return rightRotate(root);
    }
 
    // Right Right Case
    if (balance < -1 && getBalance(root->right) <= 0)
        return leftRotate(root);
 
    // Right Left Case
    if (balance < -1 && getBalance(root->right) > 0)
    {
        root->right = rightRotate(root->right);
        return leftRotate(root);
    }
 
    return root;
}
 
// A utility function to print preorder traversal of
// the tree.
// The function also prints height of every node
void preOrder(struct Node *root)
{
    if(root != NULL)
    {
        printf("%d ", root->key);
        preOrder(root->left);
        preOrder(root->right);
    }
}

/* int doIntersect(double x1, double y1, double x2, double y2, double x3, double y3, double x4, double y4)
{
    // if either segment is actually just a point, return false
    double t1, t2, determ;
    double zero = 0.0;
    double one = 1.0;
    
    if ((x1-x2)==0.0 && (y1-y2)==0.0) {
        // printf("\tcase 8\t"); //DEBUG 
        return 0;
    }
    if ((x3-x4)==0.0 && (y3-y4)==0.0) {
        // printf("\tcase 9\t"); //DEBUG
        return 0;
    }
    
    determ = (x2-x1)*(y3-y4)-(x3-x4)*(y2-y1);
    printf("determ: %f\n", determ);
    
    // if the lines are parallel, check cases:
    if (determ==0.0) 
    {
        if (x2-x1==0)   // lines are vertical
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
        } else if (y2 - y1==0) {
            // lines are horizontal
            if (y3==y2)
            {
                t1 = (x3-x1) / (x2-x1);
                t2 = (x4-x1) / (x2-x1);
                // printf("\tcase 3\t"); //DEBUG
                return ((t1 > 0 && t1 < 1) || (t2 > 0 && t2 < 1));
            } else {
                // printf("\tcase 4\t"); //DEBUG
                return 0;
            }            
        } else {
            t1 = (x3-x1) / (x2-x1);
            t2 = (y3-y1) / (y2-y1);
            if (t1==t2 && t1 >0 && t2 > 0 && t1 < 1 && t2 < 1) {
                // printf("\tcase 5\t");  //DEBUG
                return 1;
            }
            t1 = (x4-x1) / (x2-x1);
            t2 = (y4-y1) / (y2-y1);
            if (t1==t2 && t1 >0 && t2 > 0 && t1 < 1 && t2 < 1) {
                // printf("\tcase 6\t");  //DEBUG
                return 1;
            } else {
                // printf("\tcase 7\t");  //DEBUG
                return 0;
            }
        }
    }
    
    unsigned long long t1l, t2l;
    t1 = ((y3-y4)*(x3-x1)+(x4-x3)*(y3-y1))/determ;
    t2 = ((y1-y2)*(x3-x1)+(x2-x1)*(y3-y1))/determ;
    printf("\tt1: %e\tt2: %e\n", t1,t2); //DEBUG
    if (t1<1.0) 
    {
        t1l = * (unsigned long long *) &t1;
        printf("t1 < 1: %llx\n",t1l);
    }
    if (t2<1.0)
    {
        t2l = * (unsigned long long *) &t2;
        printf("t2 < 1: %llx\n",t2l);
    }
    if (t1 > 0 && t1 < 1 && t2 > 0 && t2 < 1)
    {
        return 1;
    } else {
        return 0;
    }
}
 */
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
    
    // unsigned long long t1l, t2l;
    t1 = ((y3-y4)*(x3-x1)+(x4-x3)*(y3-y1))/determ;
    t2 = ((y1-y2)*(x3-x1)+(x2-x1)*(y3-y1))/determ;
    // printf("\tt1: %e\tt2: %e\n", t1,t2); //DEBUG
    // if (t1<one) 
    // {
        // t1l = * (long long *) &t1;
        // printf("t1 < 1: %llx\n",t1l);
    // }
    // if (t2<one)
    // {
        // t2l = * (long long *) &t2;
        // printf("t2 < 1: %llx\n",t2l);
    // }
    if (t1 > 0 && t1 < 0.9999999999999 && t2 > 0 && t2 < 0.9999999999999)
    {
        return 1;
    } else {
        return 0;
    }
}

// wrapper to simplify the doIntersect call
int diw(double* s1, double* s2)
{
    double x1, y1, x2, y2, x3, y3, x4, y4;
    int res;
    x1 = s1[0];
    y1 = s1[1];
    x2 = s1[2];
    y2 = s1[3];
    x3 = s2[0];
    y3 = s2[1];
    x4 = s2[2];
    y4 = s2[3];
    // printf("\tchecking:\n\t%f\t%f\t%f\t%f\n\t%f\t%f\t%f\t%f\n",x1, y1, x2, y2, x3, y3, x4, y4);
    // return 0;
    res=doIntersect(x1, y1, x2, y2, x3, y3, x4, y4);
    if (res==1) {
        printf("intersecting points:\n");
        printf("\t%f\t%f\t%f\t%f\n\t%f\t%f\t%f\t%f\n",x1, y1, x2, y2, x3, y3, x4, y4);
    }
    // printf("\tresult: %d\n",res);
    return res;
}

// FOO_API int sweepLineIntersect(double* os, int* all_inds, int* keys, int num_pts)
int sweepLineIntersect(double* os, int* all_inds, int* keys, int num_pts)
{
    // this function returns 0 if there is an intersection and 1 if there is not.
    int start_pt = 0;
    int wait = 1;
    
    struct Node *root = NULL;
    struct Node *curr_node = NULL;
    
    // if the same segment is in the first two spots, move to the next two.
    while(wait)
    {
        if (all_inds[pind(start_pt,1)] != all_inds[pind(start_pt+1,1)])
        {
            wait = 0;
            if (diw(&os[all_inds[pind(start_pt,1)]*4],&os[all_inds[pind(start_pt+1,1)]*4])) return 0;
            root = insert(root, keys[all_inds[pind(start_pt,1)]],all_inds[pind(start_pt,1)]);
        } else {
            start_pt += 2;
            if (start_pt >= 2*num_pts) return 1;
        }
    }
    // printf("done with the wait step\n");    //DEBUG
    
    int i, curr, pred, succ, currkey, is_right;
    struct Node *pred_node;
    struct Node *succ_node;
    
    
    for (i=start_pt+1; i<2*num_pts; i++) 
    {
        curr = all_inds[pind(i,1)];
        currkey = keys[curr];
        is_right = all_inds[pind(i,0)];
        // printf("i: %d\tcu: %d\tkey: %d\tright: %d\n",i, curr, currkey, is_right);    //DEBUG
        // printf("%f\t%f\t%f\t%f\n", os[sind(curr,0)],os[sind(curr,1)],os[sind(curr,2)],os[sind(curr,3)]);    //DEBUG
        // printf("tree: ");//DEBUG
        // preOrder(root);//DEBUG
        // printf("\n");//DEBUG
        
        if (all_inds[pind(i,0)]==0)
        {
            // if the current point is a left point:
            // printf("\tleft pt: inserting into tree\n"); //DEBUG
            root = insert(root, currkey,curr);
            // preOrder(root); //DEBUG
            // printf("\n");
            // if (i==25) {
                // printNodes(root);
            // }
            curr_node = getNodeWithKey(root, currkey);
            pred_node = getPredecessorNode(root, curr_node->key);
            succ_node = getSuccessorNode(root, curr_node->key);
            // if (succ_node!=NULL) {
                // printf("\tsuccessor node: %d", succ_node->key);
            // }
            
            
            //check the predecessor node:
            if (pred_node != NULL) 
            {
                // printf("\tchecking predecessor in tree\n"); //DEBUG
                pred = pred_node->seg_id;
                if (diw(&os[curr*4],&os[pred*4])) return 0;
            }
            
            //check the successor node:
            if (succ_node != NULL) 
            {
                // printf("\tchecking successor in tree\n"); //DEBUG
                succ = succ_node->seg_id;
                if (diw(&os[curr*4],&os[succ*4])) return 0;
            }
        } else {
            // printf("\tright pt:");    //DEBUG
            
            // current point is a right point
            if (root == NULL) 
            {
                printf("ERROR: right node reached with nothing in the tree");
                return -1;
            } else {
                curr_node = getNodeWithKey(root, currkey);
                pred_node = getPredecessorNode(root, curr_node->key);
                succ_node = getSuccessorNode(root, curr_node->key);
                if (pred_node != NULL && succ_node != NULL) 
                {
                    // printf("\tin the pred-succ loop\n");  //DEBUG
                    // pred_node = getPredecessorNode(root, curr_node->key);
                    pred = pred_node->seg_id;
                    // succ_node = getSuccessorNode(root, curr_node->key);
                    succ = succ_node->seg_id;
                    if (diw(&os[pred*4],&os[succ*4])) return 0;
                }
                // preOrder(root); //DEBUG
                // printf("\tdeleting node: %d\n", currkey);  //DEBUG
                root = deleteNode(root, currkey);
                // TODO: Modify this to handle ties.
            }
        }
    }
    // printf("returning 1\n");    //DEBUG
    return 1;
}
 
int main()
{
    int np;
    FILE *npfile = fopen("num_pts.bin","rb");
    fread((void*)(&np),sizeof(int),1,npfile);
    fclose(npfile);
    printf("points: %d\n",np);
    
    
    double *pts = (double *)malloc(np * 4 * sizeof(double));
    FILE *xfile = fopen("test.bin","rb");
    fread((void*)(pts),sizeof(double),np*4,xfile);
    fclose(xfile);
    
    int *inds = (int *)malloc(np*4 * sizeof(int));
    FILE *xifile = fopen("test_inds.bin","rb");
    fread((void*)(inds),sizeof(int),np * 4,xifile);
    fclose(xifile);
    
    int *keys = (int *)malloc(np * sizeof(int));
    FILE *kfile = fopen("test_keys.bin","rb");
    fread((void*)(keys),sizeof(int),np,kfile);
    fclose(kfile);
  
    int i;
    i = sweepLineIntersect(&pts[0], &inds[0], &keys[0], np);
    printf("result (1=no intersect): %d\n",i);
 
    /*
    printf("ordered_segs (*pts):\n");
    for (i=0; i<20; i++) 
    {
        printf("%f\t%f\t%f\t%f\n",pts[i*4], pts[i*4+1], pts[i*4+2], pts[i*4+3]);
    }
    
    printf("inds:\n");
    for (i=0; i<20; i++) 
    {
        printf("%d\t%d\t\t\t%d\t%d\n",inds[i*2], inds[i*2+1], inds[i*2+20], inds[i*2+20+1]);
    }
    
    printf("keys:\n");
    for (i=0; i<5; i++) 
    {
        printf("%d\t%d\t%d\t%d\n",keys[i*4], keys[i*4+1], keys[i*4+2], keys[i*4+3]);
    }
    */
    
    
    
    return 0;
} 

/*
int main()
{
    struct Node *root = NULL;
    
    root = insert(root, 9, 1);
    root = insert(root, 5, 2);
    root = insert(root, 10, 3);
    root = insert(root, 0, 4);
    root = insert(root, 6, 5);
    root = insert(root, 11, 6);
    root = insert(root, -1, 7);
    root = insert(root, 1, 8);
    root = insert(root, 2, 9);
    
    printNodes(root);
    
    struct Node *mypred = getPredecessorNode(root, 6);
    struct Node *mysucc = getSuccessorNode(root, 5);
    preOrder(root);
    printf("\n");
    printf("%d pred is %d\n",6, mypred->key);
    printf("%d succ is %d\n",5, mysucc->key);
    
    
    mypred = getPredecessorNode(root, 9);
    mysucc = getSuccessorNode(root, 6);
    printf("%d pred is %d\n",9, mypred->key);
    printf("%d succ is %d\n",6, mysucc->key);
    
    
    mypred = getPredecessorNode(root, 2);
    mysucc = getSuccessorNode(root, 1);
    printf("%d pred is %d\n",2, mypred->key);
    printf("%d succ is %d\n",1, mysucc->key);
    
    return 0;
} */

/* Drier program to test above function*/
/*
int main()
{
  struct Node *root = NULL;
 
  // Constructing tree given in the above figure
    root = insert(root, 9);
    root = insert(root, 5);
    root = insert(root, 10);
    root = insert(root, 0);
    root = insert(root, 6);
    root = insert(root, 11);
    root = insert(root, -1);
    root = insert(root, 1);
    root = insert(root, 2);
 
    //The constructed AVL Tree would be
    //        9
    //       /  \
    //      1    10
    //    /  \     \
    //   0    5     11
    //  /    /  \
    // -1   2    6
    
 
    printf("Preorder traversal of the constructed AVL "
           "tree is \n");
    preOrder(root);
 
    root = deleteNode(root, 10);
 
    // The AVL Tree after deletion of 10
    //        1
    //       /  \
    //      0    9
    //    /     /  \
    //   -1    5     11
    //       /  \
    //      2    6
    
 
    printf("\nPreorder traversal after deletion of 10 \n");
    preOrder(root);
 
    return 0;
}
*/ 