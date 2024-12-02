##################################################################################################
#                            Min max toes and finger transform values
##################################################################################################

minimum_toes_L_setup = [5.36, 2.626, 13.562]
maximum_toes_L_setup = [14.048, 2.626, 13.562]
minimum_toes_R_setup = [-14.048, 2.626, 13.562]
maximum_toes_R_setup = [-5.36, 2.626, 13.562]

minimum_hands_L_setup = [[70.889,140,4.718],[78.963,140,4.718],[84.173,140,4.718],[89.3,140,4.718],[93.338,140,4.718]]
maximum_hands_L_setup = [[70.889,140,-5.954],[78.963,140,-5.954],[84.173,140,-5.954],[89.3,140,-5.954],[93.338,140,-5.954]]
minimum_hands_R_setup = [[-70.889,140,4.718],[-78.963,140,4.718],[-84.173,140,4.718],[-89.3,140,4.718],[-93.338,140,4.718]]
maximum_hands_R_setup = [[-70.889,140,-5.954],[-78.963,140,-5.954],[-84.173,140,-5.954],[-89.3,140,-5.954],[-93.338,140,-5.954]]

##################################################################################################
#                                          Naming Rules
##################################################################################################

biped_hand_foot_naming = ['thumb', 'index', 'middle', 'ring', 'little']
toes_naming = 'toe'
foot_naming = 'foot'
finger_thumb_naming = 'thumb'

PLACE_LOCATOR_naming = "place_locator"
BOUNDING_BOX_naming = "boundBox"

GROUP_naming = "grp"
JOINT_naming = "jnt"
CONTROL_naming = "ctrl"
LOCATOR_naming = "loc"
IK_HANDLE_naming = "ik_handle"
IK_EFFECTOR_naming = "ik_eff"

LEFT_naming = 'L'
RIGHT_naming = 'R'

