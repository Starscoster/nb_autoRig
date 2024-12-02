import maya.cmds as cmds
import math
from nb_autoRig_v3 import nb_autorig_v3_get_pivots as get_pv
from nb_autoRig_v3 import nb_autorig_v3_datas as datas
from nb_autoRig_v3 import nb_autorig_v3_matrix_constraints as mat_const
from nb_autoRig_v3 import nb_autorig_v3_controls as ctrl 
from nb_autoRig_v3 import nb_autorig_v3_process as utils

import imp
imp.reload(datas)
imp.reload(get_pv)
imp.reload(mat_const)
imp.reload(ctrl)

############################################################################################################
#                                     Rigging utils functions
############################################################################################################

def add_attr_modules (object_to_add_attribut, attributs_to_add) :
    '''
    This function add a matrix-type attribut to object_to_add_attribut for each element of attributs_to_add
    and connect world matrix to this new attribut
    object_to_add_attribut -> object to add matrix attributs (str)
    attributs_to_add -> list of all attributs name that correspond to a maya object (list)
    Return created attribut list
    '''

    attrList = []

    for group in attributs_to_add :

        if "." in group :
            attribut = group.split(".")[1]
            cmds.addAttr(object_to_add_attribut, at = "matrix", ln = attribut)
            cmds.connectAttr (group, f'{object_to_add_attribut}.{attribut}')
            attrList.append (f'{object_to_add_attribut}.{attribut}')
        else :
            cmds.addAttr(object_to_add_attribut, at = "matrix", ln = group)
            cmds.connectAttr (f'{group}.wm[0]', f'{object_to_add_attribut}.{group}')
            attrList.append (f'{object_to_add_attribut}.{group}')

    return attrList

def connect_modules (outputGroup, inputGroups) :
    '''
    This function connect twomodules groups together by connecting translate, rotate and scale
    '''
    cmds.connectAttr (f'{outputGroup}.t', f'{inputGroups}.t')
    cmds.connectAttr (f'{outputGroup}.r', f'{inputGroups}.r')
    cmds.connectAttr (f'{outputGroup}.s', f'{inputGroups}.s')

def kill_inverse_scale (bone): 

    bones = cmds.listRelatives (bone, ad=True, type = 'joint')
    bones.append (bone)

    for each in bones :
        connectionList = cmds.listConnections (each, type = 'joint')
        connectionAttrList = cmds.listConnections (each, p=True, type = 'joint')

        for attr in connectionAttrList :
            if '.inverseScale' in attr :
                cmds.disconnectAttr (f'{each}.s', f'{connectionList[connectionAttrList.index(attr)]}.is')

def init_module_sequence (module_name) :
    '''
    Create necessaries groups to create a module.
    module_name -> created module naming (str)    
    '''
    msg_init = 'Setting up ' + module_name + ' rig'
    msg_init_len = len(msg_init) + 6
    message  = '\n' + '+'*msg_init_len +'\n' + '++ ' + msg_init + ' ++\n' + '+'*msg_init_len +'\n'

    print (message)

    #create groups
    module_grp = cmds.createNode('transform', name = f'{module_name}_module_{datas.GROUP_naming}')
    public_grp = cmds.createNode('transform', name = f'{module_name}_public_{datas.GROUP_naming}')
    private_grp = cmds.createNode('transform', name = f'{module_name}_private_{datas.GROUP_naming}')
    input_grp = cmds.createNode('transform', name = f'{module_name}_input_{datas.GROUP_naming}')
    output_grp = cmds.createNode('transform', name = f'{module_name}_output_{datas.GROUP_naming}')

    #set outliner color
    cmds.setAttr (f'{public_grp}.useOutlinerColor', True)
    cmds.setAttr (f'{public_grp}.outlinerColor', 0,1,0)
    cmds.setAttr (f'{private_grp}.useOutlinerColor', True)
    cmds.setAttr (f'{private_grp}.outlinerColor', 1,0,0)
    cmds.setAttr (f'{input_grp}.useOutlinerColor', True)
    cmds.setAttr (f'{input_grp}.outlinerColor', 0,1,1)
    cmds.setAttr (f'{output_grp}.useOutlinerColor', True)
    cmds.setAttr (f'{output_grp}.outlinerColor', 0,1,1)

    #parent to module group
    cmds.parent(output_grp,input_grp,private_grp,public_grp,module_grp)

    return input_grp, output_grp, public_grp, private_grp, module_grp

