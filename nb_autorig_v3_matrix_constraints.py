from maya import cmds

#parent matrix : contraint two objects, with maintain offset option, in translate, scale and/or rotates. option for constraint opm or matrix attribut
def parent (trigger, target, offset, translate, rotate, scale, opm, nodeName) :

    #condition for offset
    if offset == True :

        #creates necesary nodes
        multNode = cmds.createNode ('multMatrix', name = nodeName + '_multMat')
        offsetNode = cmds.createNode ('composeMatrix', name = nodeName + '_offset')
        decNode = cmds.createNode ('decomposeMatrix', name = nodeName + '_decMat')
        tempoffset = cmds.createNode ('composeMatrix', name = nodeName + '_tempoffset')
        tempmult = cmds.createNode ('multMatrix', name = nodeName + '_tempmult')
        tempdecMat = cmds.createNode ('decomposeMatrix', name = nodeName + '_tempDecMat')

        #get parent
        parent = cmds.listRelatives (target, p=True, typ = 'transform')

        #parent target to trigger
        cmds.parent (target, trigger)

        #get translate relative to trigger

        tempTarget = target

        try :
            cmds.connectAttr ('{}.t'.format (target), '{}.inputTranslate'.format (tempoffset))
        except RuntimeError :
            cmds.connectAttr ('{}|{}.t'.format (trigger,target), '{}.inputTranslate'.format (tempoffset))
            tempTarget = f'{trigger}|{target}'
            
        cmds.connectAttr ('{}.r'.format (tempTarget), '{}.inputRotate'.format (tempoffset))
        cmds.connectAttr ('{}.s'.format (tempTarget), '{}.inputScale'.format (tempoffset))

        cmds.disconnectAttr ('{}.t'.format (tempTarget), '{}.inputTranslate'.format (tempoffset))
        cmds.disconnectAttr ('{}.r'.format (tempTarget), '{}.inputRotate'.format (tempoffset))
        cmds.disconnectAttr ('{}.s'.format (tempTarget), '{}.inputScale'.format (tempoffset))

        #reparent target to initial parent
        if parent != None :
            cmds.parent (tempTarget, parent)
        else :
            cmds.parent (tempTarget, w=True)  

        cmds.connectAttr ('{}.outputMatrix'.format(tempoffset), '{}.matrixIn[0]'.format(tempmult))
        cmds.connectAttr ('{}.offsetParentMatrix'.format(target), '{}.matrixIn[1]'.format(tempmult))
        cmds.connectAttr ('{}.matrixSum'.format(tempmult), '{}.inputMatrix'.format(tempdecMat))

        #parent target to trigger
        cmds.connectAttr ('{}.outputTranslate'.format (tempdecMat), '{}.inputTranslate'.format (offsetNode))
        cmds.connectAttr ('{}.outputRotate'.format (tempdecMat), '{}.inputRotate'.format (offsetNode))
        cmds.connectAttr ('{}.outputScale'.format (tempdecMat), '{}.inputScale'.format (offsetNode))

        cmds.disconnectAttr ('{}.outputTranslate'.format (tempdecMat), '{}.inputTranslate'.format (offsetNode))
        cmds.disconnectAttr ('{}.outputRotate'.format (tempdecMat), '{}.inputRotate'.format (offsetNode))
        cmds.disconnectAttr ('{}.outputScale'.format (tempdecMat), '{}.inputScale'.format (offsetNode))

        cmds.connectAttr ('{}.outputMatrix'.format(offsetNode), '{}.matrixIn[0]'.format(multNode))
        cmds.connectAttr ('{}.worldMatrix[0]'.format(trigger), '{}.matrixIn[1]'.format(multNode))
        

        cmds.connectAttr ('{}.matrixSum'.format(multNode), '{}.inputMatrix'.format(decNode))
        
        #condition for connection mode
        if opm == False :

            cmds.connectAttr ('{}.parentInverseMatrix[0]'.format(target), '{}.matrixIn[2]'.format(multNode))

            if translate == True :
                cmds.connectAttr ('{}.outputTranslate'.format (decNode), '{}.t'.format (target))

            if rotate == True :    
                cmds.connectAttr ('{}.outputRotate'.format (decNode), '{}.r'.format (target))

            if scale == True :
                cmds.connectAttr ('{}.outputScale'.format (decNode), '{}.s'.format (target))
            
        else : 

            compNode = cmds.createNode ('composeMatrix', name = nodeName + '_compMat')
            

            if translate == True :
                cmds.connectAttr ('{}.outputTranslate'.format (decNode), '{}.inputTranslate'.format (compNode))

            if rotate == True :    
                cmds.connectAttr ('{}.outputRotate'.format (decNode), '{}.inputRotate'.format (compNode))

            if scale == True :
                cmds.connectAttr ('{}.outputScale'.format (decNode), '{}.inputScale'.format (compNode))

            cmds.connectAttr ('{}.outputMatrix'.format (compNode), '{}.offsetParentMatrix'.format (target))

            cmds.setAttr ('{}.tx'.format(target),0)
            cmds.setAttr ('{}.ty'.format(target),0)
            cmds.setAttr ('{}.tz'.format(target),0)
            cmds.setAttr ('{}.rx'.format(target),0)
            cmds.setAttr ('{}.ry'.format(target),0)
            cmds.setAttr ('{}.rz'.format(target),0)
            cmds.setAttr ('{}.sx'.format(target),1)
            cmds.setAttr ('{}.sy'.format(target),1)
            cmds.setAttr ('{}.sz'.format(target),1)

        
        #delete unused nodes
        if cmds.objExists(tempoffset) == True :

            cmds.delete (tempoffset)

        if cmds.objExists(tempmult) == True :

            cmds.delete (tempmult)

        if cmds.objExists(tempdecMat) == True :

            cmds.delete (tempdecMat)  
        
        return multNode

    else :

        decNode = cmds.createNode ('decomposeMatrix', name = nodeName + '_decMat')

        if opm == False :
            
            multNode = cmds.createNode ('multMatrix', name = nodeName + '_multMat')
            cmds.connectAttr ('{}.worldMatrix[0]'.format(trigger), '{}.matrixIn[0]'.format(multNode))
            cmds.connectAttr ('{}.parentInverseMatrix[0]'.format(target), '{}.matrixIn[1]'.format(multNode))
            cmds.connectAttr ('{}.matrixSum'.format(multNode), '{}.inputMatrix'.format(decNode))
        
            if translate == True :
                cmds.connectAttr ('{}.outputTranslate'.format (decNode), '{}.t'.format (target))

            if rotate == True :    
                cmds.connectAttr ('{}.outputRotate'.format (decNode), '{}.r'.format (target))

            if scale == True :
                cmds.connectAttr ('{}.outputScale'.format (decNode), '{}.s'.format (target))

            return multNode

        else :

            cmds.connectAttr ('{}.worldMatrix[0]'.format(trigger), '{}.inputMatrix'.format(decNode))
            compNode = cmds.createNode ('composeMatrix', name = nodeName + '_compMat')

            if translate == True :
                cmds.connectAttr ('{}.outputTranslate'.format (decNode), '{}.inputTranslate'.format (compNode))

            if rotate == True :    
                cmds.connectAttr ('{}.outputRotate'.format (decNode), '{}.inputRotate'.format (compNode))

            if scale == True :
                cmds.connectAttr ('{}.outputScale'.format (decNode), '{}.inputScale'.format (compNode))
            
            cmds.connectAttr ('{}.outputMatrix'.format (compNode), '{}.offsetParentMatrix'.format (target))

            cmds.setAttr ('{}.tx'.format(target),0)
            cmds.setAttr ('{}.ty'.format(target),0)
            cmds.setAttr ('{}.tz'.format(target),0)
            cmds.setAttr ('{}.rx'.format(target),0)
            cmds.setAttr ('{}.ry'.format(target),0)
            cmds.setAttr ('{}.rz'.format(target),0)
            cmds.setAttr ('{}.sx'.format(target),1)
            cmds.setAttr ('{}.sy'.format(target),1)
            cmds.setAttr ('{}.sz'.format(target),1)     

