__author__ = 'Michael'
import tree_manipulator as trman
import view_classes

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if not cls.instance:
            # Not created or has been Destroyed
            obj = super(Singleton, cls).__call__(*args, **kw)
            cls.instance = obj
        return cls.instance

class Controller():
    __metaclass__ = Singleton
    def __init__(self):
        self.apm=trman.AnnotatedPhylogramModel()
        self.current_uniques=[]
        self.value_picker_ctrl=None

        #Drawing Properties:
        self.circle_size=None

    def get_relevent_data_from_model(self):
        print "getting relevant data from model"
        self.max_data_dims=self.apm.rp.get_max_dims()
        print "getting leaf coordinate data copy"
        self.leaf_coords=self.apm.rp.leaf_node_coords
        print "getting the annotation fields"
        self.annotation_fields=self.apm.annotation.annotation_fields

    def set_ValuePickerCtrl_reference(self,vpc_pointer):
        self.value_picker_ctrl=vpc_pointer

    def set_ImageFrame_referenece(self,img_frame):
        self.image_frame=img_frame

    def update_cirlces_by_annotation(self):
        self.apm.checked=[]
        for i in self.value_picker_ctrl.value_pickers:
            if i.m_checkBox1.IsChecked()==True:
                self.apm.checked.append((i.value,i.clr))

        for i in self.leaf_coords:
            self.leaf_coords[i]['drawn']=False
            self.leaf_coords[i]['color']=None
            # i['annotation']

        all_taxa=self.apm.annotation.get_EFDIDs_grouped_by(self.apm.annotation_level)
        for i in self.apm.checked:
            tx=all_taxa[i[0]]

            for j in tx:
                self.leaf_coords[j]['drawn']=True
                self.leaf_coords[j]['color']=i[1]
                self.leaf_coords[j]['annotation']=i[0]

    def get_circle_sets_by_color(self):
        '''
        this is the final helper function for the circle drawing that gets a bunch of (color, list of coordinates) pairs
        :return:
        '''
        cols={}
        for i in self.leaf_coords:
            a=self.leaf_coords[i]
            if a['drawn']==True:
                if a['color'] in cols.keys():
                    cols[a['color']].append(a['x'])
                else:
                    cols[a['color']]=[a['x']]
        return cols

    def import_tree(self,path):
        self.apm.initialize_tree(path)
        self.apm.rp.get_max_dims()

    def import_annotation(self,ann_path):
        self.apm.initialize_annotation(ann_path)

    def trigger_refresh(self):
        self.image_frame.img_panel.Refresh()