def get_rig_maximum_size (extremities_list) :
    '''
    Get distance between two points
    extremities_list -> two points list (list)
    Return distance
    '''
    obj_A, obj_B = extremities_list
    point_A = cmds.xform(obj_A, q=True, translation = True)
    point_B = cmds.xform(obj_B, q=True, translation = True, worldSpace = True)

    distance_between = math.fabs(point_B[0]+point_A[0])/2 + (point_B[1]+point_A[1])/2 + (point_B[2]+point_A[2])/2
    return distance_between

def get_object_size (object_) :
    '''
    Get object scale in word space
    objects_ -> object to get scale (str)
    Return scale
    '''
    scale = cmds.xform(object_, q=True, scale = True, worldSpace = True)
    scale_average = (scale[0] + scale[1] + scale[2])/3
    return scale_average

def get_relative_distance (point1, point2, factor) :

        coord1 = cmds.xform(point1, q=True, t=True, ws=True)
        coord2= cmds.xform(point2, q=True, t=True, ws=True)

        pointVec = [0,0,0]
        pointVec[0] = (coord2[0] - coord1[0])*factor
        pointVec[1] = (coord2[1] - coord1[1])*factor
        pointVec[2] = (coord2[2] - coord1[2])*factor

        return pointVec

def get_absolute_distance (point1, point2, factor) :

        coord1 = cmds.xform(point1, q=True, t=True, ws=True)
        coord2= cmds.xform(point2, q=True, t=True, ws=True)

        pointVec = [0,0,0]
        pointVec[0] = (coord2[0] - coord1[0])*factor
        pointVec[1] = (coord2[1] - coord1[1])*factor
        pointVec[2] = (coord2[2] - coord1[2])*factor

        finalT = [0,0,0]
        finalT[0] = round(coord1[0] + pointVec[0],5)
        finalT[1] = round(coord1[1] + pointVec[1],5)
        finalT[2] = round(coord1[2] + pointVec[2],5)

        return finalT

############################################################################################################
#                                     Rigging Process functions
############################################################################################################