#aim matrix : needs 4 objexts : trigger, target, input is translate base of target, wup is world up object
def aim(trigger, target, input, wup, primary, secondary, secTarget, opm, nodeName) :

    aimNode = cmds.createNode('aimMatrix', name = nodeName + '_aimMat')
    if opm == True :

        cmds.connectAttr ('{}.worldMatrix[0]'.format(input), '{}.inputMatrix'.format (aimNode))
        cmds.connectAttr ('{}.worldMatrix[0]'.format(trigger), '{}.primaryTargetMatrix'.format (aimNode))
        cmds.connectAttr ('{}.worldMatrix[0]'.format(wup), '{}.secondaryTargetMatrix'.format (aimNode))

        cmds.setAttr ('{}.secondaryMode'.format (aimNode), 2)

        cmds.setAttr ('{}.primaryInputAxisX'.format (aimNode), primary[0])
        cmds.setAttr ('{}.primaryInputAxisY'.format (aimNode), primary[1])
        cmds.setAttr ('{}.primaryInputAxisZ'.format (aimNode), primary[2])

        cmds.setAttr ('{}.secondaryInputAxisX'.format (aimNode), secondary[0])
        cmds.setAttr ('{}.secondaryInputAxisY'.format (aimNode), secondary[1])
        cmds.setAttr ('{}.secondaryInputAxisZ'.format (aimNode), secondary[2])

        cmds.setAttr ('{}.secondaryTargetVectorX'.format (aimNode), secTarget[0])
        cmds.setAttr ('{}.secondaryTargetVectorY'.format (aimNode), secTarget[1])
        cmds.setAttr ('{}.secondaryTargetVectorZ'.format (aimNode), secTarget[2])

        decNode = cmds.createNode('decomposeMatrix', name = nodeName + '_decMat')
        compNode = cmds.createNode('composeMatrix', name = nodeName + '_compMat')

        cmds.connectAttr ('{}.outputMatrix'.format(aimNode), '{}.imat'.format(decNode))
        cmds.connectAttr ('{}.or'.format(decNode), '{}.ir'.format(compNode))
        cmds.connectAttr ('{}.omat'.format(compNode), '{}.offsetParentMatrix'.format(target))

        cmds.setAttr ('{}.tx'.format(target), 0)
        cmds.setAttr ('{}.ty'.format(target), 0)
        cmds.setAttr ('{}.tz'.format(target), 0)
        cmds.setAttr ('{}.rx'.format(target), 0)
        cmds.setAttr ('{}.ry'.format(target), 0)
        cmds.setAttr ('{}.rz'.format(target), 0)
        cmds.setAttr ('{}.sx'.format(target), 1)
        cmds.setAttr ('{}.sy'.format(target), 1)
        cmds.setAttr ('{}.sz'.format(target), 1)

    else :

        decomposeNode = cmds.createNode('decomposeMatrix', name = nodeName + '_aimDecMat')

        cmds.connectAttr ('{}.worldMatrix[0]'.format(input), '{}.inputMatrix'.format (aimNode))
        cmds.connectAttr ('{}.worldMatrix[0]'.format(trigger), '{}.primaryTargetMatrix'.format (aimNode))
        cmds.connectAttr ('{}.worldMatrix[0]'.format(wup), '{}.secondaryTargetMatrix'.format (aimNode))

        cmds.setAttr ('{}.secondaryMode'.format (aimNode), 2)

        cmds.setAttr ('{}.primaryInputAxisX'.format (aimNode), primary[0])
        cmds.setAttr ('{}.primaryInputAxisY'.format (aimNode), primary[1])
        cmds.setAttr ('{}.primaryInputAxisZ'.format (aimNode), primary[2])

        cmds.setAttr ('{}.secondaryInputAxisX'.format (aimNode), secondary[0])
        cmds.setAttr ('{}.secondaryInputAxisY'.format (aimNode), secondary[1])
        cmds.setAttr ('{}.secondaryInputAxisZ'.format (aimNode), secondary[2])

        cmds.setAttr ('{}.secondaryTargetVectorX'.format (aimNode), secTarget[0])
        cmds.setAttr ('{}.secondaryTargetVectorY'.format (aimNode), secTarget[1])
        cmds.setAttr ('{}.secondaryTargetVectorZ'.format (aimNode), secTarget[2])

        cmds.connectAttr ('{}.outputMatrix'.format(aimNode), '{}.inputMatrix'.format(decomposeNode))
        #cmds.connectAttr ('{}.outputTranslate'.format(decomposeNode), '{}.t'.format(target))
        cmds.connectAttr ('{}.outputRotate'.format(decomposeNode), '{}.r'.format(target))
        #cmds.connectAttr ('{}.outputScale'.format(decomposeNode), '{}.s'.format(target))

