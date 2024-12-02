import maya.cmds as cmds

from nb_autoRig_v3 import nb_autorig_v3_controls as ctrl 
from nb_autoRig_v3 import nb_autorig_v3_get_pivots  as get_pv
from nb_autoRig_v3 import nb_autorig_v3_process as utils
from nb_autoRig_v3 import nb_autorig_v3_matrix_constraints as mat_const
from nb_autoRig_v3 import nb_autorig_v3_datas as datas
from nb_autoRig_v3 import nb_autorig_v3_facial as facial

import imp
#reload modules
imp.reload(ctrl)
imp.reload(get_pv)
imp.reload(utils)
imp.reload(mat_const)

class RigSystem () :

    def __init__ (self, rig_name, skeletons_datas) :
        '''
        This class will hold rig current name and all functions created elements
        rig_name -> character name (str)
        skeletons_datas -> initial setup skeleton (dict)
        '''
        # Class variable 
        self.rig_name = rig_name
        self.initial_datas = self.sort_skeleton_datas(skeletons_datas)
        self.joint_radius = self.initial_datas["locator_size"] *.5
        self.binded_bones = []
        
        # Module creation
        master_output = self.build_main_rig(self.initial_datas['spine'])
        spine_output = self.build_spine_rig(master_output, self.initial_datas['spine'])
        arm_L_output = self.build_biped_part_rig(master_output, spine_output, self.initial_datas['arm__L'], "arm_L", 5, "Cyan", "arm")
        arm_R_output = self.build_biped_part_rig(master_output, spine_output, self.initial_datas['arm__R'], "arm_R", 5, "Red", "arm")
        leg_L_output = self.build_biped_part_rig(master_output, spine_output, self.initial_datas['leg__L'], "leg_L", 5, "Cyan", "leg")
        leg_R_output = self.build_biped_part_rig(master_output, spine_output, self.initial_datas['leg__R'], "leg_R", 5, "Red", "leg")

        hand_L_output = self.build_hand_rig (master_output, arm_L_output, "L", self.initial_datas['hand__L'], "Cyan")
        hand_R_output = self.build_hand_rig (master_output, arm_R_output, "R", self.initial_datas['hand__R'], "Red")

        neck_output = self.build_neck_rig (master_output, spine_output, self.initial_datas['neck'])
        print (skeletons_datas)
        if skeletons_datas["use_facial"] :
            head_output = facial.create_facial_rig(self.rig_name, self.initial_datas['head'], master_output, spine_output, neck_output)
        else :
            head_output = self.build_head_rig (master_output, spine_output, neck_output, self.initial_datas['head'])

        foot_L_output = self.build_foot_rigging (master_output, spine_output, leg_L_output, "L", self.initial_datas['foot__L'], self.initial_datas['reverse_foot__L'])
        foot_R_output = self.build_foot_rigging (master_output, spine_output, leg_R_output, "R", self.initial_datas['foot__R'], self.initial_datas['reverse_foot__R'])

        # Delete skeleton group and organize rigging modules in outliner
        cmds.delete(self.initial_datas["setup_group_name"])
        rigging_group = cmds.createNode("transform", name = "{}_RIG_grp".format(self.rig_name))

        for module in [master_output, spine_output, arm_L_output, arm_R_output, hand_L_output, hand_R_output, neck_output, head_output, foot_L_output, foot_R_output, leg_L_output, leg_R_output] :
            cmds.parent(module["module"], rigging_group)

        cmds.select(d=True)

    def sort_skeleton_datas (self, skeleton_datas) :
        '''
        This function takes dict that has been used for setup the skeleton and keep only joints and bounding box datas
        skeleton_datas -> start dict (dict)
        Return initial_datas -> dict with only joints and bounding_box datas (dict)
        '''
        initial_datas = {}

        for part_ in skeleton_datas :
            if part_ != "locator_size" and part_ != "setup_group_name" and part_ != "use_facial":
                new_dict = {}
                new_dict['joints'] = skeleton_datas[part_]["joints"]
                new_dict['bounding_box'] = skeleton_datas[part_]["bounding_box"]

                initial_datas[part_] = new_dict
            else :
                initial_datas[part_] = skeleton_datas[part_]

        return initial_datas
    