def create_twist (name, start_bone, end_bone, twist_parent_bone, twist_joint_number, joint_radius, create_curve, curve, scale, orient_axis, orient_vector) :

    #g Create twist joints
    twist_joint_list = create_twist_joint (name, twist_joint_number, joint_radius)

    # If create curve 
    if create_curve == True :
        # Get cvs coord
        points = get_pv.get_bend_points (start_bone, end_bone)
        points = list(points)

        for each in points:
            x=points.index(each)
            res = tuple(map(float, each.split(', ')))
            points[x] = res

        # Create curve with points coord
        crv = cmds.curve(d=3, p=points, name = f'{name}_bend_curve')

        if cmds.objExists ('curveShape1') == True:
            cmds.rename ('curveShape1', f'{crv}Shape') 
    else :
        crv = curve

    # Scale system
    curve_info = cmds.createNode('curveInfo', name = f'{name}_bend_curveInfo')
    mult_node = cmds.createNode('multDoubleLinear', name = f'{name}_bend_ratio')
    scale_node = cmds.createNode('multiplyDivide', name = f'{name}_bend_scale')

    cmds.connectAttr (f'{crv}Shape.local', f'{curve_info}.inputCurve')
    cmds.connectAttr (f'{curve_info}.al', f'{mult_node}.i1')
    ratio = 1 / float (len(twist_joint_list)-1)
    cmds.setAttr(f'{mult_node}.i2', ratio)
    cmds.setAttr ("{}.operation".format(scale_node), 2)
    cmds.connectAttr (f'{mult_node}.o', f'{scale_node}.input1X')
    cmds.connectAttr (scale, f'{scale_node}.input2X')
    cmds.connectAttr (f'{scale_node}.outputX', f'{twist_joint_list[1]}.ty')

    for i in range (1, len(twist_joint_list)-1) :
        cmds.connectAttr (f'{twist_joint_list[i]}.ty', f'{twist_joint_list[i+1]}.ty')

    cmds.parent (twist_joint_list[0], twist_parent_bone)
    cmds.setAttr (f'{twist_joint_list[0]}.translate', *(0,0,0))
    cmds.setAttr (f'{twist_joint_list[0]}.rotate', *(0,0,0))
    cmds.setAttr (f'{twist_joint_list[0]}.jointOrient', *(0,0,0))

    # Create ikspline Handle
    spline_ik = f'{name}_spline_ik'
    eff = f'{name}_eff'
    cmds.ikHandle(sj=twist_joint_list[0], ee = twist_joint_list[len(twist_joint_list)-1], ccv=False, c=crv, name = spline_ik, sol = 'ikSplineSolver', tws = 'linear')
    cmds.rename ('effector1', eff)

    # Twist variables
    if orient_axis == 'X' :
        world_up_axis = 6
    else :
        world_up_axis = 3

    # Twist system
    cmds.setAttr (f'{spline_ik}.dTwistControlEnable', 1)
    cmds.setAttr (f'{spline_ik}.dWorldUpType', 4)
    cmds.setAttr (f'{spline_ik}.dForwardAxis', 2)
    cmds.setAttr (f'{spline_ik}.dWorldUpAxis', world_up_axis)
    cmds.setAttr (f'{spline_ik}.dWorldUpVector', *orient_vector)
    cmds.setAttr (f'{spline_ik}.dWorldUpVectorEnd', *orient_vector)

    cmds.connectAttr (f'{start_bone}.worldMatrix[0]' , f'{spline_ik}.dWorldUpMatrix')
    cmds.connectAttr (f'{end_bone}.worldMatrix[0]' , f'{spline_ik}.dWorldUpMatrixEnd')

    cmds.parent(crv, w=True)

    return crv, spline_ik, eff, twist_joint_list

def create_twist_joint (name, joint, joint_radius):

    jointList = []

    for each in range (joint) :
        cmds.select(d=True)
        twsJnt = cmds.joint (name = f'{name}_twist0{each+1}_jnt', rad = joint_radius)
        jointList.append(twsJnt)

    for x in range (len(jointList)-1) :
        if x != len(jointList)-1:
            cmds.setAttr (f'{jointList[x+1]}.ty', 1)
            cmds.parent(jointList[x+1], jointList[x])
            
    return jointList


 # make ik fk switch, in ik controls, the 3rd index is ik sk switch attibut