def blendParent (target, trigger, name) :
    
    print ("blend parent", target, trigger)

    #creates necesary nodes
    multNode = cmds.createNode ('multMatrix', name = name + '_multMat')
    offsetNode = cmds.createNode ('composeMatrix', name = name + '_offset')
    tempoffset = cmds.createNode ('composeMatrix', name = name + '_tempoffset')
    tempmult = cmds.createNode ('multMatrix', name = name + '_tempmult')
    tempdecMat = cmds.createNode ('decomposeMatrix', name = name + '_tempDecMat')

    #get parent
    parent = cmds.listRelatives (target, p=True, typ = 'transform')

    #parent target to trigger
    cmds.parent (target, trigger)

    print (cmds.getAttr("{}.translate".format(target)), cmds.getAttr("{}.rotate".format(target)), cmds.getAttr("{}.scale".format(target)))

    #get translate relative to trigger
    cmds.connectAttr ('{}.t'.format (target), '{}.inputTranslate'.format (tempoffset))
    cmds.connectAttr ('{}.r'.format (target), '{}.inputRotate'.format (tempoffset))
    cmds.connectAttr ('{}.s'.format (target), '{}.inputScale'.format (tempoffset))

    cmds.disconnectAttr ('{}.t'.format (target), '{}.inputTranslate'.format (tempoffset))
    cmds.disconnectAttr ('{}.r'.format (target), '{}.inputRotate'.format (tempoffset))
    cmds.disconnectAttr ('{}.s'.format (target), '{}.inputScale'.format (tempoffset))

    cmds.connectAttr ('{}.outputMatrix'.format(tempoffset), '{}.matrixIn[0]'.format(tempmult))
    cmds.connectAttr ('{}.offsetParentMatrix'.format(target), '{}.matrixIn[1]'.format(tempmult))
    cmds.connectAttr ('{}.matrixSum'.format(tempmult), '{}.inputMatrix'.format(tempdecMat))

    #parent target to trigger
    cmds.connectAttr ('{}.outputTranslate'.format (tempdecMat), '{}.inputTranslate'.format (offsetNode))
    cmds.connectAttr ('{}.outputRotate'.format (tempdecMat), '{}.inputRotate'.format (offsetNode))
    cmds.connectAttr ('{}.outputScale'.format (tempdecMat), '{}.inputScale'.format (offsetNode))

    cmds.disconnectAttr ('{}.outputTranslate'.format (tempdecMat), '{}.inputTranslate'.format (offsetNode))
    cmds.disconnectAttr ('{}.outputRotate'.format (tempdecMat), '{}.inputRotate'.format (offsetNode))
    cmds.disconnectAttr ('{}.outputScale'.format (tempdecMat), '{}.inputScale'.format (offsetNode))

    cmds.connectAttr ('{}.outputMatrix'.format(offsetNode), '{}.matrixIn[0]'.format(multNode))
    cmds.connectAttr ('{}.worldMatrix[0]'.format(trigger), '{}.matrixIn[1]'.format(multNode))

    #reparent target to initial parent
    if parent != None :
        cmds.parent (target, parent)
    else :
        cmds.parent (target, w=True)  

    #delete unused nodes
    if cmds.objExists(tempoffset) == True :

        cmds.delete (tempoffset)

    if cmds.objExists(tempmult) == True :

        cmds.delete (tempmult)

    if cmds.objExists(tempdecMat) == True :

        cmds.delete (tempdecMat)  
        
    return multNode

