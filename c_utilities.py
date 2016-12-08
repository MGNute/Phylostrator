import numpy as np
import ctypes as C
import os, platform

np.seterr(divide='ignore')

if platform.system()=='Windows':
    sweepline = C.CDLL('resources/cutils/avl_sweep_line.dll')
elif platform.system()=='Darwin':
    sweepline = C.CDLL('resources/cutils/avl_sweep_line.dylib')

sweepline.sweepLineIntersect.restype = C.c_int
sweepline.sweepLineIntersect.argtypes = [C.POINTER(C.c_double), C.POINTER(C.c_int), C.POINTER(C.c_int), C.c_int]

if platform.system()=='Windows':
    treeops = C.CDLL('resources/cutils/treeops.dll')
elif platform.system()=='Darwin':
    treeops = C.CDLL('resources/cutils/treeops.dylib')

# treeops.centerCladeRotationally.restype = C.c_void_p
treeops.centerCladeRotationally.restype = None
treeops.centerCladeRotationally.argtypes = [C.POINTER(C.c_double),C.POINTER(C.c_int),C.POINTER(C.c_double),
                                            C.POINTER(C.c_double),C.POINTER(C.c_double),C.c_int32, C.c_int32]
treeops.angleSpreadExtension.restype = None
treeops.angleSpreadExtension.argtypes = [C.POINTER(C.c_double),C.POINTER(C.c_int),C.c_int32,
                                         C.POINTER(C.c_double),C.POINTER(C.c_double),C.POINTER(C.c_double),
                                            C.POINTER(C.c_double),C.POINTER(C.c_double),C.c_int32]
# treeops.testCheckRotationAngle.restype = C.c_void_p

def testCheck():
    treeops.testCheckRotationAngle()


def np_find_intersect_segments_c(segs):
    numpts = segs.shape[0]

    # SORT LEFT AND RIGHT POINTS
    left_pts = np.zeros((numpts, 2), dtype=np.float64)
    left_inds = np.vstack((np.zeros(numpts, dtype=np.int8), np.arange(numpts, dtype=np.int32))).transpose()
    right_pts = np.zeros((numpts, 2), dtype=np.float64)
    right_inds = np.vstack((np.ones(numpts, dtype=np.int8), np.arange(numpts, dtype=np.int32))).transpose()

    left_pts[:, 0] = np.where(segs[:, 0] > segs[:, 2], segs[:, 2], segs[:, 0])
    left_pts[:, 1] = np.where(segs[:, 0] > segs[:, 2], segs[:, 3], segs[:, 1])
    right_pts[:, 0] = np.where(segs[:, 0] > segs[:, 2], segs[:, 0], segs[:, 2])
    right_pts[:, 1] = np.where(segs[:, 0] > segs[:, 2], segs[:, 1], segs[:, 3])

    # MAKE KEYS:
    ordered_segs = np.hstack((left_pts, right_pts)).copy()
    sl = (ordered_segs[:, 3] - ordered_segs[:, 1]) / (ordered_segs[:, 2] - ordered_segs[:, 0])
    keys = np.lexsort((ordered_segs[:, 1], sl, ordered_segs[:, 2])).astype(np.int32)

    # If we have duplicate lines, call that a fail:
    try:
        assert np.max(keys) == ordered_segs.shape[0] - 1
    except:
        return False
    
    all_pts = np.vstack((left_pts,right_pts))
    all_inds = np.vstack((left_inds,right_inds))
    
    all_view = np.array(np.zeros(2*numpts),dtype=[('x','f8'),('y','f8'),('left','i1'),('ind','i4')])
    all_view['x']=all_pts[:,0]
    all_view['y'] = all_pts[:, 1]
    all_view['left'] = all_inds[:,0]
    all_view['ind'] = all_inds[:,1]
    sort_inds = np.argsort(all_view,order=['x','left'])

    all_inds = all_inds[sort_inds]

    # run the C sweepline algorithm:
    res = sweepline.sweepLineIntersect(ordered_segs.ctypes.data_as(C.POINTER(C.c_double)),
                                       all_inds.ctypes.data_as(C.POINTER(C.c_int)),
                                       keys.ctypes.data_as(C.POINTER(C.c_int)),numpts)
    if res==0:
        return False
    else:
        return True