def ik_fk_switch (fk_bones_list, ik_bones_list, main_bones_list, fk_control_list, ik_control, arm_settings_control, module_name, visibility_control, do_parent_ik) :

    #connect ik controls with visibility attr
    switch_reverse_node = cmds.createNode('reverse', name = module_name + '_ikfk_rev')
    visibility_mult_node = cmds.createNode('multDoubleLinear', name = module_name + '_ikfk_vis')
    visibility_reverse_mult_node = cmds.createNode('multDoubleLinear', name = module_name + '_ikfk_visRev')
    cmds.connectAttr (f'{visibility_control}.controlVis', f'{visibility_mult_node}.i1')
    cmds.connectAttr (f'{visibility_control}.controlVis', f'{visibility_reverse_mult_node}.i1')
    cmds.connectAttr (f'{arm_settings_control}.ikFkSwitch', f'{visibility_mult_node}.i2')
    cmds.connectAttr (f'{arm_settings_control}.ikFkSwitch', f'{switch_reverse_node}.inputX')
    cmds.connectAttr (f'{switch_reverse_node}.ox', f'{visibility_reverse_mult_node}.i2')
    cmds.connectAttr (f'{visibility_mult_node}.o', f'{ik_control}.visibility')
    
    
    #fk control constrain fk skel and connect visibility
    for each in fk_bones_list : 

        name = each.replace('_ctrl','')
        mat_const.parent(fk_control_list[fk_bones_list.index(each)].control_name, each, False, True, True, True, False, name)
        cmds.connectAttr (f'{visibility_reverse_mult_node}.o', f'{fk_control_list[fk_bones_list.index(each)].control_name}.visibility')
        cmds.setAttr ("{}.jointOrient".format(each), *(0,0,0))

    #get ik bones pv
    ik_pv_locator = module_name + '_pv_' + datas.LOCATOR_naming
    ik_pv = get_pv.find_pivot(ik_bones_list, ik_pv_locator)
    cmds.select(d=True)
    ik_pv_joint = cmds.joint(name = module_name + '_pv_' + datas.JOINT_naming)
    cmds.matchTransform (ik_pv_joint, ik_pv, pos=True, rot=True)
    cmds.delete(ik_pv)

    #freeze rotate of ik bones
    for each in ik_bones_list :
        cmds.makeIdentity(each, apply = True, rotate = True)

    #create ik and ik pv
    ik , ikeff = cmds.ikHandle (ik_bones_list[0],sj=ik_bones_list[0], ee=ik_bones_list[3], sol='ikRPsolver', name= "{}_{}".format(module_name, datas.IK_HANDLE_naming))
    ikeff = "{}_{}".format(module_name, datas.IK_EFFECTOR_naming)
    cmds.rename ('effector1', ikeff)

    cmds.poleVectorConstraint (ik_pv_joint, ik)

    if do_parent_ik == True :
        mat_const.parent(ik_control, ik, False, True, False, False, False, module_name + '_ik')

    #connect ik and fk skeletons to main skel with blendMatrix node. connect settings ik fk switch attr to enveloppe
    for each in range(len(main_bones_list)) :

        naming = main_bones_list[each].replace('_jnt','')

        out_decompose_node = cmds.createNode('decomposeMatrix', name = naming + '_switch_outDecMat')

        mult_nodes_list = []

        for i in [fk_bones_list[each], ik_bones_list[each]] :
            mult_node = cmds.createNode("multMatrix", name = i + '_switch_multMat')
            cmds.connectAttr ("{}.worldMatrix[0]".format(i), "{}.matrixIn[0]".format(mult_node))
            cmds.connectAttr ("{}.parentInverseMatrix[0]".format(main_bones_list[each]), "{}.matrixIn[1]".format(mult_node))
            mult_nodes_list.append(mult_node)

        blend_mat_node = cmds.createNode("blendMatrix", name = naming + '_switch_blendMat')
        cmds.connectAttr ("{}.matrixSum".format(mult_nodes_list[0]), "{}.inputMatrix".format(blend_mat_node))
        cmds.connectAttr ("{}.matrixSum".format(mult_nodes_list[1]), "{}.target[0].targetMatrix".format(blend_mat_node))

        cmds.connectAttr (f'{arm_settings_control}.ikFkSwitch', "{}.target[0].weight".format(blend_mat_node))

        cmds.connectAttr("{}.outputMatrix".format(blend_mat_node), "{}.inputMatrix".format(out_decompose_node))

        cmds.connectAttr (f'{out_decompose_node}.outputTranslate', f'{main_bones_list[each]}.t')
        cmds.connectAttr (f'{out_decompose_node}.outputRotate', f'{main_bones_list[each]}.r')
        cmds.connectAttr (f'{out_decompose_node}.outputScale', f'{main_bones_list[each]}.s')

        cmds.setAttr ("{}.jointOrient".format(main_bones_list[each]), *(0,0,0))

    return ik, ik_pv_joint, visibility_mult_node

