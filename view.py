__author__ = 'Michael'

from controller import Singleton

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




class WxGUIConnectorView(AbstractView):
    __metaclass__ = Singleton
    def __init__(self):

        AbstractView.__init__(self)


    def tree_coords_to_viewer_coords(self, tree_coords):

        pass

    # TODO: fill this in with connenctions to the gui_manager

