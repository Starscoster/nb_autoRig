from maya import cmds

from nb_autoRig_v3 import nb_autorig_v3_controls as ctrl
from nb_autoRig_v3 import nb_autorig_v3_matrix_constraints as mat_const
from nb_autoRig_v3 import nb_autorig_v3_process as utils
from nb_autoRig_v3 import nb_autorig_v3_datas as datas

def create_facial_rig (rig_name, head_setup_dict, master_output, spine_output, neck_output) :
    

    # Associate element to correspongind data 

    print (rig_name)
    print (head_setup_dict)
    print (master_output)
    print (spine_output)
    print (neck_output)