#strech function
def strech (start_position, parent_start_strech, parent_end_strech, bones_scale_attribut, settings, naming) :

    initial_translate_1 = cmds.getAttr(f'{bones_scale_attribut[0]}')
    initial_translate_2 = cmds.getAttr(f'{bones_scale_attribut[1]}')

    initial_add = cmds.createNode ('addDoubleLinear', name = f'{naming}_init_add')
    cmds.setAttr (f'{initial_add}.input1', initial_translate_1)
    cmds.setAttr (f'{initial_add}.input2', initial_translate_2)

    first_strech_group = cmds.createNode ('transform', name = f'{naming}_first_strech_grp')
    last_strech_group = cmds.createNode ('transform', name = f'{naming}_last_strech_grp')
    cmds.matchTransform (first_strech_group, start_position, pos=True, rot = True)
    mat_const.parent (parent_start_strech, first_strech_group, True, True, False, False, False, f'{naming}_first_Strech')
    mat_const.parent (parent_end_strech, last_strech_group, False, True, False, False, False, f'{naming}_last_Strech')

    distance_node = cmds.createNode ('distanceBetween', name = f'{naming}_dist')
    cmds.connectAttr(f'{first_strech_group}.t', f'{distance_node}.point1')
    cmds.connectAttr(f'{last_strech_group}.t', f'{distance_node}.point2')
    
    mult_div_node = cmds.createNode ('multiplyDivide', name = f'{naming}_strechDist')
    cmds.connectAttr (f'{initial_add}.input1', f'{mult_div_node}.input1X')
    cmds.connectAttr (f'{initial_add}.input2', f'{mult_div_node}.input1Y')
    cmds.connectAttr (f'{initial_add}.output', f'{mult_div_node}.input1Z')

    ratio_mult_div_node = cmds.createNode ('multiplyDivide', name = f'{naming}_distRatio')
    cmds.connectAttr (f'{mult_div_node}.outputZ', f'{ratio_mult_div_node}.input2X')
    cmds.connectAttr (f'{distance_node}.distance', f'{ratio_mult_div_node}.input1X')
    cmds.setAttr (f'{ratio_mult_div_node}.operation', 2)

    strech_value_mult = cmds.createNode ('multiplyDivide', name = f'{naming}_strech_value_mult')
    cmds.connectAttr (f'{ratio_mult_div_node}.outputX', f'{strech_value_mult}.input1X')
    cmds.connectAttr (f'{ratio_mult_div_node}.outputX', f'{strech_value_mult}.input1Y')
    cmds.connectAttr (f'{initial_add}.input1', f'{strech_value_mult}.input2X')
    cmds.connectAttr (f'{initial_add}.input2', f'{strech_value_mult}.input2Y')

    strech_switch_mult = cmds.createNode ('multDoubleLinear', name = f'{naming}_strech_switch_mult')
    cmds.connectAttr (f'{distance_node}.distance', f'{strech_switch_mult}.input1')
    cmds.connectAttr (f'{settings}', f'{strech_switch_mult}.input2')

    strech_condition = cmds.createNode('condition', name = f'{naming}_strech_condition')
    cmds.connectAttr (f'{initial_add}.input1', f'{strech_condition}.colorIfFalse.colorIfFalseR')
    cmds.connectAttr (f'{initial_add}.input2', f'{strech_condition}.colorIfFalse.colorIfFalseG')
    cmds.connectAttr (f'{strech_value_mult}.outputX', f'{strech_condition}.colorIfTrue.colorIfTrueR')
    cmds.connectAttr (f'{strech_value_mult}.outputY', f'{strech_condition}.colorIfTrue.colorIfTrueG')
    cmds.connectAttr (f'{strech_switch_mult}.output', f'{strech_condition}.firstTerm')
    cmds.connectAttr (f'{mult_div_node}.outputZ', f'{strech_condition}.secondTerm')
    cmds.setAttr(f'{strech_condition}.operation', 2)

    cmds.connectAttr (f'{strech_condition}.outColor.outColorR', bones_scale_attribut[0])
    cmds.connectAttr (f'{strech_condition}.outColor.outColorG', bones_scale_attribut[1])

    return [f'{mult_div_node}.input2X', f'{mult_div_node}.input2Y', f'{mult_div_node}.input2Z'], [first_strech_group, last_strech_group]