def opm(transform) :

    cmds.select (d=True)
    
    cmds.createNode ('composeMatrix', name = 'OPMtemp_compMat')
    cmds.createNode ('decomposeMatrix', name = 'OPMtemp_decompMat')
    cmds.createNode ('multMatrix', name = 'OPMtemp_multMat')
    
    cmds.connectAttr(transform + '.matrix', 'OPMtemp_multMat.matrixIn[0]')
    cmds.connectAttr(transform + '.offsetParentMatrix', 'OPMtemp_multMat.matrixIn[1]')
    
    cmds.connectAttr('OPMtemp_multMat.matrixSum', 'OPMtemp_decompMat.inputMatrix')
    
    cmds.connectAttr('OPMtemp_decompMat.ot', 'OPMtemp_compMat.inputTranslate')
    cmds.connectAttr('OPMtemp_decompMat.or', 'OPMtemp_compMat.inputRotate')
    cmds.connectAttr('OPMtemp_decompMat.os', 'OPMtemp_compMat.inputScale')
    
    cmds.disconnectAttr('OPMtemp_decompMat.ot', 'OPMtemp_compMat.inputTranslate')
    cmds.disconnectAttr('OPMtemp_decompMat.or', 'OPMtemp_compMat.inputRotate')
    cmds.disconnectAttr('OPMtemp_decompMat.os', 'OPMtemp_compMat.inputScale')
    
    cmds.connectAttr('OPMtemp_compMat.outputMatrix', transform + '.offsetParentMatrix')
    
    cmds.setAttr (transform + '.t', *(0,0,0))
    cmds.setAttr (transform + '.r', *(0,0,0))
    cmds.setAttr (transform + '.s', *(1,1,1))

    
    if cmds.objExists('OPMtemp_compMat') == True :
        
        cmds.delete ('OPMtemp_compMat')
        
    if cmds.objExists('OPMtemp_decompMat') == True :
        
        cmds.delete ('OPMtemp_decompMat')
        
    if cmds.objExists('OPMtemp_multMat') == True :
        
        cmds.delete ('OPMtemp_multMat')

