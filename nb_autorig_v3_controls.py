import maya.cmds as cmds

from nb_autoRig_v3 import nb_autorig_v3_controls_datas as controls_datas
from nb_autoRig_v3 import nb_autorig_v3_process as utils

class ControlObj () :
    '''
    This class holds control datas and functions to manage it
    '''
    

    def __init__(self, control_name, control_shape, control_color, tuple_datas_factor):
        '''
        Call functions to create the control
        control_name -> control naming (str)
        control_shape -> control shape to apply (str)
        control_color -> control color to display
        '''
        
        self.control_name = control_name
        self.control_shape = control_shape
        self.control_color = control_color
        self.controls_datas = ControlsDatas()
        self.controls_datas.change_tuples_values (tuple_datas_factor)

        self.create_control()
        self.change_control_color()
        self.delete_control_data_class()

    def add_attribut(self, attr_type, attr_name, limite_attr, defaut_value, enum_list) :
        '''
        This function add a new attribut to control. Depends on the attribut type, the added attribut will be different
        '''

        # Set min_attr and max_attr variable
        min_attr, max_attr = limite_attr

        # Set min_max variable. THis variable allows to call differents attributs for cmds.addAttr function
        if min_attr and max_attr :
            min_max =3
        elif min_attr and not max_attr :
            min_max = 1
        elif not min_attr and max_attr :
            min_max = 2
        else :
            min_max = 0

        # Create float or long type attribut
        if str(attr_type) == 'double' or str(attr_type) == 'long' :
            #print each, attr_type_list[counter]
            if min_max==3 :
                cmds.addAttr(self.control_name, ln = attr_name, at=attr_type, hnv=True, hxv=True, min=min_attr, max=max_attr, dv=defaut_value, k=True )
                
            if min_max==2 :
                cmds.addAttr(self.control_name, ln = attr_name, at=attr_type, hnv=True, hxv=True, max=max_attr, dv=defaut_value, k=True )
                
            if min_max==1 :
                cmds.addAttr(self.control_name, ln = attr_name, at=attr_type, hnv=True, hxv=True, min=min_attr, dv=defaut_value, k=True )
                
            if min_max==0 :
                cmds.addAttr(self.control_name, ln = attr_name, at=attr_type, hnv=True, hxv=True,  dv=defaut_value,k=True )

        # Create boolean attribut
        if attr_type == 'bool' : 
            cmds.addAttr(self.control_name, ln=attr_name, at=attr_type, dv=defaut_value, k=True)
        
        # Create enum attribut
        # Enum_list need to be wrote : 'Green:Blue'
        if attr_type == 'enum' :
            cmds.addAttr (self.control_name, ln=attr_name, at=attr_type, en=enum_list, k=True)

        # Create separator attribut
        if attr_type == 'separator' :

            cmds.addAttr(self.control_name, at='enum', ln=attr_name, en=('-----------'), k=True)
            cmds.setAttr (self.control_name+'.'+attr_name, e=True, l=False)

        # Create matrix attribut

    def create_control (self) :
        '''
        Create control shape based on self.control_shape variable
        Return created curve name
        '''

        #exception for curve
        if self.control_shape == 'Circle':
            crv = cmds.circle(d=3, r=self.controls_datas.cv_tuples[self.control_shape][0][0], nr=[0,1,0],name = self.control_name, ch=False)[0]
        else:
            crv = cmds.curve(d=1, p=self.controls_datas.cv_tuples[self.control_shape], name = self.control_name)  

        if cmds.objExists ('curveShape1') == True:
            cmds.rename ('curveShape1', f'{self.control_name}Shape')

        return crv

    def change_control_color (self) :
        '''
        This function change color of conrol shapes
        color -> Color to apply to shapes
        '''
        shape_list = cmds.listRelatives(self.control_name, s=True)

        for shape in shape_list:
            override = cmds.getAttr('%s.overrideEnabled'%(shape))
            if override == 0:
                cmds.setAttr('%s.overrideEnabled'%(shape), 1)

            display = cmds.getAttr('%s.overrideDisplayType'%(shape))
            if display != 0:
                cmds.setAttr('%s.overrideDisplayType'%(shape), 0)

            cmds.setAttr('%s.overrideColor'%(shape), self.controls_datas.control_colors[self.control_color])

    def delete_control_data_class (self) :
        '''
        Delete control datas from variable and RAM
        '''
        del self.controls_datas


class ControlsDatas(controls_datas.ControlBaseDatas) :

    def __init__ (self) :
        '''
        This class herits from controls_datas.ControlBaseDatas class
        '''
        super (ControlsDatas, self).__init__()

    def change_tuples_values (self, factor) :
        '''
        This function change values from current class tuples
        '''
        if type(factor) == str :
            factor = utils.get_object_size(factor)

        for shape_ in self.cv_tuples :
            for point_ in self.cv_tuples[shape_] :
                x, y, z = point_

                new_x = x*factor
                new_y = y*factor
                new_z = z*factor

                self.cv_tuples[shape_][self.cv_tuples[shape_].index(point_)] = (new_x, new_y, new_z)