#shoulder aux jnt
def shoulder_aux (name, bones) :

    auxJntList = []

    for each in bones[1], bones[2] :
        auxJnt = cmds.duplicate(each, name = each.replace('_jnt', '_aux_jnt'), po=True)
        auxJntList.append(auxJnt[0])
    
    cmds.parent (auxJntList[1], auxJntList[0])
    cmds.setAttr (f'{auxJntList[1]}.jointOrientX', 0)
    cmds.setAttr (f'{auxJntList[1]}.jointOrientY', 0)
    cmds.setAttr (f'{auxJntList[1]}.jointOrientZ', 0)

    ik = cmds.ikHandle (sj= auxJntList[0], ee= auxJntList[1], name = f'{name}_ik', sol= 'ikRPsolver' )
    cmds.rename ('effector1', f'{name}_eff')

    pv = cmds.spaceLocator (name = f'{name}_pv')
    cmds.matchTransform (pv, bones[1], pos=True, rot = True)
    cmds.parent (f'{name}_ik', bones[2])
    cmds.poleVectorConstraint (pv, f'{name}_ik' )    

    return auxJntList, ik, pv 

def half_rotate_joint (parent_joints) :

    cmds.select(d=True)

    half_joint = cmds.joint(name = parent_joints.replace('_jnt', '_hRot_jnt'))
    cmds.matchTransform (half_joint, parent_joints, rot=True, pos=True)
    
    parent_joint = cmds.listRelatives(parent_joints, p=True)

    cmds.parent (half_joint, parent_joint)

    half_mult = cmds.createNode ('multiplyDivide', name = parent_joints.replace('_jnt', '_hRot_mplt'))
    cmds.connectAttr (f'{parent_joints}.r', f'{half_mult}.i1')
    cmds.setAttr (f'{half_mult}.i2x', .5)
    cmds.setAttr (f'{half_mult}.i2y', .5)
    cmds.setAttr (f'{half_mult}.i2z', .5)

    cmds.connectAttr (f'{half_mult}.o', f'{half_joint}.r')
    cmds.connectAttr (f'{parent_joints}.jo', f'{half_joint}.jo')

    cmds.connectAttr("{}.translate".format(parent_joints), "{}.translate".format(half_joint))

    return half_joint

#bend function
def bend (naming, curve, target_bones, bendColor, visual_settings, settings, joint_radius, bounding_boxs) :

    bend_joint_list = [f'{naming}_start_{datas.JOINT_naming}', f'{naming}_start_tan_{datas.JOINT_naming}', f'{naming}_bend_{datas.JOINT_naming}', f'{naming}_end_tan_{datas.JOINT_naming}', f'{naming}_end_{datas.JOINT_naming}']

    middle_bend_control = ctrl.ControlObj(bend_joint_list[2].replace(datas.JOINT_naming, datas.CONTROL_naming),
                                      'Square', 
                                      'Blue', 
                                      get_object_size(bounding_boxs[2]))
    cmds.matchTransform(middle_bend_control.control_name, target_bones[1])
    mat_const.parent(target_bones[1], middle_bend_control.control_name, False, True, True, True, True, f'{naming}_bend')
    middle_bend_joint = cmds.joint (name =  bend_joint_list[2], rad = joint_radius)
    mat_const.parent(middle_bend_control.control_name, middle_bend_joint, False, True, True, True, False, f'{middle_bend_control.control_name}_jointBend')

    viibility_mult_node = cmds.createNode('multDoubleLinear', name = f'{naming}_vis_mult')
    settings.add_attribut('bool', 'bendVis', ('',''), False, '')
    cmds.connectAttr (f'{visual_settings.control_name}.controlVis', f'{viibility_mult_node}.i1')
    cmds.connectAttr (f'{settings.control_name}.bendVis', f'{viibility_mult_node}.i2')

    cmds.connectAttr (f'{viibility_mult_node}.o', f'{middle_bend_control.control_name}.visibility')

    firest_bend_joint, firest_offset_group = bend_function (target_bones[0], middle_bend_joint, f'{naming}_bend01', bendColor, viibility_mult_node, curve[0], middle_bend_control.control_name, 1, joint_radius, bounding_boxs)
    second_bend_joint, second_offset_group = bend_function (middle_bend_joint, target_bones[2], f'{naming}_bend02', bendColor, viibility_mult_node, curve[1], middle_bend_control.control_name, -1, joint_radius, bounding_boxs)

    for list in [firest_bend_joint, second_bend_joint] :
        for elem in list :
            if target_bones[0] in elem or target_bones[1] in elem or target_bones[2] in elem :
                list.pop(list.index(elem))

    return [firest_offset_group, second_offset_group], middle_bend_control, firest_bend_joint+second_bend_joint