#blend Mat is parent Matrix with multiples targets
def blend(inputList, affectList, wheightList, weightSwitch, output, nodeName):

    blendNode = cmds.createNode ('blendMatrix', name = nodeName + '_blendMat')

    cmds.connectAttr (inputList, '{}.inputMatrix'.format(blendNode))

    targetIndex = 0

    for each in affectList :

        cmds.connectAttr(each, '{}.target[{}].targetMatrix'.format(blendNode, targetIndex))

        tWeight, rWeight, sWeight = wheightList[targetIndex]

        if  isinstance(weightSwitch, str) == True :

            cmds.connectAttr (weightSwitch, '{}.target[{}].weight'.format(blendNode, targetIndex))

        else :

            cmds.setAttr('{}.target[{}].weight'.format(blendNode, targetIndex), weightSwitch)

        cmds.setAttr ('{}.target[{}].tra'.format(blendNode, targetIndex), tWeight)
        cmds.setAttr ('{}.target[{}].rot'.format(blendNode, targetIndex), rWeight)
        cmds.setAttr ('{}.target[{}].sca'.format(blendNode, targetIndex), sWeight)
        targetIndex += 1

    cmds.connectAttr('{}.outputMatrix'.format(blendNode), output)
    
    return blendNode

def getOffset (coords1, obj, compName) :

    locator2 = cmds.spaceLocator(name = 'tempLocator2')[0]
    coords2 = cmds.xform(obj, q=True, m=True, ws=True)
    cmds.xform(locator2, m=coords2)
    locator1 = cmds.spaceLocator(name = 'tempLocator1')[0]
    loc1DecMat = cmds.createNode('decomposeMatrix', name = 'tempLoc1DecMat')
    cmds.connectAttr (coords1, f'{loc1DecMat}.imat')
    cmds.connectAttr (f'{loc1DecMat}.ot', f'{locator1}.t')
    cmds.connectAttr (f'{loc1DecMat}.or', f'{locator1}.r')
    cmds.connectAttr (f'{loc1DecMat}.os', f'{locator1}.s')

    cmds.parent (locator2, locator1)

    tempDec = cmds.createNode('decomposeMatrix', name = 'tempDec')
    tempComp = cmds.createNode('composeMatrix', name = compName)

    try :
        cmds.connectAttr (f'{locator2}.m', f'{tempDec}.inputMatrix')
    except RuntimeError :
        cmds.connectAttr ('{}|{}.m'.format (locator1,locator2), f'{tempDec}.inputMatrix')
        locator2 = f'{locator1}|{locator2}'

    cmds.connectAttr(f'{tempDec}.ot', f'{tempComp}.it')
    cmds.connectAttr(f'{tempDec}.or', f'{tempComp}.ir')
    cmds.connectAttr(f'{tempDec}.os', f'{tempComp}.is')

    cmds.disconnectAttr(f'{tempDec}.ot', f'{tempComp}.it')
    cmds.disconnectAttr(f'{tempDec}.or', f'{tempComp}.ir')
    cmds.disconnectAttr(f'{tempDec}.os', f'{tempComp}.is')

    if cmds.objExists('tempDec') == True :
        cmds.delete('tempDec')
    if cmds.objExists('tempLocator') == True :
        cmds.delete('tempLocator')

    cmds.delete(locator1)

    return tempComp