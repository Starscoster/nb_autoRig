from nb_autoRig_v3 import nb_autorig_v3_skeleton as skl_
from nb_autoRig_v3 import nb_autorig_v3_rigging as rig_

import imp
imp.reload(skl_)
imp.reload(rig_)

from PySide2 import QtCore                                  # Import PySide2 ans shiboken2 modules to create ui
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui                              # Import other module used in the code, maya.OpenMayaUI and sys modules
import sys
from maya import cmds

def maya_main_windows() :
    '''
    Return maya main window widget as python object
    '''
    maya_main_window = omui.MQtUtil.mainWindow()
    
    # Return int value if current python version is 3 or upper, otherwise return long
    if sys.version_info.major >= 3 :
        return wrapInstance(int(maya_main_window), QtWidgets.QWidget)
    else :
        return wrapInstance(long(maya_main_window), QtWidgets.QWidget)


class NbAutorigV3UI (QtWidgets.QDialog) :
    '''
    Main UI python class. 
    This class contains all functions to create, laying out and connect widgets of the main Window of the code.
    MayLinkUI inherits the QtWidgets.QDialog class. The Dialog is parented to maya main Dialog
    '''
    def __init__ ( self, parent = None) :
        '''
        Init the UI, create widgets, layout and connections. 
        parent -> parent of the QDialog, if not, value is None.
        '''
        # Initialize QtWidget.QDialog class
        super (NbAutorigV3UI, self).__init__(parent = maya_main_windows())
        
        self.final_init_dict = {}
        self.setMinimumSize(300,300)
        self.setWindowFlags(self.windowFlags()^QtCore.Qt.WindowContextHelpButtonHint)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_widgets (self) :
        
        self.init_skeleton_label = QtWidgets.QLabel("Create Skeleton")
        self.init_hand_fingers_label = QtWidgets.QLabel("Hand fingers (withoutt thumb)")
        self.init_hand_fingers_int = QtWidgets.QSpinBox()
        self.init_hand_fingers_int.setValue(4)
        self.init_thumb_label = QtWidgets.QLabel("Create Thumb")
        self.init_thumb_cb = QtWidgets.QCheckBox()
        self.init_thumb_cb.setChecked(True)
        
        self.init_foot_fingers_label = QtWidgets.QLabel("Foot fingers")
        self.init_foot_fingers_int = QtWidgets.QSpinBox()
        self.init_foot_fingers_int.setValue(5)

        self.facial_rigging_text = QtWidgets.QLabel("Facial Rigging")
        self.facial_rigging_cb = QtWidgets.QCheckBox()
        self.facial_rigging_cb.setChecked(True)
        
        self.init_skeleton_btn = QtWidgets.QPushButton("Create Skeleton")
        self.init_mirror_L_btn = QtWidgets.QPushButton("Mirror R to L")
        self.init_mirror_R_btn = QtWidgets.QPushButton("Mirror L to R")
        
    
        self.rig_name_line = QtWidgets.QLineEdit()
        self.rig_name_line.setPlaceholderText("Rig Name...")

        self.curve_naming = QtWidgets.QLabel("Rigging facial curves")
        self.eyelid_l_up_curve = QtWidgets.QLineEdit()
        self.eyelid_l_up_curve.setPlaceholderText("Eyelid L up...")
        self.eyelid_l_dwn_curve = QtWidgets.QLineEdit()
        self.eyelid_l_dwn_curve.setPlaceholderText("Eyelid L dwn...")
        self.eyelid_r_up_curve = QtWidgets.QLineEdit()
        self.eyelid_r_up_curve.setPlaceholderText("Eyelid R up...")
        self.eyelid_r_dwn_curve = QtWidgets.QLineEdit()
        self.eyelid_r_dwn_curve.setPlaceholderText("Eyelid R dwn...")

        self.upper_lip_curve = QtWidgets.QLineEdit()
        self.upper_lip_curve.setPlaceholderText("Lower lip...")
        self.lower_lip_curve = QtWidgets.QLineEdit()
        self.lower_lip_curve.setPlaceholderText("Upper lip...")

        self.build_rig_btn = QtWidgets.QPushButton("Build Rigging Systems")
        
        
    def create_layouts (self) :
        skeleton_gb = QtWidgets.QGroupBox("Create Skeleton")
        manage_skeleton_gb = QtWidgets.QGroupBox("Edit Skeleton")
        create_rig_gb = QtWidgets.QGroupBox("Create Rigging Systems")
        
        skeleton_layout = QtWidgets.QGridLayout()
        
        skeleton_layout.addWidget(self.init_hand_fingers_label, 0,0)
        skeleton_layout.addWidget(self.init_hand_fingers_int, 0,1)
        skeleton_layout.addWidget(self.init_thumb_label, 0,2)
        skeleton_layout.addWidget(self.init_thumb_cb, 0,3)
        skeleton_layout.addWidget(self.init_foot_fingers_label, 1,0)
        skeleton_layout.addWidget(self.init_foot_fingers_int, 1,1)
        skeleton_layout.addWidget(self.facial_rigging_text, 2,0)
        skeleton_layout.addWidget(self.facial_rigging_cb, 2,1)
        skeleton_layout.addWidget(self.init_skeleton_btn, 3,0,1,4)
        
        skeleton_gb.setLayout(skeleton_layout)
        
        edit_skeleton_layout = QtWidgets.QHBoxLayout()
        edit_skeleton_layout.addWidget(self.init_mirror_L_btn)
        edit_skeleton_layout.addWidget(self.init_mirror_R_btn)
        manage_skeleton_gb.setLayout(edit_skeleton_layout)

        curve_layout = QtWidgets.QGridLayout()
        curve_layout.addWidget(self.eyelid_r_up_curve, 0,0)
        curve_layout.addWidget(self.eyelid_r_dwn_curve, 1,0)
        curve_layout.addWidget(self.eyelid_l_up_curve, 0,1)
        curve_layout.addWidget(self.eyelid_l_dwn_curve, 1,1)
        
        curve_layout.addWidget(self.upper_lip_curve, 2,0,1,2)
        curve_layout.addWidget(self.lower_lip_curve, 3,0,1,2)

        self.rigging_curve_layout = QtWidgets.QVBoxLayout()
        self.rigging_curve_layout.addWidget(self.curve_naming)
        self.rigging_curve_layout.addLayout(curve_layout)

        self.create_rig_layout = QtWidgets.QVBoxLayout()
        self.create_rig_layout.addWidget(self.rig_name_line)
        self.create_rig_layout.addLayout(self.rigging_curve_layout)
        self.create_rig_layout.addWidget(self.build_rig_btn)
        create_rig_gb.setLayout(self.create_rig_layout)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(skeleton_gb)
        main_layout.addWidget(manage_skeleton_gb)
        main_layout.addWidget(create_rig_gb)
        main_layout.addStretch()
        
    def create_connections (self) :
        self.init_skeleton_btn.clicked.connect(self.create_skeleton)
        self.init_mirror_L_btn.clicked.connect(self.miror_R_to_L)
        self.init_mirror_R_btn.clicked.connect(self.miror_L_to_R)
        self.build_rig_btn.clicked.connect(self.create_rig)
        self.facial_rigging_cb.toggled.connect(self.on_facial_cb_toogled)

    def on_facial_cb_toogled (self) :
        print ("in")
        print (self.facial_rigging_cb.isChecked())
        layout_widgets = self.rigging_curve_layout.children()

        for widget in layout_widgets :
            widget.setEnabled(self.facial_rigging_cb.isChecked())
        
    def create_skeleton (self) :
        
        is_thumb = self.init_thumb_cb.isChecked()
        h_finger_number = self.init_hand_fingers_int.value()
        f_finger_number = self.init_foot_fingers_int.value()
        is_facial = self.facial_rigging_cb.isChecked()
        
        skeleton_class = skl_.InitBasicSkeleton(f_finger_number,h_finger_number,is_thumb, is_facial)
        self.final_init_dict = skeleton_class.return_dict()
        
    def miror_L_to_R (self) :
        self.mirror("L")
        
    def miror_R_to_L (self) :
        self.mirror("R")

    def create_rig (self) :
        rig_name = self.rig_name_line.text()
        
        rig_.RigSystem(rig_name, self.final_init_dict)

    def mirror (self, side) :
        '''
        This function takes all locator from a side and  miror position to the other side
        side -> "_L_" or "_R_" (str)
        '''
        mirror_locator_list = []
        if cmds.objExists("rigging_setup_grp") ==True :
            mirrorTransform = cmds.createNode('transform', name= 'locator_grp_TEMP')
            
            for part_ in self.final_init_dict.keys() :
                
                if part_ == "locator_size" or part_ == "setup_group_name" or part_ == "use_facial":
                    continue
                    
                elif self.final_init_dict[part_]["miror_locators"] and '__{}'.format(side) in part_: 
                    for mirror_loc in self.final_init_dict[part_]["miror_locators"] :
                        tempLoc = cmds.spaceLocator(name = mirror_loc + '_TEMP')
                        mirror_locator_list.append ((self.final_init_dict[part_]["miror_locators"][mirror_loc], tempLoc, mirror_loc))
                        cmds.matchTransform(tempLoc, mirror_loc, pos=True, rot=True)
                        cmds.parent(tempLoc, mirrorTransform)
                        
                elif part_ == "head":
                    for locator in self.final_init_dict[part_]["miror_locators"] :
                        if "_{}_".format(side) in locator :
                            tempLoc = cmds.spaceLocator(name = locator + '_TEMP')
                            mirror_locator_list.append ((self.final_init_dict[part_]["miror_locators"][locator], tempLoc, locator))
                            cmds.matchTransform(tempLoc, locator, pos=True, rot=True)
                            cmds.parent(tempLoc, mirrorTransform)
                            

            cmds.setAttr(f'{mirrorTransform}.sx', -1)

            for mirror_loc, temp_locator, loc_to_miror in mirror_locator_list :
                opposite_attr = self.find_opposite_sphere_attribut(loc_to_miror, side)                
                cmds.matchTransform (mirror_loc, temp_locator, pos=True, rot = True)
                
                for attribut in opposite_attr :
                    cmds.setAttr("{}.{}".format(mirror_loc, opposite_attr[attribut]), cmds.getAttr("{}.{}".format(loc_to_miror, attribut)))

            cmds.delete (mirrorTransform)
            
    def find_opposite_sphere_attribut (self, locator, side) :
        
        selAttrs = cmds.listAttr (locator, k=True)
        custom_attr_list = []
        opposite_attr_dict = {}
        
        if side == "L" :
            other_side = "R"
        else :
            other_side = "L"
        
        for each in selAttrs :
            if each in ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY','scaleZ', 'visibility'] : 
                waste = 1
            else:
                custom_attr_list.append(each)
                
        for attr in custom_attr_list :
            opposite_attr_dict[attr] = attr.replace("_{}_".format(side), "_{}_".format(other_side))
            
        return opposite_attr_dict
