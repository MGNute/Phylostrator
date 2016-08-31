__author__ = 'Michael'

import wx, sys
# from controller import Singleton


class ViewerData(object):
    default_pen=None
    default_brush=None
    default_font=None
    objects_other=[]
    objects_bitmap=[]
    objects_node=[]
    objects_edge=[]
    objects_rect=[]
    objects_text=[]

    #viewer properties
    zoom=1
    x_anchor=None
    y_anchor=None


    def __init__(self,parent,*args,**kwargs):
        self.parent=parent

    def Add(self,obj):
        if obj.type=='bitmap':
            self.objects_bitmap.append(obj)
        elif obj.type=='node':
            self.objects_node.append(obj)
        elif obj.type=='edge':
            self.objects_rect.append(obj)
        elif obj.type=='rectangle':
            self.objects_rect.append(obj)
        elif obj.type=='text':
            self.objects_text.append(obj)
        elif obj.type=='other':
            self.objects_other.append(obj)
        else:
            sys.stderr.write("the following object is not properly defined:\n" + str(obj.__dict__))

    def AddOther(self,callback,*args,**kwargs):
        self.objects_other.append(ViewerOther(callback,*args,**kwargs))



class AbstractViewerObject(object):
    # Viewer Coordinate Anchor Positions: None --> Invisible
    x=None
    y=None
    def __init__(self,type):
        self.type=type

class ViewerOther(AbstractViewerObject):
    '''
    This is for an otherwise undefined viewer object. It must include a callback as the first argument of its
    initialization, and the callback must take a wx.DC object as its first argument. Other positional and
    keyword arguments passed to the initializer are then also passed to the callback along with the wx.DC
    object.

    Note: users should not need to initialize this class directly, they should just be able to use the AddOther()
    method in the ViewerData class.
    '''
    def __init__(self,callback,*args,**kwargs):
        AbstractViewerObject.__init__(self,'other')
        self.args=args
        self.kwargs=kwargs
        self.cb=callback

    def draw_me(self,dc):
        self.cb(dc,*self.args,**self.kwargs)


class ViewerBitmap(AbstractViewerObject):
    def __init__(self,path,x,y):
        AbstractViewerObject.__init__(self,'bitmap')
        self.path=path
        self.x=x
        self.y=y

class ViewerExtraRectangle(AbstractViewerObject):
    def __init__(self,x=None,y=None,h=None,w=None,pen=None,brush=None,label=None,value=None):
        AbstractViewerObject.__init__(self,'rectangle')
        self.x=x
        self.y=y
        self.h=h
        self.w=w
        self.pen=pen
        self.brush=brush
        self.label=label
        self.value=value


class ViewerText(AbstractViewerObject):
    def __init__(self,text=None,x=None,y=None,textbox_anchor_pt=(0,0),treespace_anchorpt=None,font=None,angle=0):
        AbstractViewerObject.__init__(self,'text')
        self.text=text
        self.treespace_xy=treespace_anchorpt
        self.textbox_anchor_pt=textbox_anchor_pt
        self.x=x
        self.y=y
        self.font=font
        self.angle=angle

class LeafLabel(ViewerText):
    def __init__(self,parent,viewer_node):
        pass




class ViewerNode(AbstractViewerObject):
    def __init__(self,x=None,drawn=False,color=None,value=None,node_ref=None,theta=0):
        AbstractViewerObject.__init__(self,'node')
        self.ts_x=x #treespace x
        self.show=drawn
        self.color=color
        self.node_annotation=value
        self.node_ref=node_ref
        self.leaf=node_ref.is_leaf()
        self.node_label=node_ref.label
        self.theta=theta
        if self.leaf == True:
            self.leaf_label=node_ref.taxon.label


class ViewerEdge(AbstractViewerObject):
    def __init__(self,head_x=None,tail_x=None,color=None,size=None,label=None,bootstrap=None,showing=True,edge_ref=None):
        AbstractViewerObject.__init__(self,'edge')
        self.head_x = head_x
        self.tail_x = tail_x
        self.size = size
        self.color = color
        self.label = label
        self.bootstrap = bootstrap
        self.showing = showing
        self.edge_ref = edge_ref

class AbstractView():

    def __init__(self):
        self.full_tree_coord_range=None    # in tree-coordinate space
        self.visible_tree_coord_range=None            # in tree-coordinate space

        # note: rotation angle is applied in the tree-coordinate space, not the viewer coordinate space
        self.rotation_angle=None
        self.zoom=None
        pass

    def tree_coords_to_viewer_coords(self, tree_coords):
        '''
        Override this method in the implemented class. Method takes a set of coordinates in the tree space and
        returns a set of coordinates in the viewer space. Should return None if the viewer coordinates are outside
        of the viewable range.
        :param tree_coords:
        :return: viewer_coords, or None if outside the range.
        '''
        pass

    def set_zoom(self,zoom_level):
        '''

        :param zoom_level:
        :return:
        '''
        self.zoom=zoom_level

    def save_to_jpg(self,fpath):
        '''
        Override this method
        :param fpath: path of the target file
        :return:
        '''
        pass




# class WxGUIConnectorView(AbstractView):
#     __metaclass__ = Singleton
#     def __init__(self):
#
#         AbstractView.__init__(self)
#
#
#     def tree_coords_to_viewer_coords(self, tree_coords):
#
#         pass
#
#     # TODO: fill this in with connenctions to the gui_manager
#