def np_find_intersect_segments_c_test(segs):
    numpts = segs.shape[0]

    # SORT LEFT AND RIGHT POINTS
    left_pts = np.zeros((numpts, 2), dtype=np.float64)
    left_inds = np.vstack((np.zeros(numpts, dtype=np.int8), np.arange(numpts, dtype=np.int32))).transpose()
    right_pts = np.zeros((numpts, 2), dtype=np.float64)
    right_inds = np.vstack((np.ones(numpts, dtype=np.int8), np.arange(numpts, dtype=np.int32))).transpose()

    left_pts[:, 0] = np.where(segs[:, 0] > segs[:, 2], segs[:, 2], segs[:, 0])
    left_pts[:, 1] = np.where(segs[:, 0] > segs[:, 2], segs[:, 3], segs[:, 1])
    right_pts[:, 0] = np.where(segs[:, 0] > segs[:, 2], segs[:, 0], segs[:, 2])
    right_pts[:, 1] = np.where(segs[:, 0] > segs[:, 2], segs[:, 1], segs[:, 3])

    # MAKE KEYS:
    ordered_segs = np.hstack((left_pts, right_pts)).copy()
    sl = (ordered_segs[:, 3] - ordered_segs[:, 1]) / (ordered_segs[:, 2] - ordered_segs[:, 0])
    keys = np.lexsort((ordered_segs[:, 1], sl, ordered_segs[:, 2])).astype(np.int32)

    # If we have duplicate lines, call that a fail:
    try:
        assert np.max(keys) == ordered_segs.shape[0] - 1
    except:
        return False

    all_pts = np.vstack((left_pts, right_pts))
    all_inds = np.vstack((left_inds, right_inds))

    all_view = np.array(np.zeros(2 * numpts), dtype=[('x', 'f8'), ('y', 'f8'), ('left', 'i1'), ('ind', 'i4')])
    all_view['x'] = all_pts[:, 0]
    all_view['y'] = all_pts[:, 1]
    all_view['left'] = all_inds[:, 0]
    all_view['ind'] = all_inds[:, 1]
    sort_inds = np.argsort(all_view, order=['x', 'left'])

    all_inds = all_inds[sort_inds]

    # dump arrays to files
    # testpath = 'C:/Users/miken/Dropbox/Grad School/Phylogenetics/work/phylostrator-testing'
    testpath = 'C:/Users/miken/Grad School Stuff/Research/Phylogenetics/code/testing_ctypes'
    ordpath = os.path.join(testpath,'test.bin')
    keypath = os.path.join(testpath,'test_keys.bin')
    indpath = os.path.join(testpath,'test_inds.bin')
    num_pts_path = os.path.join(testpath,'num_pts.bin')
    ordered_segs.tofile(ordpath)
    keys.tofile(keypath)
    all_inds.tofile(indpath)
    npts = np.array(ordered_segs.shape[0],dtype=np.int32)
    npts.tofile(num_pts_path)

    # run the C sweepline algorithm:
    res = sweepline.sweepLineIntersect(ordered_segs.ctypes.data_as(C.POINTER(C.c_double)),
                                       all_inds.ctypes.data_as(C.POINTER(C.c_int)),
                                       keys.ctypes.data_as(C.POINTER(C.c_int)), numpts)
    if res == 0:
        return False
    else:
        return True

def centerCladeRot(pts, topo, edge_angles, deflect, lengths, numpts, node):
    treeops.centerCladeRotationally(pts.ctypes.data_as(C.POINTER(C.c_double)),
                                    topo.ctypes.data_as(C.POINTER(C.c_int)),
                                    edge_angles.ctypes.data_as(C.POINTER(C.c_double)),
                                    deflect.ctypes.data_as(C.POINTER(C.c_double)),
                                    lengths.ctypes.data_as(C.POINTER(C.c_double)),
                                    numpts,node)

def angleSpread(pts, topo, numpts, deflect, wedge_sizes, edges, lengths, rightsides, node):
    treeops.angleSpreadExtension(pts.ctypes.data_as(C.POINTER(C.c_double)),
                                 topo.ctypes.data_as(C.POINTER(C.c_int)),
                                 numpts,
                                 deflect.ctypes.data_as(C.POINTER(C.c_double)),
                                 wedge_sizes.ctypes.data_as(C.POINTER(C.c_double)),
                                 edges.ctypes.data_as(C.POINTER(C.c_double)),
                                 lengths.ctypes.data_as(C.POINTER(C.c_double)),
                                 rightsides.ctypes.data_as(C.POINTER(C.c_double)),
                                 node)

treeops.debugWriteSegments.restype = None
treeops.debugWriteSegments.argtypes = [C.POINTER(C.c_double),C.POINTER(C.c_int),C.c_int32]

def dbgWriteSegs(pts,topo,numpts):
    treeops.debugWriteSegments(pts.ctypes.data_as(C.POINTER(C.c_double)),
                                 topo.ctypes.data_as(C.POINTER(C.c_int)),
                                 numpts)