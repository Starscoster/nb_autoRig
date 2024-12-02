import maya.api.OpenMaya as om
from maya import cmds

def find_pivot (bonesList, locname):

    first_pos = om.MVector (cmds.xform(bonesList[0], q=True, rp=True, ws=True) )
    middle_pos = om.MVector (cmds.xform(bonesList[1], q=True, rp=True, ws=True) )
    last_pos = om.MVector (cmds.xform(bonesList[2], q=True, rp=True, ws=True) )

    first_to_last = last_pos - first_pos
    first_to_last_scaled = first_to_last/2
    mid_point = first_pos + first_to_last_scaled

    mid_point_to_middle_vec = middle_pos-mid_point
    mid_point_to_middle_vec_scaled = mid_point_to_middle_vec*4
    poleVector_pos = mid_point_to_middle_vec_scaled + mid_point

    pv_loc = cmds.spaceLocator(a=True, name = locname)
    cmds.parentConstraint (bonesList[1], pv_loc)
    cmds.delete(locname + '_parentConstraint1' ) 
    cmds.xform (locname, t= poleVector_pos)

    return pv_loc

def get_bend_points (start, end) :

    first_pos = om.MVector (cmds.xform(start, q=True, rp=True, ws=True) )
    last_pos = om.MVector (cmds.xform(end, q=True, rp=True, ws=True) )

    distance = last_pos - first_pos
    point1 = distance*0.25 + first_pos
    point2 = distance*0.5 + first_pos
    point3 = distance*0.75 + first_pos

    point0 = str(first_pos).strip('(')
    point1 = str(point1).strip('(')
    point2 = str(point2).strip('(')
    point3 = str(point3).strip('(')
    point4 = str(last_pos).strip('(')

    return str(point0).strip(')'), str(point1).strip(')'), str(point2).strip(')'), str(point3).strip(')'), str(point4).strip(')')