def bend_function (start_joint, end_joint, naming, color, visibility_node, crv, middle_bend_control, primary_axe_y, joint_radius, bounding_boxs) :

    offset_group = cmds.createNode('transform', name = f'{naming}_buff')
    offset_decompose_matrix = cmds.createNode('decomposeMatrix', name = f'{naming}_dec')

    bend_joint_list = []

    mat_const.blend(f'{start_joint}.wm[0]', [f'{end_joint}.wm[0]'], [(1,0,0)], .5, f'{offset_decompose_matrix}.inputMatrix', naming)
    cmds.connectAttr (f'{offset_decompose_matrix}.ot', f'{offset_group}.t')
    cmds.connectAttr (f'{offset_decompose_matrix}.os', f'{offset_group}.s')

    bend_control = ctrl.ControlObj("{}_{}".format(naming, datas.CONTROL_naming),
                                      'Square', 
                                      color, 
                                      get_object_size(bounding_boxs[1]))
    cmds.matchTransform(bend_control.control_name, offset_group)
    cmds.select(d=True)
    bend_joint = cmds.joint (name =  "{}_{}".format(naming, datas.JOINT_naming), rad = joint_radius)
    mat_const.parent (bend_control.control_name, bend_joint, False, True, True, True, False, naming)
    cmds.parent (bend_control.control_name, offset_group)
    cmds.connectAttr (f'{visibility_node}.o', f'{bend_control.control_name}.visibility')

    bend_control.add_attribut('double', 'InTan', (0.1,9.9), 5, '')
    bend_control.add_attribut('double', 'OutTan', (0.1,9.9), 5, '')

    attribut_mult = cmds.createNode('multiplyDivide', name = f'{naming}_ratio_mult')

    bend_tangeat_attributs = [f'{attribut_mult}.ox', f'{attribut_mult}.oy']

    cmds.connectAttr (f'{bend_control.control_name}.InTan', f'{attribut_mult}.i1x')
    cmds.connectAttr (f'{bend_control.control_name}.OutTan', f'{attribut_mult}.i1y')

    cmds.setAttr (f'{attribut_mult}.i2x', .1)
    cmds.setAttr (f'{attribut_mult}.i2y', .1)

    tangeant_index = 0

    bend_joint_list.append(start_joint)

    for control in [[start_joint, bend_control.control_name], [bend_control.control_name, end_joint]]:

        if '_{}'.format(datas.CONTROL_naming) in control[0] :
            tangeant_joint_name = control[0].replace('_{}'.format(datas.CONTROL_naming),'_tan_{}'.format(datas.JOINT_naming))
        elif '_{}'.format(datas.JOINT_naming) in control[0] :
            tangeant_joint_name = control[0].replace('_{}'.format(datas.JOINT_naming),'_tan_{}'.format(datas.JOINT_naming))

        tangeant_joint = cmds.joint(name = tangeant_joint_name, rad = joint_radius)
        tangeant_decompose_mat = cmds.createNode('decomposeMatrix', name = tangeant_joint.replace('_{}'.format(datas.JOINT_naming),'_dec'))
        cmds.connectAttr (f'{tangeant_decompose_mat}.ot',f'{tangeant_joint}.t')
        mat_const.blend(f'{control[0]}.wm[0]', [f'{control[1]}.wm[0]'], [(1,0,0)], bend_tangeat_attributs[tangeant_index], f'{tangeant_decompose_mat}.imat', tangeant_joint_name.replace('_{}'.format(datas.JOINT_naming),''))

        bend_joint_list.append(tangeant_joint)

        if tangeant_index == 0 :
            bend_joint_list.append (bend_joint)

        tangeant_index += 1

    bend_joint_list.append (end_joint)

    bend_skin_name = bend_joint.replace('_{}'.format(datas.JOINT_naming),'_skin')
    bend_skin = cmds.skinCluster(bend_joint_list, crv, mi = 1, name = bend_skin_name, wd = 0, ih = True, sm = 0, tsb=True)[0]
    if cmds.objExists("bindPose1") :
            cmds.rename("bindPose1", bend_skin_name.replace("_skin", "_bindPose"))
    for x in range(len(bend_joint_list)) :
        cmds.skinPercent( bend_skin, f'{crv}.cv[{x}]', transformValue=(bend_joint_list[x], 1))


    mat_const.aim(middle_bend_control, bend_control.control_name, offset_group, middle_bend_control, [0,primary_axe_y,0], [1,0,0], [1,0,0], True, bend_control.control_name.replace('{}'.format(datas.CONTROL_naming), 'aim_cons'))

    return bend_joint_list, offset_group