################################################################################################################
#                                         Build Rig functions
################################################################################################################

    def build_main_rig (self, spine_dict) :
        '''
        Build main rigging system : master, root and cog controls
        spine_dict : scpine dictionnary (dict)
        Return created elements in dict
        '''
        # Get head translate to xform vis control
        cog_jnt = spine_dict["joints"][1]
        cog_bounding_box = spine_dict["bounding_box"][1]
        cog_translate = cmds.xform(cog_jnt, q=1,ws=1,t=1)

        rig_size = utils.get_rig_maximum_size([self.initial_datas['leg__R']['joints'][-1], self.initial_datas['leg__L']['joints'][-1]])
        cog_size = utils.get_object_size(cog_bounding_box)

        # Create modules groups
        input_grp, output_grp, public_grp, private_grp, module_grp = utils.init_module_sequence(self.rig_name + '_MASTER')

        # Build master controls
        master = ctrl.ControlObj ("{}_MASTER_{}".format(self.rig_name, datas.CONTROL_naming), 'Circle', 'Grey', rig_size)
        root = ctrl.ControlObj ("{}_root_{}".format(self.rig_name, datas.CONTROL_naming), 'Four Arrows', 'Yellow', rig_size*.9)
        cog = ctrl.ControlObj ("{}_COG_{}".format(self.rig_name, datas.CONTROL_naming), 'Box', 'Yellow', cog_size)
        cmds.matchTransform(cog.control_name, cog_jnt)
        vis = ctrl.ControlObj ("{}_vis_{}".format(self.rig_name, datas.CONTROL_naming), 'Diamond', 'Blue', rig_size*.025)
        cmds.setAttr(f'{vis.control_name}.ty', cog_translate[1]*2)
        vis.add_attribut('separator', 'controls', ('',''), 0, '')
        vis.add_attribut('bool', 'controlVis', ('',''), 1, '')

        # Connect vis attr to master controls
        for control in [master.control_name, root.control_name, cog.control_name] :
            cmds.connectAttr (f'{vis.control_name}.controlVis', f'{control}.visibility')

        #  Set parent controls relations
        mat_const.parent(master.control_name, root.control_name, False, True, True, True, True, master.control_name.replace('_{}'.format(datas.CONTROL_naming),'Root'))
        mat_const.parent(root.control_name, cog.control_name, True, True, True, True, True, root.control_name.replace('_{}'.format(datas.CONTROL_naming),'Cog'))
        mat_const.parent(cog.control_name, vis.control_name, True, True, True, True, True, vis.control_name.replace('_{}'.format(datas.CONTROL_naming),'Vis'))

        # Parent in hierarchy public group
        cmds.parent (cog.control_name, root.control_name, vis.control_name, master.control_name, public_grp)

        # Const output group
        mat_const.parent(cog.control_name, output_grp, False, True, True, True, False, output_grp.replace('_grp','_output'))
        master_output_attr = utils.add_attr_modules (output_grp, [master.control_name, root.control_name, cog.control_name])

        return {"outputs" : output_grp, 
                "output_attr" :  master_output_attr , 
                "controls" : {"master" : master, "root" : root, "cog" : cog, "settings" : vis},
                "module" : module_grp}
    
    def build_spine_rig (self, master_dict, spine_dict): 
        '''
        Build spine rigging system and connect it to master rigging
        master_dict -> created master dict (dict)
        spine_dict -> initial bones dict (dict)
        Return created element in dict
        '''
        twist_joint_number = 7

        # Create module groups and parent master output to input group
        input_group, output_group, public_group, private_group, module_group = utils.init_module_sequence(self.rig_name + '_spine') 
        utils.connect_modules(master_dict["outputs"], input_group)
        
        top_output_group = output_group.replace('_output_', '_topOutput_')
        cmds.rename(output_group, top_output_group)
        bottom_output_group = cmds.createNode('transform', name = f'{self.rig_name}_spine_botOutput_grp')
        cmds.parent (bottom_output_group, module_group)
        cmds.setAttr (f'{bottom_output_group}.useOutlinerColor', True)
        cmds.setAttr (f'{bottom_output_group}.outlinerColor', 0,1,1)

        # Initial spines bones
        spine_base_joints = spine_dict["joints"]
        bounding_boxs = spine_dict["bounding_box"]

        # Create base skl List
        spine_driver_joints = []

        # Create spine driver joint
        for each in spine_base_joints :
            cmds.select(d=True)
            newBase = cmds.joint(name = each.replace ('_{}'.format(datas.JOINT_naming),'_driver_{}'.format(datas.JOINT_naming)), rad = self.joint_radius)
            cmds.matchTransform(newBase, each, pos=True, rot=True)
            spine_driver_joints.append(newBase)

        # Parent joint driver chain to itself
        for x in range (len(spine_driver_joints)-1) :
            cmds.parent (spine_driver_joints[x+1], spine_driver_joints[x])

        # Create control joint list and fk - ik controls list
        drived_bones = [spine_driver_joints[0], spine_driver_joints[2], spine_driver_joints[3]]
        fk_control_list = []
        ik_control_list = []

        settings = ctrl.ControlObj ("{}_spine_settings_{}".format(self.rig_name, datas.CONTROL_naming), 'Diamond', 'Blue', 1)
        settings.add_attribut('bool', 'ikVisibility',  ('',''), True, [''])
        cmds.matchTransform(settings.control_name, spine_driver_joints[1])
        cmds.setAttr ("{}.translateX".format(settings.control_name), cmds.getAttr ("{}.translateX".format(settings.control_name)) + ((utils.get_object_size(bounding_boxs[1])*2)/2))
        cmds.connectAttr (f'{master_dict["controls"]["settings"].control_name}.controlVis', f'{settings.control_name}.visibility')
        mat_const.parent (input_group, settings.control_name, True, True, True, True, True, settings.control_name.replace('_{}'.format(datas.CONTROL_naming), '_const'))

        # Create ik visibility mult node
        ik_visibility_mult = cmds.createNode('multDoubleLinear', name =  "{}_spine_ik_visibility_mult".format(self.rig_name))
        cmds.connectAttr (f'{master_dict["controls"]["settings"].control_name}.controlVis', f'{ik_visibility_mult}.i1')
        cmds.connectAttr (f'{settings.control_name}.ikVisibility', f'{ik_visibility_mult}.i2')

        # Create ik fk controls
        control_index = 1
        for each in drived_bones :

            fk_ctrl = ctrl.ControlObj ("{}_spine_fk_0{}_{}".format(self.rig_name, (control_index), datas.CONTROL_naming), 'Square', 'Yellow', utils.get_object_size(bounding_boxs[spine_driver_joints.index(each)])+.25)
            ik_ctrl = ctrl.ControlObj ("{}_spine_ik_0{}_{}".format(self.rig_name, control_index, datas.CONTROL_naming), 'Circle', 'Red', utils.get_object_size(bounding_boxs[spine_driver_joints.index(each)])+.2)

            cmds.parent (ik_ctrl.control_name, fk_ctrl.control_name)
            cmds.matchTransform(fk_ctrl.control_name, each)

            mat_const.parent(ik_ctrl.control_name, each, False, True, True, True, False,  each.replace('_jnt','_driver_const'))

            cmds.connectAttr (f'{ik_visibility_mult}.o', f'{ik_ctrl.control_name}.visibility')
            cmds.connectAttr (f'{master_dict["controls"]["settings"].control_name}.controlVis', f'{fk_ctrl.control_name}.visibility')

            fk_control_list.append (fk_ctrl)
            ik_control_list.append (ik_ctrl) 

            control_index+=1

        # Parent fk controls together
        cmds.parent (fk_control_list[1].control_name, fk_control_list[0].control_name)
        cmds.parent (fk_control_list[2].control_name, fk_control_list[1].control_name)

        # Create cvs list for curve
        cvs_list = []

        # Get control joint translate for curve cv
        for bones in spine_driver_joints :
            translate = cmds.xform (bones, q=True, t=True, ws=True)
            tuple(translate)
            cvs_list.append(translate)

        # Create twist curve
        spine_curve = cmds.curve(d=3, p=cvs_list, name = f'{self.rig_name}_spine_bend_curve')
        cmds.rename ('curveShape1', f'{spine_curve}Shape')

        # Skin curve
        spine_curve_skin = f'{self.rig_name}_spine_curve_skin'
        cmds.skinCluster(spine_driver_joints, spine_curve, mi = 1, name = spine_curve_skin, wd = 0, ih = True, sm = 0, tsb=True)
        if cmds.objExists("bindPose1") :
            cmds.rename("bindPose1", spine_curve_skin.replace("_skin", "_bindPose"))

        # Create twist
        _, spline_ik, spline_eff, spline_twist_joint = utils.create_twist (f'{self.rig_name}_spine', spine_driver_joints[0], spine_driver_joints[4], spine_driver_joints[0], twist_joint_number, self.joint_radius/2, False, spine_curve, "{}.scaleX".format(input_group), 'X', (1,0,0))
        for each in spline_twist_joint :
            self.binded_bones.append(each)

        #kill inverse scale
        utils.kill_inverse_scale (spine_driver_joints[0])

        #clean contorlers and parent
        mat_const.opm(fk_control_list[1].control_name)
        mat_const.opm(fk_control_list[2].control_name)
        mat_const.parent (input_group, fk_control_list[0].control_name, True, True, True, True, True, fk_control_list[0].control_name.replace('_{}'.format({datas.CONTROL_naming}), '_input_constraint'))
        cmds.setAttr (f'{fk_control_list[0].control_name}.t', *(0,0,0))
        cmds.setAttr (f'{fk_control_list[0].control_name}.r', *(0,0,0))


        cmds.parent (spine_curve, spine_driver_joints[0], spline_ik, private_group)
        cmds.parent (settings.control_name, fk_control_list[0].control_name, public_group)

        mat_const.parent (spine_driver_joints[-1], top_output_group, False, True, True, True, False, top_output_group.replace('_{}'.format({datas.GROUP_naming}), '_output_const'))
        mat_const.parent (spine_driver_joints[0], bottom_output_group, False, True, True, True, False, bottom_output_group.replace('_{}'.format({datas.GROUP_naming}), '_output_const'))

        bottom_output_attr = utils.add_attr_modules (bottom_output_group, [ik_control_list[0].control_name, fk_control_list[0].control_name])
        top_output_attr = utils.add_attr_modules (top_output_group, [ik_control_list[-1].control_name, fk_control_list[-1].control_name])

        return {"outputs" : [bottom_output_group, top_output_group], 
                "output_attr" : [bottom_output_attr, top_output_attr] , 
                "controls" : {"fk_controls" : fk_control_list, "ik_controls" : ik_control_list, "settings" : settings},
                "module" : module_group}

    def build_biped_part_rig (self, master_part, spine_part, part_init_dict, part_name, twist_joint_number, color, mode) :
        '''
        Build biped arm and leg skeleton
        twist_joint_number : number of twist jnt in mebmer and upper member
        color : color of controls
        visctrl : global visibility control
        size : global size control
        mode : is arm or leg
        Return created element in dict
        '''
        start_bones = part_init_dict["joints"]
        part_naming = "{}_{}".format(self.rig_name, part_name)

        # Set values based on mode variable
        if mode == 'arm' :
            first_FK_parent_space = 'Clavicle'
            last_ik_pole_vector_perent_space = 'Wrist'
            settings_separator_attribut = 'armAttr'
            ik_auxiliare_soulder_name = '_shoulderAux'
            arm_twist = 'arm_twist'
            fore_arm_name = self.rig_name.replace('arm', 'foreArm')
            fore_arm_twist_axe = 'Z'
            parent_ik= True
            
            parent_spaces = {master_part["output_attr"][0] : [True, True, True, 'Master'], 
                             master_part["output_attr"][1]  : [True, True, True, 'Root'], 
                             master_part["output_attr"][2] : [True, True, True, 'COG'], 
                             spine_part["output_attr"][1][1] : [True, True, False, 'TopSpine'], 
                             spine_part["output_attr"][0][1] : [False, True, False, 'BotSpine']}

        else :
            first_FK_parent_space = 'Hip'
            last_ik_pole_vector_perent_space = 'Ankle'
            settings_separator_attribut = 'legAttr'
            ik_auxiliare_soulder_name = '_hipAux'
            arm_twist = 'legTwist'
            fore_arm_name = self.rig_name.replace('leg', 'foreLeg')
            fore_arm_twist_axe = 'X'
            parent_ik=False

            parent_spaces = {master_part["output_attr"][0] : [True, True, True, 'Master'], 
                             master_part["output_attr"][1]  : [True, True, True, 'Root'], 
                             master_part["output_attr"][2] : [True, True, True, 'COG'], 
                             spine_part["output_attr"][0][1] : [False, True, False, 'BotSpine']}

        # Create output groups dic for parent space and input group attr creation
        input_group_attribut_list = []
        for output_group in parent_spaces :
            input_group_attribut_list.append(output_group)

        # Init message and module creation
        input_group, output_group, public_group, private_group, module_group = utils.init_module_sequence(part_naming)
        if mode == 'arm' :
            utils.connect_modules(spine_part["outputs"][1], input_group)
        else :
            utils.connect_modules(spine_part["outputs"][0], input_group)

        # Bones lists
        bones = []
        fk_bones = []
        ik_bones =[]

        past_first = False
        # Ik fk bones creation
        for each in start_bones :   
            newname = part_naming +'_' + each

            cmds.select(d=True)
            jnt = cmds.joint (name=newname, rad = self.joint_radius)
            cmds.matchTransform(jnt, each, pos=True, rot=True)
            
            bones.append (newname)

            if not past_first :
                past_first = True
            else :

                fkName = newname.replace('_{}'.format(datas.JOINT_naming),'_FK_{}'.format(datas.JOINT_naming))
                cmds.select(d=True)
                cmds.joint (name = fkName, rad = self.joint_radius)
                cmds.matchTransform(fkName, each, pos=True, rot=True)

                fk_bones.append (fkName)

                ikName = newname.replace('_{}'.format(datas.JOINT_naming),'_IK_{}'.format(datas.JOINT_naming))
                cmds.select(d=True)
                cmds.joint (name = ikName, rad = self.joint_radius)
                cmds.matchTransform(ikName, each, pos=True, rot=True)

                ik_bones.append (ikName)

        # Create ik aux joint
        cmds.select(d=True)
        ik_shoulder_joint_aux = cmds.joint (name = ik_bones[2].replace('_IK_{}'.format(datas.JOINT_naming), '_IK_aux_{}'.format(datas.JOINT_naming)), rad = self.joint_radius)
        cmds.matchTransform(ik_shoulder_joint_aux, ik_bones[2], pos=True, rot=True)

        # Create matrix attrs 
        input_group_attribut_list.append(bones[0])
        attribut_list = utils.add_attr_modules (input_group, input_group_attribut_list)

        # Create dictionaries for parent spaces
        fk_parent_space_dict = {}
        ik_parent_space_dict = {}
        ik_pv_parent_space_dict = {}
        parent_index = 0

        for each in parent_spaces :
            if parent_spaces[each][0] == True :
                fk_parent_space_dict[parent_spaces[each][3]] = attribut_list[parent_index]
            if parent_spaces[each][1] == True :
                ik_parent_space_dict[parent_spaces[each][3]] = attribut_list[parent_index]
            if parent_spaces[each][2] == True :
                ik_pv_parent_space_dict[parent_spaces[each][3]] = attribut_list[parent_index]
            parent_index += 1

        fk_parent_space_dict [first_FK_parent_space] = f'{input_group}.{bones[0]}'
        ik_parent_space_dict [first_FK_parent_space] = f'{input_group}.{bones[0]}'

        # Re-parent bones
        for i in range (1,4) :

            cmds.parent (bones[i], bones[i-1], a=True)

        for i in range(1,3):

            cmds.parent (fk_bones[i], fk_bones[i-1])
            cmds.parent (ik_bones[i], ik_bones[i-1])

        # Parent ik aux to wrisdt ik bones, and update ik_bones list
        cmds.parent (ik_shoulder_joint_aux,ik_bones[2])
        ik_bones.append(ik_bones[2])
        ik_bones[2] = ik_shoulder_joint_aux
        
        # Set main skeleton list
        main_arm_skeleton = [bones[1], bones[2], bones[3]]

        # Create fk controls
        fk_controls = []

        bounding_boxs = part_init_dict["bounding_box"]

        for each in fk_bones :
            newfk = ctrl.ControlObj ("{}_fk_{}".format(each, datas.CONTROL_naming), 
                                    'Circle', 
                                    color, 
                                    utils.get_object_size(bounding_boxs[fk_bones.index(each)+ 1]) + .5)
            cmds.matchTransform(newfk.control_name, each)
            fk_controls.append(newfk)
            
        for i in range (0,2) :
            cmds.parent (fk_controls[i+1].control_name, fk_controls[i].control_name)
            mat_const.opm(fk_controls[i+1].control_name)

        # Create clavicle control
        clavicle_control = ctrl.ControlObj ("{}_{}".format(bones[0].replace('_{}'.format(datas.JOINT_naming),''), datas.CONTROL_naming),
                                        'Box', 
                                        color, 
                                        utils.get_object_size(bounding_boxs[0]))
        cmds.matchTransform(clavicle_control.control_name, bones[0])
        mat_const.parent(clavicle_control.control_name, bones[0], False, True, True, True, False, clavicle_control.control_name.replace('_{}'.format(datas.CONTROL_naming),'_bone_main'))
        mat_const.parent(input_group, clavicle_control.control_name, True, True, True, True, True, clavicle_control.control_name.replace('_{}'.format(datas.CONTROL_naming),'_input_constraint'))
        cmds.setAttr(f'{clavicle_control.control_name}.t', *(0,0,0))
        cmds.setAttr(f'{clavicle_control.control_name}.r', *(0,0,0))
        cmds.connectAttr ('{}.controlVis'.format(master_part["controls"]["settings"].control_name), f'{clavicle_control.control_name}.visibility')
        

        # Create settings control
        arm_settings_control = ctrl.ControlObj ("{}_settings_{}".format(part_naming, datas.CONTROL_naming),
                                        'Diamond', 
                                        'Blue', 
                                        1)
        arm_settings_control.add_attribut('separator', settings_separator_attribut, ('',''), 0, '')
        arm_settings_control.add_attribut('enum', 'ikFkSwitch', ('',''), 0, 'FK:IK')
        cmds.matchTransform(arm_settings_control.control_name, main_arm_skeleton[-1])
        cmds.connectAttr ('{}.controlVis'.format(master_part["controls"]["settings"].control_name), f'{arm_settings_control.control_name}.visibility')

        # Create ik control
        ik_control = ctrl.ControlObj ("{}_ik_{}".format(part_naming, datas.CONTROL_naming),
                                        'Box', 
                                        color, 
                                        utils.get_object_size(bounding_boxs[-1]) + .5)
        
        cmds.matchTransform(ik_control.control_name, bones[3])
        ik_pv_parent_space_dict[last_ik_pole_vector_perent_space] = f'{ik_control.control_name}.wm[0]'
        attribut_list = utils.add_attr_modules (input_group, [ik_control.control_name])
        # Build ik fk
        ik_node, ik_pv_node , visibility_mult_node = utils.ik_fk_switch (fk_bones, ik_bones, main_arm_skeleton , fk_controls, ik_control.control_name, arm_settings_control.control_name, part_naming, master_part["controls"]["settings"].control_name, parent_ik)

        # Create ik pv control
        ik_pv_control = ctrl.ControlObj("{}_ik_pv_{}".format(part_naming, datas.CONTROL_naming),
                                      'Pyramid', 
                                      color, 
                                      1)
        cmds.matchTransform(ik_pv_control.control_name, ik_pv_node)
        cmds.connectAttr (f'{visibility_mult_node}.o', f'{ik_pv_control.control_name}.visibility')

        # Create visual ik pv curve
        pv_curve_bone_list = [bones[2], ik_pv_node]
        elbow_position = cmds.xform(bones[2], q=True, t=True, ws=True)
        ik_pv_control_position= cmds.xform(ik_pv_node, q=True, t=True, ws=True)
        ik_pv_curve = cmds.curve(d=1, p=[elbow_position, ik_pv_control_position], name = part_naming + '_ikPv_curve')  
        if cmds.objExists ('curveShape1') == True:
            cmds.rename ('curveShape1', f'{ik_pv_curve}Shape') 
        cmds.setAttr (f"{ik_pv_curve}.overrideEnabled", 1)
        cmds.setAttr (f"{ik_pv_curve}.overrideDisplayType", 2)
        pv_curve_skin_name = part_naming + '_ikPv_skin'
        pv_curve_skin = cmds.skinCluster(pv_curve_bone_list, ik_pv_curve, mi = 1, name = pv_curve_skin_name, wd = 0, ih = True, sm = 0, tsb=True)[0]
        if cmds.objExists("bindPose1") :
            cmds.rename("bindPose1", pv_curve_skin_name.replace("_skin", "_bindPose"))
        for x in range (0, 2) :
            cmds.skinPercent( pv_curve_skin, f'{ik_pv_curve}.cv[{x}]', transformValue=(pv_curve_bone_list[x], 1))
        cmds.connectAttr (f'{visibility_mult_node}.o', f'{ik_pv_curve}.visibility')

        # Link ik controls and settings
        mat_const.parent(ik_pv_control.control_name, ik_pv_node, False, True, False, False, False, ik_pv_node.replace('_pv_{}'.format(datas.LOCATOR_naming),'_ikPv_main'))
        mat_const.parent(ik_control.control_name, ik_shoulder_joint_aux, False, False, True, False, False, ik_shoulder_joint_aux.replace('_{}'.format(datas.JOINT_naming),'_rot'))
        mat_const.parent(main_arm_skeleton[2], arm_settings_control.control_name, True, True, True, True, False, arm_settings_control.control_name.replace('_{}'.format(datas.CONTROL_naming),'_main'))

        arm_settings_control.add_attribut('bool', 'strech', ("",""), 1, '')
        multTrechNodeList, strechGroups = utils.strech (ik_bones[0], bones[0], ik_control.control_name, [f'{ik_bones[1]}.ty', f'{ik_bones[3]}.ty'], "{}.strech".format(arm_settings_control.control_name), part_naming)

        for each in multTrechNodeList:
            cmds.connectAttr ("{}.scaleX".format(input_group), f'{each}')

        # Make shoulder aux joints
        shoulder_aux_list, shoulder_ik, shoulder_pv = utils.shoulder_aux (part_naming + ik_auxiliare_soulder_name, bones)
        shoulder_pv_dist = utils.get_relative_distance (bones[1], bones[2], .5)

        # Check if create an arm or leg, and apply the correspondant settings
        if mode == 'arm' :
            yDist = (cmds.getAttr(f'{shoulder_pv[0]}.ty')**2)**.5+ ((shoulder_pv_dist[0])**2)**0.5
            
            cmds.setAttr(f'{shoulder_pv[0]}.ty', yDist) 

        else :
            yDist = (cmds.getAttr(f'{shoulder_pv[0]}.tx')**2)**.5+ ((shoulder_pv_dist[1])**2)**0.5
        
            if mode == 'legL' :
                cmds.setAttr(f'{shoulder_pv[0]}.tx', yDist) 
            else :
                cmds.setAttr(f'{shoulder_pv[0]}.tx', -yDist) 
    
        cmds.parent (shoulder_pv, bones[0])

        # Make twits
        arm_curve, arm_spline_ik, arm_effector, arm_twist_joint = utils.create_twist ("{}_arm_twist".format(part_naming), shoulder_aux_list[0], bones[2], bones[1], twist_joint_number, self.joint_radius, True, '', "{}.scaleX".format(input_group), 'X', [1,0,0])
        forearm_curve, forearm_spline_ik, forearm_effector, forearm_twist_joint = utils.create_twist ("{}_forearm_twist".format(part_naming), bones[2], bones[3], bones[2], twist_joint_number, self.joint_radius, True, '', "{}.scaleX".format(input_group), fore_arm_twist_axe, [0,0,1])
        
        # Update global binded bones list
        self.binded_bones.append (bones[0]) 
        for each in arm_twist_joint, forearm_twist_joint :
            self.binded_bones.append (each)  

        cmds.select(d=True)
        half_elbow = cmds.joint(name = bones[2].replace('_{}'.format(datas.JOINT_naming), '_hRot_{}'.format(datas.JOINT_naming)))
        cmds.matchTransform(half_elbow, arm_twist_joint[-1])
        cmds.parent (half_elbow, arm_twist_joint[-1])

        out_half_decompose_node = cmds.createNode('decomposeMatrix', name = half_elbow + '_blend_outDecMat')

        mult_nodes_list = []

        for i in [arm_twist_joint[-1], forearm_twist_joint[0]] :
            mult_node = cmds.createNode("multMatrix", name = i + '_half_const_multMat')
            cmds.connectAttr ("{}.worldMatrix[0]".format(i), "{}.matrixIn[0]".format(mult_node))
            cmds.connectAttr ("{}.parentInverseMatrix[0]".format(half_elbow), "{}.matrixIn[1]".format(mult_node))
            mult_nodes_list.append(mult_node)

        blend_mat_node = cmds.createNode("blendMatrix", name = half_elbow + '_switch_blendMat')
        cmds.connectAttr ("{}.matrixSum".format(mult_nodes_list[0]), "{}.inputMatrix".format(blend_mat_node))
        cmds.connectAttr ("{}.matrixSum".format(mult_nodes_list[1]), "{}.target[0].targetMatrix".format(blend_mat_node))

        cmds.setAttr ("{}.target[0].weight".format(blend_mat_node), .5)

        cmds.connectAttr("{}.outputMatrix".format(blend_mat_node), "{}.inputMatrix".format(out_half_decompose_node))

        cmds.connectAttr (f'{out_half_decompose_node}.outputRotate', f'{half_elbow}.r')
        cmds.connectAttr (f'{out_half_decompose_node}.outputScale', f'{half_elbow}.s')

        cmds.setAttr ("{}.jointOrient".format(half_elbow), *(0,0,0))

        self.binded_bones.append (half_elbow)

        # Make bend
        bend_offset_group_list, midbend_offset_group_list, bendJoint = utils.bend ("{}_arm_bend".format(part_naming), [arm_curve, forearm_curve], [bones[1], bones[2], bones[3]], color, master_part["controls"]["settings"], arm_settings_control, self.joint_radius, bounding_boxs)
        # Parent ik and fk bones chain to clavicle
        cmds.parent (fk_bones[0], ik_bones[0], bones[0])
        cmds.setAttr("{}.jointOrient".format(fk_bones[0]), *(0,0,0))
        
        # Supp connection between joint scale an child joint inverse scale
        utils.kill_inverse_scale (bones[0])

        # Create parent spaces
        utils.parent_space (ik_control, ik_parent_space_dict, f'{part_naming}_ik', ik_control, 'ik')
        utils.parent_space (ik_pv_control , ik_pv_parent_space_dict, f'{part_naming}_ikPv', ik_pv_control, 'ik')
        utils.parent_space (fk_controls[0] , fk_parent_space_dict, f'{part_naming}_fk', fk_controls[0], 'fk')

        # Order nodes in groups
        fk_controlsGroup = cmds.createNode('transform', name = f'{part_naming}_fk_controls_{datas.GROUP_naming}')
        ik_controlGroup = cmds.createNode('transform', name = f'{part_naming}_ik_controls_{datas.GROUP_naming}')
        bendcontrolGroup = cmds.createNode('transform', name = f'{part_naming}_bendControls_{datas.GROUP_naming}')
        bonesGroup = cmds.createNode('transform', name = f'{part_naming}_bones_{datas.GROUP_naming}')
        arm_twistGroup = cmds.createNode('transform', name = f'{part_naming}_{arm_twist}_{datas.GROUP_naming}')
        forearm_twistGroup = cmds.createNode('transform', name = f'{part_naming}_fore{arm_twist}_{datas.GROUP_naming}')
        ikGroup = cmds.createNode('transform', name = f'{part_naming}_ik_{datas.GROUP_naming}')
        bendGroups = cmds.createNode('transform', name = f'{part_naming}_bend_{datas.GROUP_naming}')

        cmds.parent (fk_controls[0].control_name, fk_controlsGroup)
        cmds.parent (ik_control.control_name, ik_pv_control.control_name, ik_controlGroup)
        cmds.parent (bend_offset_group_list, midbend_offset_group_list.control_name, bendcontrolGroup)

        cmds.parent (bones[0], bonesGroup)
        cmds.parent (ik_node, strechGroups, ik_pv_curve, ik_pv_node, ikGroup)
        cmds.parent (arm_curve, arm_spline_ik, arm_twistGroup)
        cmds.parent (forearm_curve, forearm_spline_ik, forearm_twistGroup)
        cmds.parent (bendJoint, bendGroups)

        cmds.parent (fk_controlsGroup, ik_controlGroup, bendcontrolGroup, clavicle_control.control_name, arm_settings_control.control_name, public_group)
        cmds.parent (bonesGroup, bendGroups, arm_twistGroup, forearm_twistGroup, ikGroup, private_group)

        # Parent output group to last main bone
        mat_const.parent(bones[-1], output_group, False, True, True, True, False, output_group.replace('_grp',''))
        wrist_attribut = utils.add_attr_modules (output_group, [bones[-1]])

        if mode == "leg" :
            cmds.setAttr ("{}.ikFkSwitch".format(arm_settings_control.control_name), 1)

        return {"outputs" : output_group, 
                "output_attr" : wrist_attribut , 
                "controls" : {"fk_controls" : fk_controls, "ik_controls" : [ik_control, ik_pv_control], "settings" : arm_settings_control},
                "module" : module_group,
                "last_bone" : bones[-1],
                "ik_handle" : ik_node,
                "strech_groups" : strechGroups
                }
    
    def build_hand_rig (self, master_dict, arm_part_dict, side, hand_dict, color) :
        '''
        Buil hand rig systems
        master_dict -> master part rigging dict (dict)
        arm_part_dict -> arm part to connect rigging dict (dict)
        side -> "L" or "R" (str)
        hand_dict -> hand start element datas (dict)
        color -> color for controls (str)
        Return created element in dict
        '''
        # Setup start joint and bounding box variable
        start_joint_list = hand_dict["joints"]
        start_bounding_box_list = hand_dict["bounding_box"]
        
        hand_dict = {}

        finger_index = 1
        current_dict = ""
        finger_datas_dict = {}

        bounding_box_index = 0

        # Order hand dict in a most friendly dict to work with
        for x in range(len(start_joint_list)) :
            if "meta" in start_joint_list[x] :
                if current_dict :
                    finger_datas_dict = {}

                if "thumb" in start_joint_list[x] :
                    current_dict = "thumb"
                else :
                    current_dict = "finger_{}".format(finger_index)
                    finger_index += 1
            
            if not "tip" in start_joint_list[x] :
                finger_datas_dict[start_joint_list[x]] = start_bounding_box_list[bounding_box_index]
                bounding_box_index +=1
            else :
                finger_datas_dict[start_joint_list[x]] = ""
                hand_dict[current_dict] = finger_datas_dict

        # Setup naming, module groupes and visibility control variable          
        part_name = "{}_hand_{}".format(self.rig_name, side)
        input_group, output_group, public_group, private_group, module_group = utils.init_module_sequence(part_name)
        utils.connect_modules (arm_part_dict["outputs"], input_group)
        visibility_control = master_dict["controls"]["settings"]

        # Create element list
        control_list = []
        bone_list = []
        buffer_list = []
        meta_list = []
        control_dict = {}

        # Create meta buffer and constraint it to input 
        meta_hands_group = cmds.createNode('transform', name = f'{part_name}_meta_grp')
        mat_const.parent(input_group, meta_hands_group, False, True, True, True, False, f'{part_name}_meta')
        cmds.parent (meta_hands_group, public_group)
        # Connect visibility attribut
        visibility_mult = cmds.createNode ('multDoubleLinear', name = f'{part_name}_vis_mult')
        cmds.connectAttr (f'{visibility_control.control_name}.controlVis', f'{visibility_mult}.i1')

        # Create controls and bones for each finger part
        for finger in hand_dict :
            tempDic = {}

            for hand_joint in hand_dict[finger] :

                # Get control according bounding box
                control_bounding_box = hand_dict[finger][hand_joint]
                cmds.select(d=True)
                bone = cmds.joint (name = "{}_{}".format(part_name, hand_joint), rad = self.joint_radius)
                cmds.matchTransform (bone, hand_joint, pos=True, rot = True)
                self.binded_bones.append(bone)
                bone_list.append(bone)

                # If joint is meta joint, create circle pin control
                if 'meta' in hand_joint :
                    control = ctrl.ControlObj(bone.replace('_{}'.format(datas.JOINT_naming),'_{}'.format(datas.CONTROL_naming)),
                                      'Circle Pin', 
                                      color, 
                                      utils.get_object_size(control_bounding_box) + .1) 
                    cmds.matchTransform(control.control_name, hand_joint)
                    buff = cmds.createNode('transform', name = bone.replace('_{}'.format(datas.JOINT_naming),'_{}'.format(datas.GROUP_naming)))
                    cmds.matchTransform (buff, control.control_name, pos=True, rot = True)
                    cmds.parent (control.control_name, buff)
                    cmds.parent (buff, meta_hands_group)
                    cmds.connectAttr (f'{visibility_mult}.o', f'{control.control_name}.visibility')
                    mat_const.opm(buff)
                    control_list.append(control.control_name)
                    buffer_list.append(buff)
                    meta_list.append(bone)
                    tempDic[hand_joint] = {'control' : control, 'buffer': buff, 'joint' : bone}
                    mat_const.parent(control.control_name, bone, False, True, True, True, False, bone.replace('_{}'.format(datas.JOINT_naming),''))

                    cmds.parent (bone, private_group)

                # If joint is the last of that finger, pass control creation
                elif 'tip' in hand_joint :
                    cmds.parent (bone, bone_list[bone_list.index(bone)-1])

                # If joint isn't the last one of the finger and not meta, create a circle control
                else :
                    control = ctrl.ControlObj (bone.replace('_{}'.format(datas.JOINT_naming),'_{}'.format(datas.CONTROL_naming)),
                                               'Circle',
                                               color,
                                               utils.get_object_size(control_bounding_box) +.2)
                    cmds.matchTransform(control.control_name, hand_joint)
                    control_list.append(control.control_name)
                    buff = cmds.createNode('transform', name = bone.replace('_{}'.format(datas.JOINT_naming),'_{}'.format(datas.GROUP_naming)))
                    cmds.matchTransform (buff, control.control_name, pos=True, rot = True)
                    cmds.parent (control.control_name, buff)
                    buffer_list.append(buff)
                    cmds.parent (buff, control_list[control_list.index(control.control_name)-1])
                    cmds.parent (bone, bone_list[bone_list.index(bone)-1])
                    mat_const.opm(buff)

                    tempDic[hand_joint] = {'control' : control, 'buffer': buff, 'joint' : bone}
                    mat_const.parent(control.control_name, bone, False, True, True, True, False, bone.replace('_{}'.format(datas.JOINT_naming),''))

                    half_bone_finger = utils.half_rotate_joint (bone)

                    self.binded_bones.append(half_bone_finger)

                cmds.setAttr (f'{bone}.jointOrient', *(0,0,0))
            
            # Add created element to control_dict
            control_dict[finger] = tempDic

        # Set up finger extremities variable for hand settings movements (Spread, Slide, Pinch, Fist and Wave)
        if 'thumb' in control_dict.keys() :
            first_finger_dict = list(control_dict.keys())[1]
        else :
            first_finger_dict = list(control_dict.keys())[0]

        last_finger_dict = list(control_dict.keys())[-1]

        # Get distance between extremities fingers and place locators
        meta_little_dist = utils.get_absolute_distance (control_dict[first_finger_dict][[*control_dict[first_finger_dict].keys()][0]]['joint'], control_dict[first_finger_dict][[*control_dict[first_finger_dict].keys()][1]]['joint'], .5)
        meta_index_dist = utils.get_absolute_distance (control_dict[last_finger_dict][[*control_dict[last_finger_dict].keys()][0]]['joint'], control_dict[last_finger_dict][[*control_dict[last_finger_dict].keys()][1]]['joint'], .5)
        meta_little_loc = cmds.spaceLocator(name = 'temp_meta_little_loc')[0]
        meta_index_loc = cmds.spaceLocator(name = 'temp_meta_index_loc')[0]
        cmds.setAttr (f'{meta_little_loc}.t', *meta_little_dist)
        cmds.setAttr (f'{meta_index_loc}.t', *meta_index_dist)

        # Get the distance between the two created locators to get the middle position of the hand
        hand_center_point = utils.get_absolute_distance (meta_index_loc, meta_little_loc, .5)
        temp_settings_loc = cmds.spaceLocator(name = 'temp_settings_loc')[0]
        cmds.setAttr (f'{temp_settings_loc}.t', *hand_center_point)

        # Create settings controls and place it at the center of the hand
        settings =  ctrl.ControlObj ('{}_settings_{}'.format(part_name, datas.CONTROL_naming),
                                               'Box',
                                               color,
                                               1) 
        cmds.matchTransform(settings.control_name, temp_settings_loc, pos=True)
        cmds.matchTransform(settings.control_name, control_dict[first_finger_dict][[*control_dict[first_finger_dict].keys()][0]]['joint'], rot=True)
        mat_const.parent(input_group, settings.control_name, True, True, True, True, False, settings.control_name.replace('{}'.format(datas.CONTROL_naming),'input_const'))

        # Delete locators and parent settings control to public group
        cmds.delete(meta_little_loc, meta_index_loc, temp_settings_loc)
        cmds.parent (settings.control_name, public_group)

        # Create hands attributs
        settings.add_attribut ('bool', 'controlVis', ['',''], 0, '')
        settings.add_attribut ('double', 'spread', [-10,10], 0, '')
        settings.add_attribut ('double', 'slide', ['',''], 0, '')
        settings.add_attribut ('double', 'fist', [0,10], 0, '')
        settings.add_attribut ('double', 'wave', ['',''], 0, '')
        settings.add_attribut ('double', 'pinch', ['',''], 0, '')

        cmds.addAttr(settings.control_name, ln = "fist_finger_01_factor", at = "double", dv=85, h=False)
        cmds.addAttr(settings.control_name, ln = "fist_finger_02_factor", at = "double", dv=85, h=False)
        cmds.addAttr(settings.control_name, ln = "fist_finger_03_factor", at = "double", dv=85, h=False)
        cmds.addAttr(settings.control_name, ln = "fist_thumb_01_factor", at = "double", dv=80, h=False)
        cmds.addAttr(settings.control_name, ln = "fist_thumb_02_factor", at = "double", dv=40, h=False)
        cmds.addAttr(settings.control_name, ln = "fist_thumb_03_factor", at = "double", dv=50, h=False)

        # Connect settings visibilityhand attr to hands controls and master settings visibility controlms to hand settings
        cmds.connectAttr (f'{settings.control_name}.controlVis', f'{visibility_mult}.i2')
        cmds.connectAttr (f'{visibility_control.control_name}.controlVis', f'{settings.control_name}.visibility')

        # Meta spread max variable
        spread_output_max_values = [-5, 5]
        spread_meta_index = 0

        # Spread meta creation
        for meta in [control_dict[first_finger_dict][list(control_dict[first_finger_dict].keys())[0]]['buffer'], control_dict[last_finger_dict][list(control_dict[last_finger_dict].keys())[0]]['buffer']] :

            remap_node = cmds.createNode('remapValue', name = meta.replace('_{}'.format(datas.GROUP_naming), '_spreadOut_remap'))
            cmds.connectAttr (f'{settings.control_name}.spread', f'{remap_node}.i')
            cmds.setAttr (f'{remap_node}.imx', 10)
            cmds.setAttr (f'{remap_node}.imn', 0)
            cmds.setAttr (f'{remap_node}.omx', spread_output_max_values[spread_meta_index])
            cmds.connectAttr (f'{remap_node}.ov',f'{meta}.rx')

            spread_meta_index += 1

        # Spread and slide creation
        for x in range (0, len(control_dict.keys())-1) :
            if 'thumb' in control_dict.keys() :
                buffer = control_dict [list(control_dict.keys())[x+1]][list(control_dict[list(control_dict.keys())[x+1]].keys())[1]]['buffer']
            else :
                buffer = control_dict [list(control_dict.keys())[x]][list(control_dict[list(control_dict.keys())[x]].keys())[1]]['buffer']
            
            # Spread
            remap_node = cmds.createNode('remapValue', name = buffer.replace('_{}'.format(datas.GROUP_naming), '_spreadOut_remap'))
            cmds.connectAttr (f'{settings.control_name}.spread', f'{remap_node}.i')
            cmds.setAttr (f'{remap_node}.imx', -10)
            cmds.setAttr (f'{remap_node}.imn', 10)

            if (len(control_dict.keys())-1) %2 !=0 :
                if x  == (len(control_dict.keys())-2)/2 :
                    cmds.connectAttr (f'{settings.control_name}.slide', f'{buffer}.rx')
                    continue
                
            if x >= (len(control_dict.keys())-1)/2 : 
                cmds.setAttr (f'{remap_node}.omx', -5)
                cmds.setAttr (f'{remap_node}.omn', 5)
            else :
                cmds.setAttr (f'{remap_node}.omx', 5)
                cmds.setAttr (f'{remap_node}.omn', -5)

            # Slide
            add_node = cmds.createNode('addDoubleLinear', name = buffer.replace('_{}'.format(datas.GROUP_naming), '_slide_add'))
            cmds.connectAttr (f'{remap_node}.ov', f'{add_node}.i1')
            cmds.connectAttr (f'{settings.control_name}.slide', f'{add_node}.i2')

            cmds.connectAttr (f'{add_node}.o',f'{buffer}.rx')

        # Fingers fist and wave

        first_finger_first_remap_node = cmds.createNode('remapValue', name = f'{part_name}_first_fist_remap')
        cmds.connectAttr (f'{settings.control_name}.fist', f'{first_finger_first_remap_node}.i')
        cmds.setAttr (f'{first_finger_first_remap_node}.imx', 10)
        cmds.setAttr (f'{first_finger_first_remap_node}.imn', 0)
        cmds.connectAttr ("{}.fist_finger_01_factor".format(settings.control_name), f'{first_finger_first_remap_node}.omx')
        cmds.setAttr (f'{first_finger_first_remap_node}.omn', 0)

        sec_finger_first_remap_node = cmds.createNode('remapValue', name = f'{part_name}_sec_fist_remap')
        cmds.connectAttr (f'{settings.control_name}.fist', f'{sec_finger_first_remap_node}.i')
        cmds.setAttr (f'{sec_finger_first_remap_node}.imx', 10)
        cmds.setAttr (f'{sec_finger_first_remap_node}.imn', 0)
        cmds.connectAttr ("{}.fist_finger_02_factor".format(settings.control_name), f'{sec_finger_first_remap_node}.omx')
        cmds.setAttr (f'{sec_finger_first_remap_node}.omn', 0)

        trd_finger_first_remap_node = cmds.createNode('remapValue', name = f'{part_name}_trd_fist_remap')
        cmds.connectAttr (f'{settings.control_name}.fist', f'{trd_finger_first_remap_node}.i')
        cmds.setAttr (f'{trd_finger_first_remap_node}.imx', 10)
        cmds.setAttr (f'{trd_finger_first_remap_node}.imn', 0)
        cmds.connectAttr ("{}.fist_finger_03_factor".format(settings.control_name), f'{trd_finger_first_remap_node}.omx')
        cmds.setAttr (f'{trd_finger_first_remap_node}.omn', 0)

        wave_reverse_mult = cmds.createNode('multDoubleLinear', name = f'{part_name}_revWave_mult')
        cmds.setAttr (f'{wave_reverse_mult}.i2', -2)
        cmds.connectAttr (f'{settings.control_name}.wave', f'{wave_reverse_mult}.i1') 

        pinch_counter = 1
        thumb_fist_values = ["{}.fist_thumb_01_factor".format(settings.control_name), "{}.fist_thumb_02_factor".format(settings.control_name), "{}.fist_thumb_03_factor".format(settings.control_name)]
        thumb_fist_index = 0
        
        for elem in control_dict :
            for part in control_dict[elem] :

                group = control_dict[elem][part]['buffer']

                if "01" in group :
                    fist_remap_node = first_finger_first_remap_node
                elif "02" in group :
                    fist_remap_node = sec_finger_first_remap_node
                elif "03" in group:
                    fist_remap_node = trd_finger_first_remap_node
                else :
                    fist_remap_node = ""
                    
                if 'thumb' in control_dict.keys() :
                    compare = control_dict[list(control_dict.keys())[0]]
                    index_compare = control_dict[list(control_dict.keys())[1]]

                else :
                    compare = ''
                    index_compare = control_dict[list(control_dict.keys())[0]]

                if 'meta' in group and control_dict[elem] != compare and control_dict[elem] != index_compare:

                    meta_pinch_mult = cmds.createNode('multDoubleLinear', name = group.replace('_{}'.format(datas.GROUP_naming), '_pinch_mult'))
                    cmds.connectAttr (f'{settings.control_name}.pinch', f'{meta_pinch_mult}.i2')
                    cmds.setAttr (f'{meta_pinch_mult}.i1', pinch_counter/2)
                    cmds.connectAttr (f'{meta_pinch_mult}.o', f'{group}.rz')
                
                elif 'thumb' in control_dict.keys() and control_dict[elem] == compare:

                    thumb_remap = cmds.createNode('remapValue', name = f'{part_name}_fist_remap')
                    cmds.connectAttr (f'{settings.control_name}.fist', f'{thumb_remap}.i')
                    cmds.setAttr (f'{thumb_remap}.imx', 10)
                    cmds.setAttr (f'{thumb_remap}.imn', 0)
                    cmds.connectAttr (thumb_fist_values[thumb_fist_index], f'{thumb_remap}.omx')
                    cmds.setAttr (f'{thumb_remap}.omn', 0)

                    cmds.connectAttr (f'{thumb_remap}.ov', f'{group}.rz')

                    thumb_fist_index +=1

                elif 'meta' in group and control_dict[elem] == index_compare :
                    pass
                else :

                    wave_add = cmds.createNode('addDoubleLinear', name = group.replace('_{}'.format(datas.GROUP_naming), '_wave_add'))

                    if control_dict[elem] != index_compare: 

                        pinch_add = cmds.createNode('addDoubleLinear', name = group.replace('_{}'.format(datas.GROUP_naming), '_pinch_add'))
                        cmds.connectAttr (f'{fist_remap_node}.ov', f'{pinch_add}.i1')

                        pinch_mult = cmds.createNode('multDoubleLinear', name = group.replace('_{}'.format(datas.GROUP_naming), '_pinch_mult'))
                        cmds.connectAttr (f'{settings.control_name}.pinch', f'{pinch_mult}.i2')
                        cmds.setAttr (f'{pinch_mult}.i1', pinch_counter)
                        cmds.connectAttr (f'{pinch_mult}.o', f'{pinch_add}.i2')
                        cmds.connectAttr (f'{pinch_add}.o', f'{wave_add}.i2')

                        pinch_counter += 1

                    else :
                        cmds.connectAttr (f'{fist_remap_node}.ov', f'{wave_add}.i2')

                    wave_rev = cmds.createNode('multDoubleLinear', name = group.replace('_{}'.format(datas.GROUP_naming), '_wave_rev'))
                    cmds.setAttr (f'{wave_rev}.i2', -1)

                    if control_dict[elem][part] == control_dict[elem][list(control_dict[elem].keys())[2]] :
                        cmds.connectAttr (f'{wave_reverse_mult}.o', f'{wave_rev}.i1')
                        cmds.connectAttr (f'{wave_rev}.o', f'{wave_add}.i1')
                    else :
                        cmds.connectAttr (f'{settings.control_name}.wave', f'{wave_rev}.i1')
                        cmds.connectAttr (f'{wave_rev}.o', f'{wave_add}.i1')

                    
                    cmds.connectAttr (f'{wave_add}.o', f'{group}.rz')
        
        # Kill inverse scale connection
        for meta in meta_list :
            utils.kill_inverse_scale (meta)

        retrun_control_list = []
        for finger in control_dict :
            for joint in control_dict[finger] :
                retrun_control_list.append(control_dict[finger][joint]["control"])

        return {"outputs" : "", 
                "output_attr" : "" , 
                "controls" : {"hand_controls" : retrun_control_list, "settings" : settings},
                "module" : module_group}
    
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
    def build_neck_rig (self, master_part, spine_part, neck_start_datas) :

        input_group, output_group, public_group, private_group, module_group = utils.init_module_sequence(self.rig_name + '_neck' )
        utils.connect_modules (spine_part["outputs"][1], input_group)

        input_attributs = master_part["output_attr"] + [spine_part["output_attr"][1][0]]
        
        neck_attribut_list = utils.add_attr_modules (input_group, input_attributs)

        neck_parent_dict = {}
        neck_parent_dict_name = ["Master", "Root", "COG", "Top_Spine"]
        
        for each in range(len(input_attributs)) :
            neck_parent_dict[neck_parent_dict_name[each]] = neck_attribut_list[each]

        bone_list = []
        start_bones_list = neck_start_datas["joints"]
        start_bounding_box_list = neck_start_datas["bounding_box"]
        visibility_control = master_part["controls"]["settings"]

        for each in start_bones_list :
            cmds.select(d=True)
            bones = cmds.joint (name = f'{self.rig_name}_{each}', rad = self.joint_radius)
            bone_list.append(bones)
            cmds.matchTransform(bones, each, pos=True, rot=True)

            if bone_list.index(bones) != 0 :
                cmds.parent (bones, bone_list[bone_list.index(bones)-1])


        fk_control_list = []
        fk_control_list.append(ctrl.ControlObj(bone_list[0].replace(datas.JOINT_naming, datas.CONTROL_naming),
                                      'Circle', 
                                      "Yellow", 
                                      utils.get_object_size(start_bounding_box_list[0]) + .2))
        ik_control = ctrl.ControlObj(bone_list[1].replace(datas.JOINT_naming, "ik_{}".format(datas.CONTROL_naming)),
                                      'Circle', 
                                      "Red", 
                                      utils.get_object_size(start_bounding_box_list[1]))
        fk_control_list.append(ctrl.ControlObj(bone_list[1].replace(datas.JOINT_naming, datas.CONTROL_naming),
                                      'Circle', 
                                      "Yellow", 
                                      utils.get_object_size(start_bounding_box_list[0])))
        
        cmds.matchTransform(fk_control_list[0].control_name, bone_list[0], pos=True, rot=True)
        cmds.parent (ik_control.control_name, fk_control_list[1].control_name)
        cmds.matchTransform(fk_control_list[1].control_name, bone_list[1], pos=True, rot=True)

        cmds.parent (fk_control_list[1].control_name, fk_control_list[0].control_name)
        mat_const.opm(fk_control_list[1].control_name)
        cmds.connectAttr (f'{visibility_control.control_name}.controlVis', f'{fk_control_list[0].control_name}.visibility')
        cmds.connectAttr (f'{visibility_control.control_name}.controlVis', f'{fk_control_list[1].control_name}.visibility')

        mat_const.parent(fk_control_list[0].control_name, bone_list[0], False, True, True, True, False, bone_list[0].replace('_{}'.format(datas.JOINT_naming),'_const'))
        mat_const.parent(ik_control.control_name, bone_list[1], False, True, True, True, False, bone_list[1].replace('_{}'.format(datas.JOINT_naming),'_const'))
        mat_const.parent(fk_control_list[1].control_name, bone_list[2], True, True, True, True, False, bone_list[2].replace('_{}'.format(datas.JOINT_naming),'_const')) 

        cv_list = []
        for bones in bone_list :
            translate = cmds.xform (bones, q=True, t=True, ws=True)
            tuple(translate)
            cv_list.append(translate)

        #create curve
        twist_curve = cmds.curve(d=2, p=cv_list, name = f'{self.rig_name}_neck_bend_curve')
        cmds.rename ('curveShape1', f'{twist_curve}Shape')

        #skin curve
        curve_skin_name = f'{self.rig_name}_neck_curve_skin'
        cmds.skinCluster(bone_list, twist_curve, mi = 1, name = curve_skin_name, wd = 0, ih = True, sm = 0, tsb=True)
        for x in range (len(bone_list)) :
            cmds.skinPercent(curve_skin_name, f'{twist_curve}.cv[{x}]', transformValue=(bone_list[x], 1))

        #create twist
        _, spline_ik, spline_eff, spline_twist_joint = utils.create_twist (f'{self.rig_name}_neck', bone_list[0], bone_list[2], bone_list[0], 4, self.joint_radius, False, twist_curve, "{}.scaleX".format(input_group), 'X', [1,0,0])

        for each in spline_twist_joint :
            self.binded_bones.append (each)

        #kill inverse scale
        utils.kill_inverse_scale (bone_list[0])

        utils.parent_space (fk_control_list[0], neck_parent_dict, f'{self.rig_name}_neck', fk_control_list[0], 'fk')

        cmds.parent (spline_ik, bone_list[0], twist_curve, private_group)
        cmds.parent (fk_control_list[0].control_name, public_group)

        mat_const.parent(bone_list[2], output_group, False, True, True, True, False, output_group.replace('_{}'.format(datas.GROUP_naming),'_const'))

        return {"outputs" : output_group, 
                "output_attr" : output_group , 
                "controls" : {"fk_controls" : fk_control_list, "ik_control" : ik_control},
                "ik_twist" : spline_ik,
                "module" : module_group
                }
    

    def build_head_rig (self, master_part, spine_part, neck_part, head_start_datas) :

        input_group, output_group, public_group, private_group, module_group = utils.init_module_sequence(self.rig_name + '_head' )
        utils.connect_modules (neck_part["outputs"], input_group)

        input_attributs = master_part["output_attr"] + [spine_part["output_attr"][1][0]] + [neck_part["output_attr"]]
        head_bones_list = []

        visibility_control = master_part["controls"]["settings"]
        joint_start_list = head_start_datas["joints"]
        bounding_box_start_list = head_start_datas["bounding_box"]

        input_attributs_list = []
        for attribut in input_attributs :
            input_attributs_list.append(attribut)

        
        for bones in joint_start_list : 

            cmds.select(d=True)
            joint = cmds.joint(name = f'{self.rig_name}_{bones}', rad = self.joint_radius)
            head_bones_list.append (joint)
            cmds.matchTransform(joint, bones, rot=True, pos=True)
            self.binded_bones.append (joint)

        input_attributs_list.append(head_bones_list[0])

        input_attributs_dict = utils.add_attr_modules (input_group, input_attributs_list)
        auxiliaire_bone_list = []

        head_parent_dict = {
            "Master" : input_attributs_dict[0],
            "Root" : input_attributs_dict[1],
            "COG" : input_attributs_dict[2],
            "TopSpine" : input_attributs_dict[3],
            "Neck" : input_attributs_dict[4],
        }
        eyes_parent_dict = {
            "Master" : input_attributs_dict[0],
            "Root" : input_attributs_dict[1],
            "COG" : input_attributs_dict[2],
            "TopSpine" : input_attributs_dict[3],
            "Neck" : input_attributs_dict[4],
            "Head" : input_attributs_dict[5]
        }

        for joint in [head_bones_list[1],head_bones_list[2]] :

            cmds.select(d=True)
            auxiliaire_joint_name = joint.replace('_{}'.format(datas.JOINT_naming), '')
            auxiliaire_joint = cmds.joint(name = f'{auxiliaire_joint_name}_aux_jnt', rad = self.joint_radius)
            auxiliaire_bone_list.append (auxiliaire_joint)
            cmds.matchTransform(auxiliaire_joint, joint, pos=True, rot=True)
            cmds.parent (joint, auxiliaire_joint)

        cmds.parent (auxiliaire_bone_list[0], auxiliaire_bone_list[1], head_bones_list[0])

        head_control = ctrl.ControlObj(head_bones_list[0].replace(datas.JOINT_naming, datas.CONTROL_naming),
                                      'Circle', 
                                      "Yellow", 
                                      utils.get_object_size(bounding_box_start_list[0]))
        eye_L_control = ctrl.ControlObj(head_bones_list[1].replace(datas.JOINT_naming, datas.CONTROL_naming),
                                      'Circle', 
                                      "Cyan", 
                                      1.5)
        eye_R_control = ctrl.ControlObj(head_bones_list[2].replace(datas.JOINT_naming, datas.CONTROL_naming),
                                      'Circle', 
                                      "Red", 
                                      1.5)
        
        cmds.matchTransform(head_control.control_name, head_bones_list[0], pos=True, rot=True)

        eye_control_position = ((cmds.xform(head_bones_list[1], q=True, translation=True, ws=True)[0] + cmds.xform(head_bones_list[2], q=True, translation=True, ws=True)[0])/2, 
                                (cmds.xform(head_bones_list[1], q=True, translation=True, ws=True)[1] + cmds.xform(head_bones_list[2], q=True, translation=True, ws=True)[1])/2,
                                (cmds.xform(head_bones_list[1], q=True, translation=True, ws=True)[2] + cmds.xform(head_bones_list[2], q=True, translation=True, ws=True)[2])/2)
        
        eye_control_temp_loc = cmds.spaceLocator(name = 'tempEyesControl')[0]
        cmds.setAttr (f'{eye_control_temp_loc}.t', *eye_control_position)

        eyes_control = ctrl.ControlObj(head_bones_list[1].replace("_L_{}".format(datas.JOINT_naming), "s_{}".format(datas.CONTROL_naming)),
                                      'Square', 
                                      "Yellow", 
                                      2)

        cmds.connectAttr (f'{visibility_control.control_name}.controlVis', f'{head_control.control_name}.visibility')
        cmds.connectAttr (f'{visibility_control.control_name}.controlVis', f'{eyes_control.control_name}.visibility')

        mat_const.parent(head_control.control_name, head_bones_list[0], False, True, True, True, False, head_bones_list[0].replace("_{}".format(datas.JOINT_naming),'_const'))

        cmds.select(d=True)

        head_parent_groups = utils.parent_space (head_control, head_parent_dict, f'{self.rig_name}_head', head_control, 'fk')

        eye_dist = utils.get_absolute_distance (head_bones_list[0], eye_control_temp_loc, 2.5)

        cmds.setAttr (f'{eyes_control.control_name}.t', *eye_dist)
        cmds.setAttr (f'{eyes_control.control_name}.ty', cmds.getAttr(f'{eye_control_temp_loc}.ty'))

        cmds.matchTransform (eye_L_control.control_name, head_bones_list[1])
        cmds.setAttr (f'{eye_L_control.control_name}.tz', eye_dist[2])
        cmds.matchTransform (eye_R_control.control_name, head_bones_list[2])
        cmds.setAttr (f'{eye_R_control.control_name}.tz', eye_dist[2])

        cmds.parent (eye_L_control.control_name, eye_R_control.control_name, eyes_control.control_name)
        mat_const.opm (eye_L_control.control_name)
        mat_const.opm (eye_R_control.control_name)

        eyes_parent_spaces = utils.parent_space (eyes_control, eyes_parent_dict, f'{self.rig_name}_eyes', eyes_control, 'ik')

        cmds.delete (eye_control_temp_loc)

        mat_const.aim (eye_L_control.control_name, head_bones_list[1], auxiliaire_bone_list[0], head_bones_list[0], [0,0,1], [0,1,0], [0,1,0], False, head_bones_list[1].replace("_{}".format(datas.JOINT_naming),'_aim_const'))
        mat_const.aim (eye_R_control.control_name, head_bones_list[2], auxiliaire_bone_list[1], head_bones_list[0], [0,0,1], [0,1,0], [0,1,0], False, head_bones_list[2].replace("_{}".format(datas.JOINT_naming),'_aim_const'))
        
        utils.kill_inverse_scale (head_bones_list[0])
 
        cmds.parent (head_bones_list[0], private_group)
        cmds.parent (eyes_control.control_name, head_control.control_name, public_group)

        cmds.select(d=True)
        cmds.connectAttr (f'{head_bones_list[0]}.worldMatrix[0]' , f'{neck_part["ik_twist"]}.dWorldUpMatrixEnd', force = True)

        return {"outputs" : "",
                "output_attr" : "" , 
                "controls" : {"head_control" : head_control, "eyes_controls" : [eyes_control, eye_L_control, eye_R_control]},
                "module" : module_group}
    
    def build_foot_rigging (self, master_part, spine_part, leg_part, side, foot_start_datas, reverse_foot_start_datas) :

        input_group, output_group, public_group, private_group, module_group = utils.init_module_sequence(f'{self.rig_name}_foot{side}' )
        utils.connect_modules (leg_part["outputs"], input_group)

        # Ankle joint creation
        cmds.select(d=True)
        foot_ankle = cmds.joint(name = leg_part["last_bone"].replace('ankle','foot_ankle'), rad = self.joint_radius)
        cmds.matchTransform(foot_ankle, leg_part["last_bone"], pos=True, rot=True)

        start_joint_list = foot_start_datas["joints"]
        start_reverse_joint_list = reverse_foot_start_datas["joints"]
        start_bounding_box_list = foot_start_datas["bounding_box"]

        foot_dict = {}
        finger_index=0
        bounding_box_index=0

        for x in range(len(start_joint_list)) :
            if not "tip" in start_joint_list[x] :
                finger_datas_dict = {}
                current_dict = "finger_{}".format(finger_index)
                finger_index += 1

                finger_datas_dict[start_joint_list[x]] = start_bounding_box_list[bounding_box_index]
                bounding_box_index +=1
            else :
                finger_datas_dict[start_joint_list[x]] = ""
                foot_dict[current_dict] = finger_datas_dict

        # Ball joint creation
        cmds.select(d=True)
        ball_joint_name = start_joint_list[0]
        ball_joint = cmds.joint(name = f'{self.rig_name}_{ball_joint_name}')
        cmds.matchTransform(ball_joint, ball_joint_name, pos=True, rot=True)
        cmds.parent (ball_joint, foot_ankle)

        main_skeleton = [foot_ankle, ball_joint]
        joint_dics = []
        joint_fk_dics = []
        joint_ik_dics = []
        fk_list_skeleton = []
        ik_list_skeleton = []

        #create aux joint
        cmds.select(d=True)
        auxJoint = cmds.joint(name = '{}_{}_ankle_aux_{}'.format(self.rig_name, side, datas.JOINT_naming), rad = self.joint_radius)
        cmds.matchTransform(auxJoint, main_skeleton[0])
        mat_const.parent (input_group, auxJoint, True, True, True, True, False, auxJoint.replace('_{}'.format(datas.JOINT_naming),'_const'))

        #create toes joints
        names = [foot_ankle, ball_joint]

        for i in range (2) :

            cmds.select(d=True)
            fk_joint = cmds.joint (name = names[i].replace('_{}'.format(datas.JOINT_naming),'_fk_{}'.format(datas.JOINT_naming)), rad = self.joint_radius)
            fk_list_skeleton.append (fk_joint)
            cmds.matchTransform(fk_joint, names[i], pos=True, rot=True)
            cmds.select(d=True)
            ik_joint = cmds.joint (name = names[i].replace('_{}'.format(datas.JOINT_naming),'_ik_{}'.format(datas.JOINT_naming)), rad = self.joint_radius)
            ik_list_skeleton.append (ik_joint)
            cmds.matchTransform(ik_joint, names[i], pos=True, rot=True)

            if i != 0:
                cmds.parent (fk_joint, fk_list_skeleton[i-1])
                cmds.parent (ik_joint, ik_list_skeleton[i-1]) 
                for part in [fk_list_skeleton[0], ik_list_skeleton[0]] :
                    cmds.makeIdentity(part, apply = True, rotate = True)
                    cmds.joint(part, e=True, oj = 'yzx', sao = 'xup')
            
        cmds.select(d=True)
        toe_ref_joint = cmds.joint(name = '{}_{}_toeIK_tip_{}'.format(self.rig_name, side, datas.JOINT_naming))
        cmds.matchTransform(toe_ref_joint, ball_joint, pos=True, rot=True)
        toe_ref_jointDist = utils.get_relative_distance (ball_joint, start_reverse_joint_list[1], 1)
        cmds.parent (toe_ref_joint, ik_list_skeleton[1])
        cmds.setAttr(f'{toe_ref_joint}.r', *(0,0,0))
        cmds.setAttr(f'{toe_ref_joint}.jo', *(0,0,0))
        cmds.setAttr (f'{toe_ref_joint}.tz', cmds.getAttr(f'{toe_ref_joint}.tz') + toe_ref_jointDist[2])
        

        for finger in foot_dict :
            
            temp_toe_joint = []
            temp_fk = []
            temp_ik = []

            for joint in foot_dict[finger] :
                cmds.select(d=True)
                toe_joint = cmds.joint(name = f'{self.rig_name}_{joint}')
                cmds.matchTransform(toe_joint, joint, pos=True, rot=True)

                fk_name = toe_joint.replace('_jnt','_foot_FK_jnt')
                ik_name = toe_joint.replace('_jnt','_foot_IK_jnt')

                cmds.select(d=True)
                fk_joint = cmds.joint (name = fk_name, rad = self.joint_radius)
                cmds.matchTransform(fk_joint, toe_joint, pos=True, rot=True)
                cmds.select(d=True)
                ik_joint = cmds.joint (name = ik_name, rad = self.joint_radius)
                cmds.matchTransform(ik_joint, toe_joint, pos=True, rot=True)

                temp_toe_joint.append(toe_joint)
                main_skeleton.append(toe_joint)
                fk_list_skeleton.append(fk_joint)
                ik_list_skeleton.append(ik_joint)
                temp_fk.append(fk_joint)
                temp_ik.append(ik_joint)

            cmds.parent (temp_toe_joint[1], temp_toe_joint[0])
            cmds.parent (temp_toe_joint[0], ball_joint)
            cmds.parent (temp_fk[1], temp_fk[0])
            cmds.parent (temp_fk[0], fk_list_skeleton[1])
            cmds.parent (temp_ik[1], temp_ik[0])
            cmds.parent (temp_ik[0], ik_list_skeleton[1])
            joint_dics.append ({finger : temp_toe_joint})
            joint_fk_dics.append ({finger : temp_fk})
            joint_ik_dics.append ({finger : temp_ik})

        #freeze transformations and reset rotate order
        for finger in  range(len(joint_dics)) :  
            for elem in joint_dics[finger]:
                for x in range(len(joint_dics[finger][elem])) :
                    self.binded_bones.append (joint_dics[finger][elem][x])

                    if joint_dics[finger][elem][x] == joint_dics[finger][elem][-1]:
                        for part in [joint_dics[finger][elem][x], joint_fk_dics[finger][elem][x], joint_ik_dics[finger][elem][x]] :
                            cmds.makeIdentity(part, apply = True, rotate = True)
                            cmds.setAttr (f'{part}.jointOrientX',0)
                            cmds.setAttr (f'{part}.jointOrientY',0)
                            cmds.setAttr (f'{part}.jointOrientZ',0)
            
                    else :
                        for part in [joint_fk_dics[finger][list(joint_fk_dics[finger].keys())[0]], joint_ik_dics[finger][list(joint_ik_dics[finger].keys())[0]]] :
                            cmds.makeIdentity(part, apply = True, rotate = True)
                            cmds.joint(part, e=True, oj = 'yzx', sao = 'xup')

        #parent skeletons
        cmds.parent (main_skeleton[0], fk_list_skeleton[0], ik_list_skeleton[0], auxJoint)

        self.foot_finger_ik_fk (main_skeleton, fk_list_skeleton, ik_list_skeleton, leg_part["controls"]["settings"].control_name)

        #get distance for ik pvs and bank_mult
        ball_ankle_distance = utils.get_relative_distance (ik_list_skeleton[0], ik_list_skeleton[1], .25)
        if side == 'L' :
            yDist = - ((ball_ankle_distance[2])**2)**0.5
            bank_mult = -5
            color = 'Cyan'
        else :
            yDist = + ((ball_ankle_distance[2])**2)**0.5
            bank_mult = 5
            color = 'Red'

        
        reverse_visibility = cmds.createNode("reverse", name = "{}_foot_{}_visibility_rev".format(self.rig_name, side))
        reverse_visibility_mult = cmds.createNode("multDoubleLinear", name = "{}_foot_{}_visibility_mult".format(self.rig_name, side))
        cmds.connectAttr("{}.controlVis".format(master_part["controls"]["settings"].control_name), "{}.input1".format(reverse_visibility_mult))
        cmds.connectAttr("{}.ikFkSwitch".format(leg_part["controls"]["settings"].control_name), "{}.inputX".format(reverse_visibility))
        cmds.connectAttr("{}.outputX".format(reverse_visibility), "{}.input2".format(reverse_visibility_mult))

        main_reverse_skeleton, bank_groups = self.reverse_foot_system (leg_part["controls"]["ik_controls"][0], start_reverse_joint_list, ik_list_skeleton, f'{self.rig_name}_reverseFoot{side}', bank_mult)

        #connect ankle
        mat_const.parent(main_reverse_skeleton[3], leg_part["ik_handle"], False, True, False, False, False, leg_part["ik_handle"].replace('_{}'.format(datas.IK_HANDLE_naming),'_ik_const'))
        decompose_node = cmds.listConnections("{}.translate".format(leg_part["strech_groups"][1]), d=True)[1]
        mult_mat_strech = cmds.listConnections(decompose_node, d=True) [00]
        cmds.connectAttr("{}.worldMatrix[0]".format(main_reverse_skeleton[3]), "{}.matrixIn[0]".format(mult_mat_strech), force = True)

        toes_ik_list = []
        fk_contorl_list = []

        for each in range(len(joint_fk_dics)) :
            for elem in joint_fk_dics[each] :

                toe_fk_control = ctrl.ControlObj(joint_fk_dics[each][elem][0].replace(datas.JOINT_naming, datas.CONTROL_naming),
                                    'Circle Pin', 
                                    color, 
                                    1.5)
                cmds.matchTransform(toe_fk_control.control_name, joint_fk_dics[each][elem][0])

                mat_const.parent(toe_fk_control.control_name, joint_fk_dics[each][elem][0], False, True, True, True, False, joint_fk_dics[each][elem][0].replace('_jnt','_jntConst'))
                cmds.connectAttr (f'{reverse_visibility_mult}.o',f'{toe_fk_control.control_name}.visibility')
                mat_const.parent(input_group, toe_fk_control.control_name, True, True, True, True, True, toe_fk_control.control_name.replace('_{}'.format(datas.CONTROL_naming),'_const'))
                cmds.setAttr (f'{toe_fk_control.control_name}.t', *(0,0,0))
                cmds.setAttr (f'{toe_fk_control.control_name}.r', *(0,0,0))
                cmds.setAttr (f'{joint_fk_dics[each][elem][0]}.jo', *(0,0,0))

                #create ikball
                ball_ik = joint_ik_dics[each][elem][0].replace(datas.JOINT_naming, datas.IK_HANDLE_naming)
                ball_eff = joint_ik_dics[each][elem][0].replace(datas.JOINT_naming, datas.IK_EFFECTOR_naming)
                ball_pv = cmds.spaceLocator(name = joint_ik_dics[each][elem][0].replace(datas.JOINT_naming,'PV'))[0]
                ik_buffer = cmds.createNode ('transform', name =f'{ball_ik}_{datas.GROUP_naming}')

                cmds.matchTransform (ik_buffer, joint_ik_dics[each][elem][0], pos=True, rot=True)
                cmds.ikHandle(sj=joint_ik_dics[each][elem][0], ee = joint_ik_dics[each][elem][1], name = ball_ik, sol = 'ikRPsolver')
                cmds.rename ('effector1', ball_eff)
                cmds.matchTransform (ball_pv, joint_ik_dics[each][elem][0], pos=True)
                cmds.parent(ball_ik, ik_buffer)
                cmds.poleVectorConstraint(ball_pv, ball_ik)
                cmds.setAttr (f'{ball_pv}.tx', yDist)
                cmds.parent (ball_pv, main_reverse_skeleton[2])

                mat_const.parent(main_reverse_skeleton[1], ik_buffer, True, True, True, True, True, ball_ik.replace('_IK','_ik_const'))
                leg_part["controls"]["ik_controls"][0].add_attribut('double', f'toe{each+1}_RollZ', ['',''], 0, [''])
                cmds.connectAttr (f'{leg_part["controls"]["ik_controls"][0].control_name}.toe{each+1}_RollZ', f'{ik_buffer}.rz')
                cmds.setAttr (f'{ball_pv}.tx', yDist)
                toes_ik_list.append(ik_buffer)
                fk_contorl_list.append(toe_fk_control)

         #ankle_ik 
        ankle_ik = f'{self.rig_name}_{side}_ankle_IK'
        ankle_eff = f'{self.rig_name}_{side}_ankle_eff'
        ankle_pole_vector = cmds.spaceLocator(name = f'{self.rig_name}_{side}_ankle_pole_vector')[0]
        cmds.ikHandle(sj=ik_list_skeleton[0], ee = ik_list_skeleton[1], name = ankle_ik, sol = 'ikRPsolver')
        cmds.rename ('effector1', ankle_eff)
        cmds.matchTransform (ankle_pole_vector, ik_list_skeleton[0], pos=True)
        cmds.poleVectorConstraint(ankle_pole_vector, ankle_ik)

        mat_const.parent(main_reverse_skeleton[2], ankle_ik, False, True, False, False, False, ankle_ik.replace(datas.IK_HANDLE_naming,'_ik_const'))
        mat_const.parent(leg_part["controls"]["ik_controls"][0].control_name, ik_list_skeleton[0], True, False, False, True, False, ankle_ik.replace(datas.IK_HANDLE_naming,'_ik_const'))
        cmds.parent (ankle_pole_vector, main_reverse_skeleton[3])

        toe_tip_ik_name = toe_ref_joint.replace(datas.JOINT_naming, datas.IK_HANDLE_naming)
        toe_tip_eff_name = toe_ref_joint.replace(datas.JOINT_naming, datas.IK_EFFECTOR_naming)
        toe_tip_pv = cmds.spaceLocator(name = toe_ref_joint.replace(datas.JOINT_naming,'PV'))[0]
        cmds.ikHandle(sj=ik_list_skeleton[1], ee = toe_ref_joint, name = toe_tip_ik_name, sol = 'ikRPsolver')
        cmds.rename ('effector1', toe_tip_eff_name)
        mat_const.parent(main_reverse_skeleton[1], toe_tip_ik_name, True, True, False, False, False, toe_tip_ik_name.replace(datas.IK_HANDLE_naming,'_ik_const'))
        cmds.matchTransform(toe_tip_pv, ik_list_skeleton[1])
        cmds.parent(toe_tip_pv, main_reverse_skeleton[1])
    
        cmds.poleVectorConstraint(toe_tip_pv, toe_tip_ik_name)

        cmds.setAttr(f'{ankle_pole_vector}.tx', yDist)
        cmds.setAttr (f'{toe_tip_pv}.tx', yDist)
        utils.kill_inverse_scale (auxJoint)

        cmds.parent (auxJoint, toes_ik_list, ankle_ik, toe_tip_ik_name, bank_groups[0], private_group)
        for control in fk_contorl_list :
            cmds.parent (control.control_name, public_group)

        return {"outputs" : output_group, 
                "output_attr" : "" , 
                "controls" : fk_contorl_list,
                "module" : module_group,
                }

    def foot_finger_ik_fk (self, main_skeleton, fk_skeleton, ik_skeleton, ik_fk_switch): 
         
        for x in range(len(main_skeleton)) :

            fk_mult_node = cmds.createNode('multMatrix', name = main_skeleton[x].replace('_{}'.format(datas.JOINT_naming), '_fk_mult'))
            ik_mult_node = cmds.createNode('multMatrix', name = main_skeleton[x].replace('_{}'.format(datas.JOINT_naming), '_ik_mult'))
            decompose_node = cmds.createNode('decomposeMatrix', name = main_skeleton[x].replace('_{}'.format(datas.JOINT_naming), '_switch_decMat'))
            blend_node = cmds.createNode('blendMatrix', name = main_skeleton[x].replace('_{}'.format(datas.JOINT_naming), "_ik_fk_switch_blend_node"))

            cmds.connectAttr("{}.worldMatrix[0]".format(fk_skeleton[x]), "{}.matrixIn[0]".format(fk_mult_node))
            cmds.connectAttr("{}.worldMatrix[0]".format(ik_skeleton[x]), "{}.matrixIn[0]".format(ik_mult_node))
            cmds.connectAttr ('{}.pim'.format(main_skeleton[x]), f'{fk_mult_node}.matrixIn[1]')
            cmds.connectAttr ('{}.pim'.format(main_skeleton[x]), f'{ik_mult_node}.matrixIn[1]')

            cmds.connectAttr (f'{fk_mult_node}.matrixSum', "{}.inputMatrix".format(blend_node))
            cmds.connectAttr (f'{ik_mult_node}.matrixSum', "{}.target[0].targetMatrix".format(blend_node))

            cmds.connectAttr (f'{ik_fk_switch}.ikFkSwitch', "{}.target[0].weight".format(blend_node))
            cmds.connectAttr (f'{blend_node}.outputMatrix', "{}.inputMatrix".format(decompose_node))

            cmds.connectAttr (f'{decompose_node}.ot',f'{main_skeleton[x]}.t')
            cmds.connectAttr (f'{decompose_node}.or',f'{main_skeleton[x]}.r')
            cmds.connectAttr (f'{decompose_node}.os',f'{main_skeleton[x]}.s')

            cmds.setAttr (f'{main_skeleton[x]}.jo', *(0,0,0))


    #reverse foot function
    def reverse_foot_system (self, leg_ik_control, start_reverse_bones, foot_ik_bones, naming, bank_mult) :
        
        reverse_driver_bones = [start_reverse_bones[0], start_reverse_bones[1], foot_ik_bones[1], foot_ik_bones[0]]
        
        leg_ik_control.add_attribut('separator', 'reverseFootAttributs', ('',''), 0, '')
        leg_ik_control.add_attribut('double', 'footRoll', ('',''), 0, '')
        leg_ik_control.add_attribut('double', 'footBank', ('',''), 0, '')
        leg_ik_control.add_attribut('double', 'reverseMult', ('',''), 1, '')
        leg_ik_control.add_attribut( 'separator', 'footAttr', ('',''), '', '')
        leg_ik_control.add_attribut( 'double', 'heelRot_X', ('',''), 0, '')
        leg_ik_control.add_attribut( 'double', 'heelRot_Y', ('',''), 0, '')
        leg_ik_control.add_attribut( 'double', 'toeRot_X', ('',''), 0, '')
        leg_ik_control.add_attribut( 'double', 'toeRot_Y', ('',''), 0, '')
        main_reverse_skeleton = []

        for bones in reverse_driver_bones :
            
            cmds.select(d=True)
            joint = cmds.joint (name = '{}_{}'.format(naming, bones), rad = self.joint_radius)
            cmds.matchTransform (joint, bones, pos=True, rot=True)
            main_reverse_skeleton.append(joint)

            if bones != reverse_driver_bones [0] :
                cmds.parent (joint, main_reverse_skeleton[reverse_driver_bones.index(bones)-1])
            
        for bone in main_reverse_skeleton :
            cmds.makeIdentity(bone, apply = True, rotate = True)

            if bone != main_reverse_skeleton[-1]:
                cmds.joint(bone, e=True, oj = 'yxz', sao = 'xup')
            else :
                cmds.setAttr (f'{bone}.jointOrient', *(0,0,0))

        bank_groups = []
        for obj in [start_reverse_bones[2], start_reverse_bones[3]] :
            bank_naming = obj.replace('_{}'.format(datas.JOINT_naming),'Bank_{}'.format(datas.GROUP_naming))
            bank_naming = bank_naming.replace('_rev','')

            buff = cmds.createNode ('transform', name = "{}_{}".format(self.rig_name, bank_naming))
            cmds.matchTransform(buff, obj, pos=True, rot=True)
            
            bank_groups.append(buff)

        cmds.parent (bank_groups[1], bank_groups[0])
        cmds.parent (main_reverse_skeleton[0],bank_groups[1])
        
        cmds.makeIdentity(main_reverse_skeleton[0], apply = True, rotate = True)
        mat_const.opm(bank_groups[1])
        mat_const.parent (leg_ik_control.control_name, bank_groups[0], True, True, True, True, True, bank_groups[0].replace('_{}'.format(datas.GROUP_naming),'_const'))
        cmds.setAttr (f'{bank_groups[0]}.t', *(0,0,0))
        cmds.setAttr (f'{bank_groups[0]}.r', *(0,0,0))

        self.reverse_system (main_reverse_skeleton, bank_groups, leg_ik_control, "{}_reverse_system".format(naming), bank_mult)

        return main_reverse_skeleton, bank_groups

    def reverse_system (self, reverse_skeleton, bank, control, name, bank_multFactor) :
        x= 60

        bank_condition = cmds.createNode('condition', name = f'{name}_bankReverse_cond')
        bank_mult = cmds.createNode('multDoubleLinear', name = f'{name}_bankReverse_mult')
        reverse_global_mult = cmds.createNode('multiplyDivide', name = f'{name}_footReverse_mult')
        cmds.connectAttr (f'{control.control_name}.reverseMult', f'{reverse_global_mult}.i2x')
        cmds.connectAttr (f'{control.control_name}.reverseMult', f'{reverse_global_mult}.i2y')
        cmds.connectAttr (f'{control.control_name}.reverseMult', f'{reverse_global_mult}.i2z')

        cmds.connectAttr (f'{control.control_name}.footBank', f'{bank_mult}.i1')
        cmds.setAttr (f'{bank_mult}.i2', bank_multFactor)
        cmds.connectAttr (f'{control.control_name}.footBank', f'{bank_condition}.ft')
        cmds.setAttr (f'{bank_condition}.operation',2)
        cmds.connectAttr (f'{bank_mult}.o', f'{reverse_global_mult}.i1x')
        cmds.connectAttr (f'{reverse_global_mult}.ox', f'{bank_condition}.ctr')
        cmds.connectAttr (f'{reverse_global_mult}.ox', f'{bank_condition}.cfg')
        cmds.setAttr (f'{bank_condition}.cfr', 0)
        cmds.setAttr (f'{bank_condition}.ctg', 0)
        cmds.connectAttr (f'{bank_condition}.ocr', f'{bank[0]}.rz')
        cmds.connectAttr (f'{bank_condition}.ocg', f'{bank[1]}.rz')

        roll_mult = cmds.createNode('multDoubleLinear', name = f'{name}_rollReverse_mult')
        roll_forward_mult = cmds.createNode('multDoubleLinear', name = f'{name}_rollForward_mult')
        roll_heel_cond = cmds.createNode('condition', name = f'{name}_rollReverse_heel_cond')
        
        cmds.connectAttr (f'{control.control_name}.footRoll', f'{roll_mult}.i1')
        cmds.setAttr (f'{roll_mult}.i2', 5)
        cmds.connectAttr (f'{control.control_name}.footRoll', f'{roll_forward_mult}.i1')
        cmds.setAttr (f'{roll_forward_mult}.i2', 10)
        
        cmds.setAttr (f'{roll_heel_cond}.operation',2)
        cmds.connectAttr (f'{control.control_name}.footRoll', f'{roll_heel_cond}.ft')

        cmds.connectAttr (f'{roll_forward_mult}.o', f'{reverse_global_mult}.i1y')
        cmds.connectAttr (f'{roll_mult}.o', f'{reverse_global_mult}.i1z')

        cmds.connectAttr (f'{reverse_global_mult}.oy', f'{roll_heel_cond}.ctg')
        cmds.connectAttr (f'{reverse_global_mult}.oz', f'{roll_heel_cond}.cfr')
        cmds.setAttr (f'{roll_heel_cond}.cfg', 0)
        cmds.setAttr (f'{roll_heel_cond}.ctr', 0)

        manual_heel_add = cmds.createNode('addDoubleLinear', name = f'{name}_heelManual_add')
        cmds.connectAttr (f'{roll_heel_cond}.ocr', f'{manual_heel_add}.i1')
        cmds.connectAttr (f'{control.control_name}.heelRot_X', f'{manual_heel_add}.i2')
        cmds.connectAttr (f'{manual_heel_add}.o', f'{reverse_skeleton[0]}.rx')
        cmds.connectAttr (f'{control.control_name}.heelRot_Y', f'{reverse_skeleton[0]}.rz')

        roll_toe_condition = cmds.createNode('condition', name = f'{name}_rollReverse_toe_cond')
        cmds.connectAttr (f'{roll_heel_cond}.ocg', f'{roll_toe_condition}.ft')
        cmds.connectAttr (f'{roll_heel_cond}.ocg', f'{roll_toe_condition}.cfr')
        cmds.setAttr (f'{roll_toe_condition}.operation',2)
        cmds.setAttr (f'{roll_toe_condition}.st',x)
        cmds.setAttr (f'{roll_toe_condition}.cfg',0)

        toe_minus = cmds.createNode('plusMinusAverage', name = f'{name}_rollReverse_toe_SUB' )
        cmds.setAttr (f'{toe_minus}.i1[0]', -x)
        cmds.connectAttr (f'{roll_heel_cond}.ocg', f'{toe_minus}.i1[1]')
        cmds.connectAttr  (f'{toe_minus}.o1', f'{roll_toe_condition}.ctg')

        manual_toe_roll_add = cmds.createNode('addDoubleLinear', name = f'{name}_toeManual_add')
        cmds.connectAttr  (f'{roll_toe_condition}.ocg', f'{manual_toe_roll_add}.i1')
        cmds.connectAttr  (f'{control.control_name}.toeRot_X', f'{manual_toe_roll_add}.i2')
        cmds.connectAttr  (f'{manual_toe_roll_add}.o', f'{reverse_skeleton[1]}.rx')
        cmds.connectAttr (f'{control.control_name}.toeRot_Y', f'{reverse_skeleton[1]}.rz')

        ball_minus = cmds.createNode('plusMinusAverage', name = f'{name}_rollReverse_ball_SUB' )
        ball_add = cmds.createNode('addDoubleLinear', name = f'{name}_rollReverse_ball_Add' )
        cmds.setAttr (f'{ball_minus}.operation', 2)
        cmds.setAttr (f'{ball_minus}.i1[0]', 0)
        cmds.connectAttr (f'{roll_heel_cond}.ocg', f'{ball_minus}.i1[1]')
        cmds.setAttr (f'{ball_add}.i1', 2*x)
        cmds.connectAttr (f'{ball_minus}.o1', f'{ball_add}.i2')
        cmds.connectAttr (f'{ball_add}.o', f'{roll_toe_condition}.ctr')
        cmds.connectAttr (f'{roll_toe_condition}.ocr', f'{reverse_skeleton[2]}.rx')