class InitDatas : 
    '''
    This class contains all joint starting position
    '''
    def __init__ (self) :

        self.spine_setup_datas = {
            'spine_01' : {
                'name' : 'spine_01',
                'position' : (0,85,0),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : None,
                'miror_target' : False,
                'bouding_sphere' : {'spine_01' : (0,0,0)}
            },
            'spine_02' : {
                'name' : 'spine_02',
                'position' : (0,95,0),
                'joint_to_parent' : ['self','spine_01'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','spine_01'],
                'miror_target' : False,
                'bouding_sphere' : {'spine_02' : (0,0,0)}
            },
            'spine_03' : {
                'name' : 'spine_03',
                'position' : (0,106,0),
                'joint_to_parent' : ['self','spine_02'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','spine_02'],
                'miror_target' : False,
                'bouding_sphere' : {'spine_03' : (0,0,0)}
            },
            'spine_04' : {
                'name' : 'spine_04',
                'position' : (0,127.5,0),
                'joint_to_parent' : ['self','spine_03'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','spine_03'],
                'miror_target' : False,
                'bouding_sphere' : {'spine_04' : (0,0,0)}
            },
            'spine_05' : {
                'name' : 'spine_05',
                'position' : (0,140,0),
                'joint_to_parent' : ['self','spine_04'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','spine_04'],
                'miror_target' : False,
                'bouding_sphere' : {}
            },
        }
##################################################################################################
        self.neck_setup_datas = {
            'neck_01' : {
                'name' : 'neck_01',
                'position' : (0,142,0),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['spine',-1],
                'miror_target' : False,
                'bouding_sphere' : {'neck_01' : (0,0,0)}
            },
            'neck_02' : {
                'name' : 'neck_02',
                'position' : (0,148,0),
                'joint_to_parent' : ['self','neck_01'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','neck_01'],
                'miror_target' : False,
                'bouding_sphere' : {'neck_02' : (0,0,0)}
            },
            'neck_03' : {
                'name' : 'neck_03',
                'position' : (0,154,0),
                'joint_to_parent' : ['self','neck_02'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','neck_02'],
                'miror_target' : False,
                'bouding_sphere' : {}
            },
        }
##################################################################################################
        self.head_setup_datas = {
            'head' : {
                'name' : 'head',
                'position' : (0,156.442,0),
                'joint_to_parent' : None,
                'do_not_aim' : True,
                'locator_to_parent' : ['neck',-1],
                'miror_target' : False,
                'bouding_sphere' : {'head' : (0,0,0)}
            },
            'eye_L' : {
                'name' : 'eye_{}'.format(LEFT_naming),
                'position' : (7.445,156.442,13.309),
                'joint_to_parent' : ['self','head'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','head'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            'eye_R' : {
                'name' : 'eye_{}'.format(RIGHT_naming),
                'position' : (-7.445,156.442,13.309),
                'joint_to_parent' : ['self','head'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','head'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
        }
##################################################################################################
        self.arm_L_setup_datas = {
            'clavicle_L' : {
                'name' : 'clavicle_{}'.format(LEFT_naming),
                'position' : (5.946,140,0),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['spine',-1],
                'miror_target' : True,
                'bouding_sphere' : {'clavicle_L' : (0,0,0)}
            },
            'shoulder_L' : {
                'name' : 'shoulder_{}'.format(LEFT_naming),
                'position' : (21.191,140,0),
                'joint_to_parent' : ['self','clavicle_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','clavicle_L'],
                'miror_target' : True,
                'bouding_sphere' : {'shoulder_L' : (0,0,0), 'shoulder_L_bend' : (0,12.442,0)}
            },
            'elbow_L' : {
                'name' : 'elbow_{}'.format(LEFT_naming),
                'position' : (46.089,140,-4.084),
                'joint_to_parent' : ['self','shoulder_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','shoulder_L'],
                'miror_target' : True,
                'bouding_sphere' : {'elbow_L' : (0,0,0), 'elbow_L_bend' : (0,10.631,0)}
            },
            'wrist_L' : {
                'name' : 'wrist_{}'.format(LEFT_naming),
                'position' : (66.925,140,0),
                'joint_to_parent' : ['self','elbow_L'],
                'do_not_aim' : 'parent',
                'locator_to_parent' : ['self','elbow_L'],
                'miror_target' : True,
                'bouding_sphere' : {'wrist_L' : (0,0,0)}
            },
        }
##################################################################################################
        self.arm_R_setup_datas = {
            'clavicle_R' : {
                'name' : 'clavicle_{}'.format(RIGHT_naming),
                'position' : (-5.946,140,0),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['spine',-1],
                'miror_target' : True,
                'bouding_sphere' : {'clavicle_R' : (0,0,0)}
            },
            'shoulder_R' : {
                'name' : 'shoulder_{}'.format(RIGHT_naming),
                'position' : (-21.191,140,0),
                'joint_to_parent' : ['self','clavicle_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','clavicle_R'],
                'miror_target' : True,
                'bouding_sphere' : {'shoulder_R' : (0,0,0), 'shoulder_R_bend' : (0,12.442,0)}
            },
            'elbow_R' : {
                'name' : 'elbow_{}'.format(RIGHT_naming),
                'position' : (-46.089,140,-4.084),
                'joint_to_parent' : ['self','shoulder_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','shoulder_R'],
                'miror_target' : True,
                'bouding_sphere' : {'elbow_R' : (0,0,0), 'elbow_R_bend' : (0,10.631,0)}
            },
            'wrist_R' : {
                'name' : 'wrist_{}'.format(RIGHT_naming),
                'position' : (-66.925,140,0),
                'joint_to_parent' : ['self','elbow_R'],
                'do_not_aim' : "parent",
                'locator_to_parent' : ['self','elbow_R'],
                'miror_target' : True,
                'bouding_sphere' : {'wrist_R' : (0,0,0)}
            },
        }
##################################################################################################        
        self.hand_L_setup_datas = {
             'meta_thumb_L' : {
                'name' : 'meta_thumb_{}'.format(LEFT_naming),
                'position' : (68.369,140,5.884),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['arm__L',-1],
                'miror_target' : True,
                'bouding_sphere' : {'meta_thumb_L' : (0,0,0)}
            },
            'thumb_01_L' : {
                'name' : 'thumb_01_{}'.format(LEFT_naming),
                'position' : (68.369,140,10.707),
                'joint_to_parent' : ['self','meta_thumb_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','meta_thumb_L'],
                'miror_target' : True,
                'bouding_sphere' : {'thumb_01_L' : (0,0,0)}
            },
            'thumb_02_L' : {
                'name' : 'thumb_02_{}'.format(LEFT_naming),
                'position' : (68.369,140,15.397),
                'joint_to_parent' : ['self','thumb_01_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','thumb_01_L'],
                'miror_target' : True,
                'bouding_sphere' : {'thumb_02_L' : (0,0,0)}
            },
            'thumb_tip_L' : {
                'name' : 'thumb_tip_{}'.format(LEFT_naming),
                'position' : (68.369,140,20.01),
                'joint_to_parent' : ['self','thumb_02_L'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','thumb_02_L'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            ##################################################################################################
             'meta_index_L' : {
                'name' : 'meta_index_{}'.format(LEFT_naming),
                'position' : (70.889,140,4.718),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['arm__L',-1],
                'miror_target' : True,
                'bouding_sphere' : {'meta_index_L' : (0,0,0)}
            },
            'index_01_L' : {
                'name' : 'index_01_{}'.format(LEFT_naming),
                'position' : (78.963,140,4.718),
                'joint_to_parent' : ['self','meta_index_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','meta_index_L'],
                'miror_target' : True,
                'bouding_sphere' : {'index_01_L' : (0,0,0)}
            },
            'index_02_L' : {
                'name' : 'index_02_{}'.format(LEFT_naming),
                'position' : (84.173,140,4.718),
                'joint_to_parent' : ['self','index_01_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','index_01_L'],
                'miror_target' : True,
                'bouding_sphere' : {'index_02_L' : (0,0,0)}
            },
            'index_03_L' : {
                'name' : 'index_03_{}'.format(LEFT_naming),
                'position' : (89.3,140,4.718),
                'joint_to_parent' : ['self','index_02_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','index_02_L'],
                'miror_target' : True,
                'bouding_sphere' : {'index_03_L' : (0,0,0)}
            },
            'index_tip_L' : {
                'name' : 'index_tip_{}'.format(LEFT_naming),
                'position' : (93.338,140,4.718),
                'joint_to_parent' : ['self','index_03_L'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','index_03_L'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            ##################################################################################################
             'meta_middle_L' : {
                'name' : 'meta_middle_{}'.format(LEFT_naming),
                'position' : (70.889,140,1.205),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['arm__L',-1],
                'miror_target' : True,
                'bouding_sphere' : {'meta_middle_L' : (0,0,0)}
            },
            'middle_01_L' : {
                'name' : 'middle_01_{}'.format(LEFT_naming),
                'position' : (78.963,140,1.205),
                'joint_to_parent' : ['self','meta_middle_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','meta_middle_L'],
                'miror_target' : True,
                'bouding_sphere' : {'middle_01_L' : (0,0,0)}
            },
            'middle_02_L' : {
                'name' : 'middle_02_{}'.format(LEFT_naming),
                'position' : (84.173,140,1.205),
                'joint_to_parent' : ['self','middle_01_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','middle_01_L'],
                'miror_target' : True,
                'bouding_sphere' : {'middle_02_L' : (0,0,0)}
            },
            'middle_03_L' : {
                'name' : 'middle_03_{}'.format(LEFT_naming),
                'position' : (89.3,140,1.205),
                'joint_to_parent' : ['self','middle_02_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','middle_02_L'],
                'miror_target' : True,
                'bouding_sphere' : {'middle_03_L' : (0,0,0)}
            },
            'middle_tip_L' : {
                'name' : 'middle_tip_{}'.format(LEFT_naming),
                'position' : (93.338,140,1.205),
                'joint_to_parent' : ['self','middle_03_L'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','middle_03_L'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            ##################################################################################################
             'meta_ring_L' : {
                'name' : 'meta_ring_{}'.format(LEFT_naming),
                'position' : (70.889,140,-2.177),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['arm__L',-1],
                'miror_target' : True,
                'bouding_sphere' : {'meta_ring_L' : (0,0,0)}
            },
            'ring_01_L' : {
                'name' : 'ring_01_{}'.format(LEFT_naming),
                'position' : (78.963,140,-2.177),
                'joint_to_parent' : ['self','meta_ring_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','meta_ring_L'],
                'miror_target' : True,
                'bouding_sphere' : {'ring_01_L' : (0,0,0)}
            },
            'ring_02_L' : {
                'name' : 'ring_02_{}'.format(LEFT_naming),
                'position' : (84.173,140,-2.177),
                'joint_to_parent' : ['self','ring_01_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','ring_01_L'],
                'miror_target' : True,
                'bouding_sphere' : {'ring_02_L' : (0,0,0)}
            },
            'ring_03_L' : {
                'name' : 'ring_03_{}'.format(LEFT_naming),
                'position' : (89.3,140,-2.177),
                'joint_to_parent' : ['self','ring_02_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','ring_02_L'],
                'miror_target' : True,
                'bouding_sphere' : {'ring_03_L' : (0,0,0)}
            },
            'ring_tip_L' : {
                'name' : 'ring_tip_{}'.format(LEFT_naming),
                'position' : (93.338,140,-2.177),
                'joint_to_parent' : ['self','ring_03_L'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','ring_03_L'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            ##################################################################################################
             'meta_little_L' : {
                'name' : 'meta_little_{}'.format(LEFT_naming),
                'position' : (70.889,140,-5.954),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['arm__L',-1],
                'miror_target' : True,
                'bouding_sphere' : {'meta_little_L' : (0,0,0)}
            },
            'little_01_L' : {
                'name' : 'little_01_{}'.format(LEFT_naming),
                'position' : (78.963,140,-5.954),
                'joint_to_parent' : ['self','meta_little_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','meta_little_L'],
                'miror_target' : True,
                'bouding_sphere' : {'little_01_L' : (0,0,0)}
            },
            'little_02_L' : {
                'name' : 'little_02_{}'.format(LEFT_naming),
                'position' : (84.173,140,-5.954),
                'joint_to_parent' : ['self','little_01_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','little_01_L'],
                'miror_target' : True,
                'bouding_sphere' : {'little_02_L' : (0,0,0)}
            },
            'little_03_L' : {
                'name' : 'little_03_{}'.format(LEFT_naming),
                'position' : (89.3,140,-5.954),
                'joint_to_parent' : ['self','little_02_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','little_02_L'],
                'miror_target' : True,
                'bouding_sphere' : {'little_03_L' : (0,0,0)}
            },
            'little_tip_L' : {
                'name' : 'little_tip_{}'.format(LEFT_naming),
                'position' : (93.338,140,-5.954),
                'joint_to_parent' : ['self','little_03_L'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','little_03_L'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
        }
##################################################################################################
        self.hand_R_setup_datas = {
             'meta_thumb_R' : {
                'name' : 'meta_thumb_{}'.format(RIGHT_naming),
                'position' : (-68.369,140,5.884),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['arm__R',-1],
                'miror_target' : True,
                'bouding_sphere' : {'meta_thumb_R' : (0,0,0)}
            },
            'thumb_01_R' : {
                'name' : 'thumb_01_{}'.format(RIGHT_naming),
                'position' : (-68.369,140,10.707),
                'joint_to_parent' : ['self','meta_thumb_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','meta_thumb_R'],
                'miror_target' : True,
                'bouding_sphere' : {'thumb_01_R' : (0,0,0)}
            },
            'thumb_02_R' : {
                'name' : 'thumb_02_{}'.format(RIGHT_naming),
                'position' : (-68.369,140,15.397),
                'joint_to_parent' : ['self','thumb_01_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','thumb_01_R'],
                'miror_target' : True,
                'bouding_sphere' : {'thumb_02_R' : (0,0,0)}
            },
            'thumb_tip_R' : {
                'name' : 'thumb_tip_{}'.format(RIGHT_naming),
                'position' : (-68.369,140,20.01),
                'joint_to_parent' : ['self','thumb_02_R'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','thumb_02_R'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            ##################################################################################################
             'meta_index_R' : {
                'name' : 'meta_index_{}'.format(RIGHT_naming),
                'position' : (-70.889,140,4.718),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['arm__R',-1],
                'miror_target' : True,
                'bouding_sphere' : {'meta_index_R' : (0,0,0)}
            },
            'index_01_R' : {
                'name' : 'index_01_{}'.format(RIGHT_naming),
                'position' : (-78.963,140,4.718),
                'joint_to_parent' : ['self','meta_index_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','meta_index_R'],
                'miror_target' : True,
                'bouding_sphere' : {'index_01_R' : (0,0,0)}
            },
            'index_02_R' : {
                'name' : 'index_02_{}'.format(RIGHT_naming),
                'position' : (-84.173,140,4.718),
                'joint_to_parent' : ['self','index_01_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','index_01_R'],
                'miror_target' : True,
                'bouding_sphere' : {'index_02_R' : (0,0,0)}
            },
            'index_03_R' : {
                'name' : 'index_03_{}'.format(RIGHT_naming),
                'position' : (-89.3,140,4.718),
                'joint_to_parent' : ['self','index_02_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','index_02_R'],
                'miror_target' : True,
                'bouding_sphere' : {'index_03_R' : (0,0,0)}
            },
            'index_tip_R' : {
                'name' : 'index_tip_{}'.format(RIGHT_naming),
                'position' : (-93.338,140,4.718),
                'joint_to_parent' : ['self','index_03_R'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','index_03_R'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            ##################################################################################################
             'meta_middle_R' : {
                'name' : 'meta_middle_{}'.format(RIGHT_naming),
                'position' : (-70.889,140,1.205),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['arm__R',-1],
                'miror_target' : True,
                'bouding_sphere' : {'meta_middle_R' : (0,0,0)}
            },
            'middle_01_R' : {
                'name' : 'middle_01_{}'.format(RIGHT_naming),
                'position' : (-78.963,140,1.205),
                'joint_to_parent' : ['self','meta_middle_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','meta_middle_R'],
                'miror_target' : True,
                'bouding_sphere' : {'middle_01_R' : (0,0,0)}
            },
            'middle_02_R' : {
                'name' : 'middle_02_{}'.format(RIGHT_naming),
                'position' : (-84.173,140,1.205),
                'joint_to_parent' : ['self','middle_01_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','middle_01_R'],
                'miror_target' : True,
                'bouding_sphere' : {'middle_02_R' : (0,0,0)}
            },
            'middle_03_R' : {
                'name' : 'middle_03_{}'.format(RIGHT_naming),
                'position' : (-89.3,140,1.205),
                'joint_to_parent' : ['self','middle_02_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','middle_02_R'],
                'miror_target' : True,
                'bouding_sphere' : {'middle_03_R' : (0,0,0)}
            },
            'middle_tip_R' : {
                'name' : 'middle_tip_{}'.format(RIGHT_naming),
                'position' : (-93.338,140,1.205),
                'joint_to_parent' : ['self','middle_03_R'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','middle_03_R'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            ##################################################################################################
             'meta_ring_R' : {
                'name' : 'meta_ring_{}'.format(RIGHT_naming),
                'position' : (-70.889,140,-2.177),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['arm__R',-1],
                'miror_target' : True,
                'bouding_sphere' : {'meta_ring_R' : (0,0,0)}
            },
            'ring_01_R' : {
                'name' : 'ring_01_{}'.format(RIGHT_naming),
                'position' : (-78.963,140,-2.177),
                'joint_to_parent' : ['self','meta_ring_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','meta_ring_R'],
                'miror_target' : True,
                'bouding_sphere' : {'ring_01_R' : (0,0,0)}
            },
            'ring_02_R' : {
                'name' : 'ring_02_{}'.format(RIGHT_naming),
                'position' : (-84.173,140,-2.177),
                'joint_to_parent' : ['self','ring_01_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','ring_01_R'],
                'miror_target' : True,
                'bouding_sphere' : {'ring_02_R' : (0,0,0)}
            },
            'ring_03_R' : {
                'name' : 'ring_03_{}'.format(RIGHT_naming),
                'position' : (-89.3,140,-2.177),
                'joint_to_parent' : ['self','ring_02_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','ring_02_R'],
                'miror_target' : True,
                'bouding_sphere' : {'ring_03_R' : (0,0,0)}
            },
            'ring_tip_R' : {
                'name' : 'ring_tip_{}'.format(RIGHT_naming),
                'position' : (-93.338,140,-2.177),
                'joint_to_parent' : ['self','ring_03_R'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','ring_03_R'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            ##################################################################################################
             'meta_little_R' : {
                'name' : 'meta_little_{}'.format(RIGHT_naming),
                'position' : (-70.889,140,-5.954),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['arm__R',-1],
                'miror_target' : True,
                'bouding_sphere' : {'meta_little_R' : (0,0,0)}
            },
            'little_01_R' : {
                'name' : 'little_01_{}'.format(RIGHT_naming),
                'position' : (-78.963,140,-5.954),
                'joint_to_parent' : ['self','meta_little_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','meta_little_R'],
                'miror_target' : True,
                'bouding_sphere' : {'little_01_R' : (0,0,0)}
            },
            'little_02_R' : {
                'name' : 'little_02_{}'.format(RIGHT_naming),
                'position' : (-84.173,140,-5.954),
                'joint_to_parent' : ['self','little_01_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','little_01_R'],
                'miror_target' : True,
                'bouding_sphere' : {'little_02_R' : (0,0,0)}
            },
            'little_03_R' : {
                'name' : 'little_03_{}'.format(RIGHT_naming),
                'position' : (-89.3,140,-5.954),
                'joint_to_parent' : ['self','little_02_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','little_02_R'],
                'miror_target' : True,
                'bouding_sphere' : {'little_03_R' : (0,0,0)}
            },
            'little_tip_R' : {
                'name' : 'little_tip_{}'.format(RIGHT_naming),
                'position' : (-93.338,140,-5.954),
                'joint_to_parent' : ['self','little_03_R'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','little_03_R'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
        }
##################################################################################################
        self.hand_L_custom_setup_datas = {}
##################################################################################################
        self.hand_R_custom_setup_datas = {}
##################################################################################################
        self.leg_L_setup_datas = {
             'pelvis_L' : {
                'name' : 'pelvis_{}'.format(LEFT_naming),
                'position' : (9.24,89.981,0),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['spine',0],
                'miror_target' : True,
                'bouding_sphere' : {'pelvis_L' : (0,0,0)}
            },
            'hip_L' : {
                'name' : 'hip_{}'.format(LEFT_naming),
                'position' : (9.24,84.981,0),
                'joint_to_parent' : ['self','pelvis_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','pelvis_L'],
                'miror_target' : True,
                'bouding_sphere' : {'hip_L' : (0,0,0), 'hip_bend_L' : (0,16.626,0)}
            },
            'knee_L' : {
                'name' : 'knee_{}'.format(LEFT_naming),
                'position' : (9.24,48.935,4.517),
                'joint_to_parent' : ['self','hip_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','hip_L'],
                'miror_target' : True,
                'bouding_sphere' : {'knee_L' : (0,0,0), 'knee_bend_L' : (0,19.626,0)}
            },
            'ankle_L' : {
                'name' : 'ankle_{}'.format(LEFT_naming),
                'position' : (9.24,8.542,0),
                'joint_to_parent' : ['self','knee_L'],
                'do_not_aim' : "parent",
                'locator_to_parent' : ['self','knee_L'],
                'miror_target' : True,
                'bouding_sphere' : {'ankle_L' : (0,0,0)}
            },
        }
##################################################################################################
        self.leg_R_setup_datas = {
             'pelvis_R' : {
                'name' : 'pelvis_{}'.format(RIGHT_naming),
                'position' : (-9.24,89.981,0),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['spine',0],
                'miror_target' : True,
                'bouding_sphere' : {'pelvis_R' : (0,0,0)}
            },
            'hip_R' : {
                'name' : 'hip_{}'.format(RIGHT_naming),
                'position' : (-9.24,84.981,0),
                'joint_to_parent' : ['self','pelvis_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','pelvis_R'],
                'miror_target' : True,
                'bouding_sphere' : {'hip_R' : (0,0,0), 'hip_bend_R' : (0,16.626,0)}
            },
            'knee_R' : {
                'name' : 'knee_{}'.format(RIGHT_naming),
                'position' : (-9.24,48.935,4.517),
                'joint_to_parent' : ['self','hip_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','hip_R'],
                'miror_target' : True,
                'bouding_sphere' : {'knee_R' : (0,0,0), 'knee_bend_R' : (0,19.626,0)}
            },
            'ankle_R' : {
                'name' : 'ankle_{}'.format(RIGHT_naming),
                'position' : (-9.24,8.542,0),
                'joint_to_parent' : ['self','knee_R'],
                'do_not_aim' : "parent",
                'locator_to_parent' : ['self','knee_R'],
                'miror_target' : True,
                'bouding_sphere' : {'ankle_R' : (0,0,0)}
            },
        }
##################################################################################################
        self.single_toe_L_setup_datas = {
             'ball_L' : {
                'name' : 'ball_{}'.format(LEFT_naming),
                'position' : (9.24,2.626,9.626),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['leg__L',-1],
                'miror_target' : True,
                'bouding_sphere' : {'ball_L' : (0,0,0)}
            },
            'toe_L' : {
                'name' : 'toe_{}'.format(LEFT_naming),
                'position' : (9.24,2.626,19.597),
                'joint_to_parent' : ['self','ball_L'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','ball_L'],
                'miror_target' : True,
                'bouding_sphere' : {'toe_L' : (0,0,0)}
            },
            'toe_L_tip' : {
                'name' : 'toe_tip_{}'.format(LEFT_naming),
                'position' : (9.24,2.626,29.597),
                'joint_to_parent' : ['self','toe_L'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','toe_L'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
        }
##################################################################################################
        self.single_toe_R_setup_datas = {
             'ball_R' : {
                'name' : 'ball_{}'.format(RIGHT_naming),
                'position' : (-9.24,2.626,9.626),
                'joint_to_parent' : None,
                'do_not_aim' : False,
                'locator_to_parent' : ['leg__R',-1],
                'miror_target' : True,
                'bouding_sphere' : {'ball_R' : (0,0,0)}
            },
            'toe_R' : {
                'name' : 'toe_{}'.format(RIGHT_naming),
                'position' : (-9.24,2.626,19.597),
                'joint_to_parent' : ['self','ball_R'],
                'do_not_aim' : False,
                'locator_to_parent' : ['self','ball_R'],
                'miror_target' : True,
                'bouding_sphere' : {'toe_R' : (0,0,0)}
            },
            'toe_R_tip' : {
                'name' : 'toe_tip_{}'.format(RIGHT_naming),
                'position' : (-9.24,2.626,29.597),
                'joint_to_parent' : ['self','toe_R'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','toe_R'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
        }

##################################################################################################
        self.toes_L_setup_datas = {
             'ball_L' : {
                'name' : 'ball_{}'.format(LEFT_naming),
                'position' : (9.24,2.626,9.626),
                'joint_to_parent' : None,
                'do_not_aim' : "parent",
                'locator_to_parent' : ['leg__L',-1],
                'miror_target' : True,
                'bouding_sphere' : {'ball_L' : (0,0,0)}
            },
        }
##################################################################################################
        self.toes_R_setup_datas = {
             'ball_R' : {
                'name' : 'ball_{}'.format(RIGHT_naming),
                'position' : (-9.24,2.626,9.626),
                'joint_to_parent' : None,
                'do_not_aim' : "parent",
                'locator_to_parent' : ['leg__R',-1],
                'miror_target' : True,
                'bouding_sphere' : {'ball_R' : (0,0,0)}
            },
        }
##################################################################################################
        self.rev_L_setup_datas = {
             'heel_L' : {
                'name' : 'heel_{}'.format(LEFT_naming),
                'position' : (9.404,0,-4.835),
                'joint_to_parent' : None,
                'do_not_aim' : "parent",
                'locator_to_parent' : ['leg__L',-1],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            'toe_rev_L' : {
                'name' : 'toe_rev_{}'.format(LEFT_naming),
                'position' : (9.24,0,21.995),
                'joint_to_parent' : ['self','heel_L'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','heel_L'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            'outer_L' : {
                'name' : 'outer_{}'.format(LEFT_naming),
                'position' : (14.521,0,12.157),
                'joint_to_parent' : ['self','heel_L'],
                'do_not_aim' : "parent",
                'locator_to_parent' : ['self','heel_L'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            'inner_L' : {
                'name' : 'inner_{}'.format(LEFT_naming),
                'position' : (4.806,0,12.157),
                'joint_to_parent' : ['self','heel_L'],
                'do_not_aim' : "parent",
                'locator_to_parent' : ['self','heel_L'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
        }
##################################################################################################
        self.rev_R_setup_datas = {
             'heel_R' : {
                'name' : 'heel_{}'.format(RIGHT_naming),
                'position' : (-9.404,0,-4.835),
                'joint_to_parent' : None,
                'do_not_aim' : "parent",
                'locator_to_parent' : ['leg__R',-1],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            'toe_rev_R' : {
                'name' : 'toe_rev_{}'.format(RIGHT_naming),
                'position' : (-9.24,0,21.995),
                'joint_to_parent' : ['self','heel_R'],
                'do_not_aim' : True,
                'locator_to_parent' : ['self','heel_R'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            'outer_R' : {
                'name' : 'outer_{}'.format(RIGHT_naming),
                'position' : (-14.521,0,12.157),
                'joint_to_parent' : ['self','heel_R'],
                'do_not_aim' : "parent",
                'locator_to_parent' : ['self','heel_R'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
            'inner_R' : {
                'name' : 'inner_{}'.format(RIGHT_naming),
                'position' : (-4.806,0,12.157),
                'joint_to_parent' : ['self','heel_R'],
                'do_not_aim' : "parent",
                'locator_to_parent' : ['self','heel_R'],
                'miror_target' : True,
                'bouding_sphere' : {}
            },
        }

###################################################################################################
        self.facial_rigging_datas = {
            'head' : {
                        'name' : 'head',
                        'position' : (0,158.536, 1.733),
                        'joint_to_parent' : None,
                        'do_not_aim' : True,
                        'locator_to_parent' : ['neck',-1],
                        'miror_target' : False,
                        'bouding_sphere' : {'head' : (0,0,0)}
                    },
            'head_up' : {
                        'name' : 'head_up',
                        'position' : (0,175.755, 1.733),
                        'joint_to_parent' : ["self", "head"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "head"],
                        'miror_target' : False,
                        'bouding_sphere' : {'head_up' : (0,0,0)}
                    },
            'jaw' : {
                        'name' : 'jaw',
                        'position' : (0,160.305, 3.502),
                        'joint_to_parent' : ["self", "head"],
                        'do_not_aim' : False,
                        'locator_to_parent' : ["self", "head"],
                        'miror_target' : False,
                        'bouding_sphere' : {'jaw' : (0,0,0)}
                    },
            'jaw_tip' : {
                        'name' : 'jaw_tip',
                        'position' : (0,154.169, 11.793),
                        'joint_to_parent' : ["self", "jaw"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "jaw"],
                        'miror_target' : False,
                        'bouding_sphere' : {}
                    },
            'face_up' : {
                        'name' : 'face_up',
                        'position' : (0, 165.077, 12.788),
                        'joint_to_parent' : ["self", "head"],
                        'do_not_aim' : False,
                        'locator_to_parent' : ["self", "head"],
                        'miror_target' : False,
                        'bouding_sphere' : {'face_up' : (0,0,0)}
                    },
            'nose_base' : {
                        'name' : 'nose_base',
                        'position' : (0, 163.603, 13.749),
                        'joint_to_parent' : ["self", "face_up"],
                        'do_not_aim' : False,
                        'locator_to_parent' : ["self", "face_up"],
                        'miror_target' : False,
                        'bouding_sphere' : {'nose_base' : (0,0,0)}
                    },
            'nose' : {
                        'name' : 'nose',
                        'position' : (0, 161.206, 13.931),
                        'joint_to_parent' : ["self", "nose_base"],
                        'do_not_aim' : False,
                        'locator_to_parent' : ["self", "nose_base"],
                        'miror_target' : False,
                        'bouding_sphere' : {'nose' : (0,0,0)}
                    },
            'nose_tip' : {
                        'name' : 'nose_tip',
                        'position' : (0, 160.415, 14.317),
                        'joint_to_parent' : ["self", "nose"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "nose"],
                        'miror_target' : False,
                        'bouding_sphere' : {'nose_tip' : (0,0,0)}
                    },
            'nostril_L' : {
                        'name' : 'nostril_{}'.format(LEFT_naming),
                        'position' : (0.938, 160.526, 13.322),
                        'joint_to_parent' : ["self", "nose"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "nose"],
                        'miror_target' : True,
                        'bouding_sphere' : {'nostril_L' : (0,0,0)}
                    },
            'nostril_R' : {
                        'name' : 'nostril_{}'.format(RIGHT_naming),
                        'position' : (-0.938, 160.526, 13.322),
                        'joint_to_parent' : ["self", "nose"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "nose"],
                        'miror_target' : True,
                        'bouding_sphere' : {'nostril_R' : (0,0,0)}
                    },
            'upper_teeth' : {
                        'name' : 'upper_teeth',
                        'position' : (0, 159.052, 10.043),
                        'joint_to_parent' : ["self", "nose_base"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "nose_base"],
                        'miror_target' : False,
                        'bouding_sphere' : {}
                    },
            'lower_teeth' : {
                        'name' : 'lower_teeth',
                        'position' : (0, 156.749, 9.545),
                        'joint_to_parent' : ["self", "jaw"],
                        'do_not_aim' : "parent",
                        'locator_to_parent' : ["self", "jaw"],
                        'miror_target' : False,
                        'bouding_sphere' : {}
                    },
            'hear_L' : {
                        'name' : 'hear_{}'.format(LEFT_naming),
                        'position' : (6.56, 162.875, 2.987),
                        'joint_to_parent' : ["self", "head"],
                        'do_not_aim' : False,
                        'locator_to_parent' : ["self", "head"],
                        'miror_target' : True,
                        'bouding_sphere' : {'hear_L' : (0,0,0)}
                    },
            'hear_L_tip' : {
                        'name' : 'hear_{}_tip'.format(LEFT_naming),
                        'position' : (7.574, 162.428, -0.435),
                        'joint_to_parent' : ["self", "hear_L"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "hear_L"],
                        'miror_target' : True,
                        'bouding_sphere' : {}
                    },
            'hear_R' : {
                        'name' : 'hear_{}'.format(RIGHT_naming),
                        'position' : (-6.56, 162.875, 2.987),
                        'joint_to_parent' : ["self", "head"],
                        'do_not_aim' : False,
                        'locator_to_parent' : ["self", "head"],
                        'miror_target' : True,
                        'bouding_sphere' : {'hear_R' : (0,0,0)}
                    },
            'hear_R_tip' : {
                        'name' : 'hear_{}_tip'.format(RIGHT_naming),
                        'position' : (-7.574, 162.428, -0.435),
                        'joint_to_parent' : ["self", "hear_R"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "hear_R"],
                        'miror_target' : True,
                        'bouding_sphere' : {}
                    },
            'eye_L' : {
                        'name' : 'eye_{}'.format(LEFT_naming),
                        'position' : (2.876, 164.177, 10.542),
                        'joint_to_parent' : ["self", "head"],
                        'do_not_aim' : False,
                        'locator_to_parent' : ["self", "head"],
                        'miror_target' : True,
                        'bouding_sphere' : {}
                    },
            'eye_L_tip' : {
                        'name' : 'eye_{}_tip'.format(LEFT_naming),
                        'position' : (2.876, 164.177, 12.329),
                        'joint_to_parent' : ["self", "eye_L"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "eye_L"],
                        'miror_target' : True,
                        'bouding_sphere' : {}
                    },
            'eye_R' : {
                        'name' : 'eye_{}'.format(RIGHT_naming),
                        'position' : (-2.876, 164.177, 10.542),
                        'joint_to_parent' : ["self", "head"],
                        'do_not_aim' : False,
                        'locator_to_parent' : ["self", "head"],
                        'miror_target' : True,
                        'bouding_sphere' : {}
                    },
            'eye_R_tip' : {
                        'name' : 'eye_{}_tip'.format(RIGHT_naming),
                        'position' : (-2.876, 164.177, 12.329),
                        'joint_to_parent' : ["self", "eye_R"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "eye_R"],
                        'miror_target' : True,
                        'bouding_sphere' : {}
                    },
            'tongue_1' : {
                        'name' : 'tongue_01',
                        'position' : (0,156.539, 4.603),
                        'joint_to_parent' : ["self", "jaw"],
                        'do_not_aim' : False,
                        'locator_to_parent' : ["self", "jaw"],
                        'miror_target' : False,
                        'bouding_sphere' : {'tongue_1' : (0,0,0)}
                    },
            'tongue_2' : {
                        'name' : 'tongue_02',
                        'position' : (0, 157.039, 6.511),
                        'joint_to_parent' : ["self", "tongue_1"],
                        'do_not_aim' : False,
                        'locator_to_parent' : ["self", "tongue_1"],
                        'miror_target' : False,
                        'bouding_sphere' : {'tongue_2' : (0,0,0)}
                    },
            'tongue_3' : {
                        'name' : 'tongue_03',
                        'position' : (0, 156.861, 8.775),
                        'joint_to_parent' : ["self", "tongue_2"],
                        'do_not_aim' : True,
                        'locator_to_parent' : ["self", "tongue_2"],
                        'miror_target' : False,
                        'bouding_sphere' : {'tongue_3' : (0,0,0)}
                    },

        }

        self.size_setup_datas = 5

