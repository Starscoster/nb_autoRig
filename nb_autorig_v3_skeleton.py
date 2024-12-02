"""
This file contains all functions, class, process to create a basic skeleton setup thet th user must used
to place rig. 

The number of fingers for hands and toes can be changed. Also, the hand thumb can be removed. 
The skeleton has the same size no matter if the scene unit is in cm or m. 
Once the skeleton's created, the user must move locators to place rigs. Joints are point and aimed constrainted to it.
Bounding box are used to get mesh part dimensuions to adapt controls size to it as much as possible
"""
from nb_autoRig_v3 import nb_autorig_v3_datas as datas
from maya import cmds

class InitBasicSkeleton (datas.InitDatas) :

    #################################################################################################################
    #                                            INIT FUNCTION
    #################################################################################################################

    def __init__ (self, toes_number, fingers_number, create_thumb, is_facial) :
        '''
        Initialize class will complete datas.InitDatas class with UI settings
        toes_number -> number of toes for rigging (int)
        fingers_number -> number of fingers for rigging (int)
        create_thumb -> if rig create a thumb for the hands or not (boll)
        '''
        super (InitBasicSkeleton, self).__init__()

        # Start datas
        toe_L_minimum = datas.minimum_toes_L_setup
        toe_L_maximum = datas.maximum_toes_L_setup
        toe_R_minimum = datas.minimum_toes_R_setup
        toe_R_maximum = datas.maximum_toes_R_setup

        hand_L_minimum = datas.minimum_hands_L_setup
        hand_L_maximum = datas.maximum_hands_L_setup
        hand_R_minimum = datas.minimum_hands_R_setup
        hand_R_maximum = datas.maximum_hands_R_setup

        # If toes number is different from one, complete toes dict
        if toes_number != 1 :
            self.get_values_in_between_toe (toe_L_minimum, toe_L_maximum, toes_number, 'L')
            self.get_values_in_between_toe (toe_R_minimum, toe_R_maximum, toes_number, 'R')
            use_multiple_toe = True
        else :
            use_multiple_toe = False

        # If toes number is different from four, complete hand dict
        if fingers_number != 4 :
            self.get_values_in_between_finger (hand_L_minimum, hand_L_maximum, fingers_number, 'L', create_thumb)
            self.get_values_in_between_finger (hand_R_minimum, hand_R_maximum, fingers_number, 'R', create_thumb)
            use_custom_hand = True
        else :
            use_custom_hand = False

        # Set up skeleton_datas dict for rigging.
        self.skeleton_datas = self.set_final_dict(use_custom_hand, use_multiple_toe, is_facial)
        self.create_base_skeleton()

        cmds.select(d=True)

    #################################################################################################################
    #                                  Manage rigging setup dictionary functions
    #################################################################################################################

    def get_values_in_between_toe (self, min_values, max_values, number, side) :
        '''
        This function complete datas.InitDatas toe dic with number
        min_values -> list of minimum translate range ([float, float, float])
        max_values -> list of maximum translate range ([float, float, float])
        number -> number of toes (int)
        side -> side of created toe dic (str)
        '''

        # Get datas variable
        toes_naming = datas.toes_naming
        foot_naming = datas.foot_naming
        foot_toe = "{}_{}".format(foot_naming, toes_naming)

        # Add dic in class toes dic
        if side == 'L' :
            dict_to_add = self.toes_L_setup_datas
            suffix = datas.LEFT_naming
        else :
            dict_to_add = self.toes_R_setup_datas
            suffix = datas.RIGHT_naming

        # If number is 5, then create a biped foot toe naming
        if number == 5 :
            biped_foot_naming = datas.biped_hand_foot_naming
            name_list = ["{}_{}_{}".format(foot_naming, biped_foot_naming[0], side),
                        "{}_{}_{}".format(foot_naming, biped_foot_naming[1], side),
                        "{}_{}_{}".format(foot_naming, biped_foot_naming[2], side),
                        "{}_{}_{}".format(foot_naming, biped_foot_naming[3], side),
                        "{}_{}_{}".format(foot_naming, biped_foot_naming[4], side),
                        ]
                           
            name_tip_list = ["{}_tip".format(name_list[0]),
                            "{}_tip".format(name_list[1]),
                            "{}_tip".format(name_list[2]),
                            "{}_tip".format(name_list[3]),
                            "{}_tip".format(name_list[4]),
                            ]
            
            # Set position in dic in between mon range and max values
            for i in range(0, 5) :

                ratio = i/(number-1)
                value = self.get_distance(min_values, max_values, ratio)
                tip_transform = [value[0], value[1], value[2]+10]

                dict_to_add[name_list[i]] = {  'position' : tuple(value), 
                                            'name' : "{}_{}_{}".format(foot_naming, biped_foot_naming[i], suffix),
                                            'joint_to_parent' : None,
                                            'do_not_aim' : False,
                                            'locator_to_parent' : ['self','ball_{}'.format(suffix)],
                                            'miror_target' : True,
                                            'bouding_sphere' : {name_list[i] : (0,0,0)}}
                dict_to_add[name_tip_list[i]] = {'position' : tuple(tip_transform), 
                                            'name' : "{}_{}_{}_tip".format(foot_naming, biped_foot_naming[i], suffix),
                                            'joint_to_parent' : ['self', name_list[i]],
                                            'do_not_aim' : True,
                                            'locator_to_parent' : ['self',name_list[i]],
                                            'miror_target' : True,
                                            'bouding_sphere' : {}}

        # Else, create a procedural naming
        else :
            # Set position in dic in between mon range and max values
            for i in range(0, number) :

                ratio = i/(number-1)

                value = self.get_distance(min_values, max_values, ratio)
                tip_transform = [value[0], value[1], value[2]+10]

                toe_naming = "{}_{}_{}".format(foot_toe, str(i+1), side)
                toe_tip_naming = "{}_tip".format(toe_naming)
                
                dict_to_add[toe_naming] = {'position' : tuple(value), 
                                            'name' : "{}_{}_{}".format(foot_toe, str(i+1), suffix),
                                            'joint_to_parent' : None,
                                            'do_not_aim' : False,
                                            'locator_to_parent' : ['self','ball_{}'.format(side)],
                                            'miror_target' : True,
                                            'bouding_sphere' : {toe_naming : (0,0,0)}}
                dict_to_add[toe_tip_naming] = {'position' : tuple(tip_transform), 
                                            'name' : "{}_{}_{}_tip".format(foot_toe, str(i+1), suffix),
                                            'joint_to_parent' : ['self', toe_naming],
                                            'do_not_aim' : True,
                                            'locator_to_parent' : ['self', toe_naming],
                                            'miror_target' : True,
                                            'bouding_sphere' : {}}
        
        # Add dict to according self variable
        if side == 'L' :
            self.toes_L_setup_datas = dict_to_add
        else :
            self.toes_R_setup_datas = dict_to_add

    def get_values_in_between_finger (self, min_values, max_values, finger_number, side, create_thumb) :
        '''
        This function complete datas.InitDatas hand dic
        min_values -> list of minimum translate range ([float, float, float])
        max_values -> list of maximum translate range ([float, float, float])
        finger_number -> number of fingers (without thumb) (int)
        side -> side of created toe dic (str)
        create_thumb -> add thumb dic to hand dic (bool)
        '''
        # Add dic in class toes dic
        if side == 'L' :
            dict_to_add = self.hand_L_custom_setup_datas
            suffix = datas.LEFT_naming
        else :
            dict_to_add = self.hand_R_custom_setup_datas
            suffix = datas.RIGHT_naming

        # If create_thumb, add thumb dic to hand dic
        if create_thumb :
            dict_to_add[f'meta_thumb_{side}'] = {'position' : (68.369,140,5.884),
                                                'name' : 'meta_thumb_{}'.format(suffix),
                                                'joint_to_parent' : None,
                                                'do_not_aim' : False,
                                                'locator_to_parent' : ['arm_{}'.format(side),-1],
                                                'miror_target' : True,
                                                'bouding_sphere' : {"meta_thumb_{}".format(side) : (0,0,0)}} 
            dict_to_add[f'thumb_01_{side}'] = {'position' : (68.369,140,10.707),
                                                'name' : 'thumb_01_{}'.format(suffix),
                                                'joint_to_parent' : ['self',"meta_thumb_{}".format(side)],
                                                'do_not_aim' : False,
                                                'locator_to_parent' : ['self',"meta_thumb_{}".format(side)],
                                                'miror_target' : True,
                                                'bouding_sphere' : {"thumb_01_{}".format(side) : (0,0,0)}}
            dict_to_add[f'thumb_02_{side}'] =  {'position' : (68.369,140,15.397), 
                                                'name' : 'thumb_02_{}'.format(suffix),
                                                'joint_to_parent' : ['self',"thumb_01_{}".format(side)],
                                                'do_not_aim' : False,
                                                'locator_to_parent' : ['self',"thumb_01_{}".format(side)],
                                                'miror_target' : True,
                                                'bouding_sphere' : {"thumb_02_{}".format(side) : (0,0,0)}}
            dict_to_add[f'thumb_tip_{side}'] = {'position' : (68.369,140,20.01),  
                                                'name' : 'thumb_tip_{}'.format(suffix),
                                                'joint_to_parent' : ['self',"thumb_02_{}".format(side)],
                                                'do_not_aim' : True,
                                                'locator_to_parent' : ['self',"thumb_02_{}".format(side)],
                                                'miror_target' : True,
                                                'bouding_sphere' : {}}
            
        # Create fingers loop
        for i in range(0, finger_number) :

            ratio = i/(finger_number-1)
            # Get positions of all bones for current finger
            metaValue = self.get_distance(min_values[0], max_values[0], ratio)
            jnt01Value = self.get_distance(min_values[1], max_values[1], ratio)
            jnt02Value = self.get_distance(min_values[2], max_values[2], ratio)
            jnt03Value = self.get_distance(min_values[3], max_values[3], ratio)
            jnt04Value = self.get_distance(min_values[4], max_values[4], ratio)

            dict_to_add['meta_finger_{}_0{}'.format(side, i+1)] = {'position' : tuple(metaValue),
                                                                    'name' : 'meta_finger_{}_0{}'.format(suffix, i+1),
                                                                    'joint_to_parent' : None,
                                                                    'do_not_aim' : False,
                                                                    'locator_to_parent' : ['arm_{}'.format(side),-1],
                                                                    'miror_target' : True,
                                                                    'bouding_sphere' : {'meta_finger_{}_0{}'.format(suffix, i+1) : (0,0,0)}}
            dict_to_add['finger_{}_0{}_01'.format(side, i+1)] = {'position' : tuple(jnt01Value), 
                                                                    'name' : 'finger_{}_0{}_01'.format(suffix, i+1),
                                                                    'joint_to_parent' : ['self','meta_finger_{}_0{}'.format(side, i+1)],
                                                                    'do_not_aim' : False,
                                                                    'locator_to_parent' : ['self','meta_finger_{}_0{}'.format(side, i+1)],
                                                                    'miror_target' : True,
                                                                    'bouding_sphere' : {'finger_{}_0{}_01'.format(suffix, i+1) : (0,0,0)}}
            dict_to_add['finger_{}_0{}_02'.format(side, i+1)] = {'position' : tuple(jnt02Value), 
                                                                    'name' : 'finger_{}_0{}_02'.format(suffix, i+1),
                                                                    'joint_to_parent' : ['self','finger_{}_0{}_01'.format(side, i+1)],
                                                                    'do_not_aim' : False,
                                                                    'locator_to_parent' : ['self','finger_{}_0{}_01'.format(side, i+1)],
                                                                    'miror_target' : True,
                                                                    'bouding_sphere' : {'finger_{}_0{}_02'.format(suffix, i+1) : (0,0,0)}}
            dict_to_add['finger_{}_0{}_03'.format(side, i+1)] = {'position' : tuple(jnt03Value), 
                                                                    'name' : 'finger_{}_0{}_03'.format(suffix, i+1),
                                                                    'joint_to_parent' : ['self','finger_{}_0{}_02'.format(side, i+1)],
                                                                    'do_not_aim' : False,
                                                                    'locator_to_parent' : ['self','finger_{}_0{}_02'.format(side, i+1)],
                                                                    'miror_target' : True,
                                                                    'bouding_sphere' : {'finger_{}_0{}_03'.format(suffix, i+1) : (0,0,0)}}
            dict_to_add['finger_{}_0{}_tip'.format(side, i+1)] = {'position' : tuple(jnt04Value), 
                                                                    'name' : 'finger_{}_0{}_tip'.format(suffix, i+1),
                                                                    'joint_to_parent' : ['self','finger_{}_0{}_03'.format(side, i+1)],
                                                                    'do_not_aim' : True,
                                                                    'locator_to_parent' : ['self','finger_{}_0{}_03'.format(side, i+1)],
                                                                    'miror_target' : True,
                                                                    'bouding_sphere' : {}}
        
        # Add dict to according self variable
        if side == 'L' :
            self.hand_L_custom_setup_datas = dict_to_add
        else :
            self.hand_R_custom_setup_datas = dict_to_add
        
    def check_replace_value (self) :
        '''
        Get current maya scene unit value. If it's 'm', call self.replace_values function 
        '''
        sceneUnit = get_scene_unit()
        if sceneUnit == 'm' :
            self.replace_values()
    
    def replace_values (self) :
        '''
        Remplace position values of each component dic and size value to match maya's current scene unit
        '''
        for dict_ in self.armL_setup_datas, self.armR_setup_datas, self.head_setup_datas, self.legL_setup_datas, self.legR_setup_datas, self.neck_setup_datas, self.singleToeL_setup_datas, self.singleToeR_setup_datas, self.spine_setup_datas  :
            for bone in dict_ :
                dict_[bone]['position'] = self.get_new_values(dict_[bone]['position'])
                
        for dict_ in self.handL_setup_datas, self.handR_setup_datas, self.toesL_setup_datas, self.toesR_setup_datas :
            for finger in dict_ :
                for bone in dict_[finger] :
                    newValues = self.get_new_values(dict_[finger][bone]['position'])
                    dict_[finger][bone]['position'] = newValues
                        
        self.size_setup_datas = .05

    def get_new_values(self, tuple_value) :
        '''
        Divide by 100 tuple values to match maya scene current unit
        tuple_value -> position value (tuple)
        Return new position tuple value
        '''

        oldX, oldY, oldZ = tuple_value

        newX = oldX*0.01
        newY = oldY*0.01
        newZ = oldZ*0.01

        round(newX, 3)
        round(newX, 3)
        round(newX, 3)

        return (newX, newY, newZ)
    
    def set_final_dict (self, use_custom_hand, use_multiple_toe, is_facial) :
        '''
        Set up final dict for rigging setup process
        use_custom_hand -> use hand_<side>_custom_setup_datas or hand_<side>_setup_datas (bool)
        use_multiple_toe -> use toes_<side>_setup_datas or single_toe_<side>_setup_datas (boll)
        Return this dict (dict)
        '''

        final_dict = {}

        final_dict['spine'] = self.spine_setup_datas
        final_dict['neck'] = self.neck_setup_datas
        final_dict['arm_L'] = self.arm_L_setup_datas
        final_dict['arm_R'] = self.arm_R_setup_datas
        final_dict['leg_L'] = self.leg_L_setup_datas
        final_dict['leg_R'] = self.leg_R_setup_datas
        final_dict['reverse_L'] = self.rev_L_setup_datas
        final_dict['reverse_R'] = self.rev_R_setup_datas
        final_dict['scene_size'] = get_scene_unit()

        if use_custom_hand :
            final_dict['hand_L'] = self.hand_L_custom_setup_datas
            final_dict['hand_R'] = self.hand_R_custom_setup_datas
        else :
            final_dict['hand_L'] = self.hand_L_setup_datas
            final_dict['hand_R'] = self.hand_R_setup_datas

        if use_multiple_toe :
            final_dict['foot_L'] = self.toes_L_setup_datas
            final_dict['foot_R'] = self.toes_R_setup_datas
        else :
            final_dict['foot_L'] = self.single_toe_L_setup_datas
            final_dict['foot_R'] = self.single_toe_R_setup_datas

        if is_facial :
            final_dict['head'] = self.facial_rigging_datas
            final_dict['use_facial'] = True
        else :
            final_dict['head'] = self.head_setup_datas
            final_dict['use_facial'] = False

        return final_dict

    #################################################################################################################
    #                                           Utils functions
    #################################################################################################################
    
    def get_distance (self, point_a, point_b, factor) :
        '''
        This function calcul distance between two points in 3D space
        point_a -> fisrt point (tuple)
        point_b -> second point (tuple)
        factor -> When we want a specific place between point a and b, use this argument to precise wher, in percent, you want 
            the point (float)
        Return a point in 3D space (tuple)
        '''
        pointVec = [0,0,0]
        pointVec[0] = (point_b[0] - point_a[0])*factor
        pointVec[1] = (point_b[1] - point_a[1])*factor
        pointVec[2] = (point_b[2] - point_a[2])*factor

        finalT = [0,0,0]
        finalT[0] = round(point_a[0] + pointVec[0],5)
        finalT[1] = round(point_a[1] + pointVec[1],5)
        finalT[2] = round(point_a[2] + pointVec[2],5)

        return finalT
    
    #little message patern
    def init_messages (self, part):
        '''
        Setup a simple message to show the setup processing
        part -> custom message to display (str)
        Return the message (str)
        '''
        msg_init = 'Setting up ' + part + ' structure'
        msg_init_len = len(msg_init) + 6
        message  = '\n' + '+'*msg_init_len +'\n' + '++ ' + msg_init + ' ++\n' + '+'*msg_init_len +'\n'

        return message
     
    #################################################################################################################
    #                                         Create Rigging skeleton
    #################################################################################################################

    def create_base_skeleton (self) :
        '''
        This function will call necessary functions to create basic rigging skeleton
        '''
        self.initial_skeleton_dict = {}
        circle_ = cmds.circle (name = 'rigSetup_master_ctrl', r =50, nry=1, nrz=0, nrx=0, ch=False)[0]
        cmds.addAttr(circle_, ln = "boundingBoxVisibility", at = "bool", k=True, h=False)

        self.initial_skeleton_dict ['spine'] = self.create_rigging_setup_module ('spine', self.skeleton_datas['spine'], False, False, circle_)
        self.initial_skeleton_dict ['neck'] = self.create_rigging_setup_module ('neck', self.skeleton_datas['neck'], False, False, circle_)
        self.initial_skeleton_dict ['head'] = self.create_rigging_setup_module ('head', self.skeleton_datas['head'], False, False, circle_)
        self.initial_skeleton_dict ['arm__L'] = self.create_rigging_setup_module ('arm_L', self.skeleton_datas['arm_L'], True, False, circle_)
        self.initial_skeleton_dict ['arm__R'] = self.create_rigging_setup_module ('arm_R', self.skeleton_datas['arm_R'], True, False, circle_)
        self.initial_skeleton_dict ['leg__L'] = self.create_rigging_setup_module ('leg_L', self.skeleton_datas['leg_L'], False, 'L', circle_)
        self.initial_skeleton_dict ['leg__R'] = self.create_rigging_setup_module ('leg_R', self.skeleton_datas['leg_R'], False, 'R', circle_)
        self.initial_skeleton_dict ['reverse_foot__L'] = self.create_rigging_setup_module ('reverse_foot_L', self.skeleton_datas['reverse_L'], False, False, circle_)
        self.initial_skeleton_dict ['reverse_foot__R'] = self.create_rigging_setup_module ('reverse_foot_R', self.skeleton_datas['reverse_R'], False, False, circle_)
        self.initial_skeleton_dict ['hand__L'] = self.create_rigging_setup_module ('hand_L', self.skeleton_datas['hand_L'], True, False, circle_)
        self.initial_skeleton_dict ['hand__R'] = self.create_rigging_setup_module ('hand_R', self.skeleton_datas['hand_R'], True, False, circle_)
        self.initial_skeleton_dict ['foot__L'] = self.create_rigging_setup_module ('foot_L', self.skeleton_datas['foot_L'], False, False, circle_)
        self.initial_skeleton_dict ['foot__R'] = self.create_rigging_setup_module ('foot_R', self.skeleton_datas['foot_R'], False, False, circle_)
        self.initial_skeleton_dict ['locator_size'] = self.size_setup_datas
        self.initial_skeleton_dict ["setup_group_name"] = "rigging_setup_grp"
        self.initial_skeleton_dict ["use_facial"] = self.skeleton_datas['use_facial']
        
        # Organize outliner
        global_group = cmds.createNode("transform", name = self.initial_skeleton_dict["setup_group_name"])
        
        cmds.parent (circle_, global_group)

        for each in self.initial_skeleton_dict :
            if each == "locator_size" or each == "setup_group_name" or each == "use_facial" :
                continue
            cmds.parent (self.initial_skeleton_dict[each]['group'], circle_)

        print ('\n******** Rig setup done ********\n')
        print (self.initial_skeleton_dict)

    # main creation function
    def create_rigging_setup_module (self, module, rigging_module_settings, is_arm, is_leg, vis_control): 
        '''
        This function create bones and locator network for a rigging module. Locator are pointConstraint to one bones and that bones is aim constraint to another.
        module -> current module name (str)
        rigging_module_settings -> module's dictionary with naming, position and is_last attribut for bones, locator and aimConstraint settings (dict)
        is_arm -> If current module is an arm or not (bool)
        is_leg -> If current module is a leg or not (bool)
        Return created module as dict with locators, bones and bounding boxes
        '''
        
        print (self.init_messages(module))

        jnt_list =[]
        loc_list = []
        buffer_list = []
        bounding_box_list = []
        locator_mirror_dic = {}

        index = 0
        
        for each in rigging_module_settings :
            # Create locator, move it to preset position.
            locator = cmds.spaceLocator (name = "{}_{}".format(rigging_module_settings[each]['name'], datas.PLACE_LOCATOR_naming))[0]
            cmds.setAttr ('{}.t'.format(locator), *rigging_module_settings[each]['position'])
            cmds.setAttr ('{}.s'.format(locator), *(self.size_setup_datas, self.size_setup_datas, self.size_setup_datas))
            cmds.select(d=True)

            # Create bones and move it to locator. Point constraint it
            bone = cmds.joint (name = "{}_{}".format(rigging_module_settings[each]['name'], datas.JOINT_naming))
            
            cmds.matchTransform (bone, locator, pos=True)
            cmds.pointConstraint (locator, bone)

            # Update jnt list
            jnt_list.append(bone)

            parent_bone_settings = rigging_module_settings[each]['joint_to_parent']
            parent_locator_settings = rigging_module_settings[each]['locator_to_parent']
            
            if parent_bone_settings :
                if parent_bone_settings[0] != 'self' :
                    cmds.parent (bone, self.initial_skeleton_dict[parent_bone_settings[0]]['joints'][parent_bone_settings[1]])
                else :
                    cmds.parent (bone, "{}_{}".format(rigging_module_settings[parent_bone_settings[1]]['name'], datas.JOINT_naming))

            if parent_locator_settings :
                if parent_locator_settings[0] != 'self' :
                    buffer = cmds.createNode("transform", name = locator.replace(datas.PLACE_LOCATOR_naming, "buffer_{}".format(datas.GROUP_naming)))
                    cmds.matchTransform(buffer, locator)
                    cmds.parent(locator, buffer)
                    cmds.parentConstraint (self.initial_skeleton_dict[parent_locator_settings[0]]['locators'][parent_locator_settings[1]], buffer, mo=True)
                    buffer_list.append(buffer)
                else :
                    cmds.parent (locator, "{}_{}".format(rigging_module_settings[parent_locator_settings[1]]['name'], datas.PLACE_LOCATOR_naming))

            if rigging_module_settings[each]['bouding_sphere']:
                for bouding_box in rigging_module_settings[each]['bouding_sphere'] :
                    new_sphere = cmds.polySphere(name = "{}_{}".format(bouding_box, datas.BOUNDING_BOX_naming), radius = self.size_setup_datas*.5, ch=False)[0]
                    cmds.connectAttr ("{}.boundingBoxVisibility".format(vis_control), "{}.visibility".format(new_sphere))
                    cmds.parent (new_sphere, bone)
                    cmds.setAttr("{}.rotate".format(new_sphere), *(0,0,0))
                    cmds.setAttr("{}.translate".format(new_sphere), *rigging_module_settings[each]['bouding_sphere'][bouding_box])

                    cmds.setAttr("{}.translate".format(new_sphere), lock = True)
                    cmds.setAttr("{}.rotate".format(new_sphere), lock = True)

                    cmds.addAttr(locator, ln = "{}_scale".format(bouding_box), at="double", hnv=True, min=.1, dv=10, k=True )
                    mult_node = cmds.createNode("multiplyDivide", name = "{}_scale_ratio".format(bouding_box))
                    cmds.connectAttr("{}.{}_scale".format(locator, bouding_box), "{}.input1X".format(mult_node))
                    cmds.connectAttr("{}.{}_scale".format(locator, bouding_box), "{}.input1Y".format(mult_node))
                    cmds.connectAttr("{}.{}_scale".format(locator, bouding_box), "{}.input1Z".format(mult_node))

                    cmds.setAttr ("{}.input2".format(mult_node), *(.1,.1,.1))
                    cmds.connectAttr("{}.output".format(mult_node), "{}.scale".format(new_sphere))

                    cmds.setAttr('{}.overrideEnabled'.format(new_sphere), 1)
                    cmds.setAttr('{}.overrideDisplayType'.format(new_sphere), 1)
                    
                    bounding_box_list.append(new_sphere)

            if rigging_module_settings[each]['miror_target'] :
                if '_L' in each :
                    locator_mirror_dic[locator] = locator.replace("_L_", "_R_")
                elif '_R' in each :
                    locator_mirror_dic[locator] = locator.replace("_R_", "_L_")

            index += 1

            loc_list.append(locator)

        # Aim constraints joint to next joint in list
        aim_index = 0
        for part in rigging_module_settings:
            
            # If bone needs a specific orientation (hands, foot), build a aim system with and hidden bone
            if rigging_module_settings[part]['do_not_aim'] =="parent" :
                aim_joint = cmds.joint(name = "{}_aim".format(jnt_list[aim_index]))
                cmds.matchTransform(aim_joint, jnt_list[aim_index])
                cmds.parent (aim_joint, jnt_list[aim_index])
                cmds.setAttr ("{}.ty".format(aim_joint), 1)
                cmds.parent(aim_joint, loc_list[aim_index])

                if is_arm == True :
                    cmds.aimConstraint (aim_joint, jnt_list[aim_index], aim =(0,1,0), u=(1,0,0), wut='objectrotation', wuo=loc_list[aim_index], wu = (0,1,0) )

                # If current rigging module is leg, object up vector is different, if left, it's x, if right it's -x
                else :
                    if is_leg == 'R' :
                        cmds.aimConstraint (aim_joint, jnt_list[aim_index], aim =(0,1,0), u=(1,0,0), wut='objectrotation', wuo=loc_list[aim_index], wu = (-1,0,0) )
                    else :
                        cmds.aimConstraint (aim_joint, jnt_list[aim_index], aim =(0,1,0), u=(1,0,0), wut='objectrotation', wuo=loc_list[aim_index], wu = (1,0,0) )
                
                cmds.setAttr("{}.visibility".format(aim_joint), False)
            
            # Pass last bones   
            elif rigging_module_settings[part]['do_not_aim']:    
                aim_index += 1
                continue

            else :
                # If current rigging module is arm, object up vector is z
                if is_arm == True :
                    cmds.aimConstraint (loc_list[aim_index+1], jnt_list[aim_index], aim =(0,1,0), u=(1,0,0), wut='objectrotation', wuo=loc_list[aim_index], wu = (0,1,0) )

                # If current rigging module is leg, object up vector is different, if left, it's x, if right it's -x
                elif is_leg != False :
                    if is_leg == 'R' :
                        cmds.aimConstraint (loc_list[aim_index+1], jnt_list[aim_index], aim =(0,1,0), u=(1,0,0), wut='objectrotation', wuo=loc_list[aim_index], wu = (-1,0,0) )
                    else :
                        cmds.aimConstraint (loc_list[aim_index+1], jnt_list[aim_index], aim =(0,1,0), u=(1,0,0), wut='objectrotation', wuo=loc_list[aim_index], wu = (1,0,0) )

                # Else, object up vector is x
                else :
                    cmds.aimConstraint (loc_list[aim_index+1], jnt_list[aim_index], aim =(0,1,0), u=(1,0,0), wut='objectrotation', wuo=loc_list[aim_index], wu = (1,0,0) )
        
            aim_index += 1

        # Group locators and bones in one module
        place_locator_grp = cmds.createNode ('transform', name = "{}_{}_{}".format(module, datas.PLACE_LOCATOR_naming, datas.GROUP_naming))
        module_group = cmds.createNode ("transform", name = "{}_{}".format(module, datas.GROUP_naming))

        for locator in loc_list :
            if cmds.listRelatives (locator, p=True, typ = 'transform') == None and cmds.listRelatives(locator, p=True) not in buffer_list :
                cmds.parent (locator, place_locator_grp)

        if buffer_list :    
            cmds.parent(buffer_list, place_locator_grp)

        for joint in jnt_list :
            if cmds.listRelatives (joint, p=True, typ = 'transform') == None :
                cmds.parent (joint, module_group)

        cmds.parent (place_locator_grp, module_group)

        return {"group" : module_group, "joints" : jnt_list, "locators": loc_list, "miror_locators": locator_mirror_dic, "bounding_box" : bounding_box_list}

    def return_dict (self) :
        '''
        This functions return self.skeleton_datas
        '''
        return self.initial_skeleton_dict

def get_scene_unit ():
    '''
    Get scene curent unit to adapt rig size
    '''
    unit = cmds.currentUnit(q=True, linear=True)
    return unit