def parent_space (target_control, trigger_control, name, settings, mode) :

    enumList = ''
    targetList = []
    for each in trigger_control : 
        enumList += f':{each}'
        targetList.append (trigger_control[each])
    
    enumList = enumList[1:]

    settings.add_attribut('enum', 'parentSpace', ("",""), 0, enumList)
    blend_node = cmds.createNode('blendMatrix', name = name + '_blendMat')
    mult_node_list = []

    for each in trigger_control :
        choice_node = cmds.createNode ('choice', name = f'{name}_{each}_choice')

        for x in range (len(targetList)) :
            if x == targetList.index(trigger_control[each]) :
                cmds.setAttr (f'{choice_node}.input[{x}]', 1)
            else : 
                cmds.setAttr (f'{choice_node}.input[{x}]', 0)
        
        cmds.connectAttr (f'{settings.control_name}.parentSpace', f'{choice_node}.s')
        offset = mat_const.getOffset (trigger_control[each], target_control.control_name, f'{name}_{each}_offset')

        mult_node = cmds.createNode('multMatrix', name = f'{name}_{each}_multMat')
        mult_node_list.append(mult_node)
        cmds.connectAttr (f'{offset}.omat', f'{mult_node}.i[0]')
        cmds.connectAttr (trigger_control[each], f'{mult_node}.i[1]')

        if trigger_control[each] == targetList[0] :

            cmds.connectAttr (f'{mult_node}.o', f'{blend_node}.inputMatrix')

        else : 

            cmds.connectAttr (f'{choice_node}.o', f'{blend_node}.target[{targetList.index(trigger_control[each])}].weight')
            cmds.connectAttr (f'{mult_node}.o', f'{blend_node}.target[{targetList.index(trigger_control[each])}].tmat')

    if mode == 'fk' :

        rot_blend_node = cmds.createNode('blendMatrix', name = name + '_fkRot_blendMat')
        cmds.connectAttr (f'{blend_node}.omat', f'{rot_blend_node}.inputMatrix')
        cmds.connectAttr (f'{mult_node_list[-1]}.o', f'{rot_blend_node}.target[0].tmat')
        cmds.setAttr (f'{rot_blend_node}.target[0].rot', 0)
        cmds.connectAttr (f'{rot_blend_node}.omat', f'{target_control.control_name}.opm')
        
    else :
        cmds.connectAttr (f'{blend_node}.omat', f'{target_control.control_name}.opm')

    cmds.setAttr (f'{target_control.control_name}.t', *(0,0,0))
    cmds.setAttr (f'{target_control.control_name}.r', *(0,0,0))