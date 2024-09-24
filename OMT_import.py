import bpy
from mathutils import *
import math
from .binary_reader import BinaryReader 
import time


def import_omt(context, filepath,CenterImport,Y2SUP,ShortFrames):
    OMT = open (filepath,"rb")
    reader = BinaryReader(OMT.read())
    AnimDataOffset = reader.read_uint32()
    AnimKeyFramesOffset = reader.read_uint32()
    AnimKeyFramesCount = reader.read_uint32()
    AnimTypeFlagsOffset = reader.read_uint32()
    FrameCount = reader.read_uint32()
    AnimDataBoneOffsets = reader.read_uint32()
    BoneCount = reader.read_uint32()
    print ("Header Info:",AnimDataOffset,AnimKeyFramesOffset,AnimKeyFramesCount,AnimTypeFlagsOffset,FrameCount,AnimDataBoneOffsets,BoneCount)
    reader.seek(AnimDataBoneOffsets)
    BonePointers = []
    KeyFramePointers = []
    BoneFrameCounts = []
    DataFlags = []
    KeyFrames = {}
    BoneData = {}
    
    if Y2SUP== True:
        BoneCount=23

    for BO in range (AnimKeyFramesCount):
        BonePointer = reader.read_uint32()
        BonePointers.append(BonePointer)
        
    #print ("Bone Pointers:" , BonePointers)

    for KO in range (AnimKeyFramesCount):
        KeyFramePointer = reader.read_uint32()
        KeyFramePointers.append(KeyFramePointer)
        
    #print ("KeyFrame Pointers:",KeyFramePointers)
    
    for KC in range (AnimKeyFramesCount):
        if ShortFrames==True:
            BoneFrameCount = reader.read_uint16()
        else:
            BoneFrameCount = reader.read_uint8()
        BoneFrameCounts.append(BoneFrameCount)
    #print ("Individual Bone Frame Count:" ,BoneFrameCounts)
    
    if Y2SUP== True:
        DataFlags = [5, 4, 4, 4, 16, 4, 4, 16, 4, 4, 4, 4, 4, 4, 4, 16, 4, 4,4, 4, 16, 4, 4, 0]
    else:
    
        for FLG in range (AnimKeyFramesCount):
            Flag = reader.read_uint8()
            if Flag == 5:
                DataFlags.append(Flag)
                DataFlags.append(4)
            else:
                DataFlags.append(Flag)
        #print ("Animation Data Flags:",DataFlags)
    
    
    
    for KFR1 in range(AnimKeyFramesCount):
        reader.seek(KeyFramePointers[KFR1])
        KeyFrames[KFR1] = []
        for KFR2 in range (BoneFrameCounts[KFR1]):
            if ShortFrames==True:
                Keyframe = reader.read_uint16()
            else:
                Keyframe = reader.read_uint8()
            KeyFrames[KFR1].append(Keyframe)
    #print ("Keyframes List:",KeyFrames)
    
    for ANIM in range (AnimKeyFramesCount):
        
        reader.seek(BonePointers[ANIM])
        
        if DataFlags[ANIM] == 5:
            
            
            BoneData[ANIM] = []
            for five in range(BoneFrameCounts[ANIM]):
                
                FloatDataX = reader.read_float()
                FloatDataY = reader.read_float()-8.16
                FloatDataZ = reader.read_float()
                BoneData[ANIM].append((FloatDataX,FloatDataZ,FloatDataY))
        
            
                
        elif DataFlags[ANIM] == 4:
            BoneData[ANIM] = []
            for four in range(BoneFrameCounts[ANIM]):
                

                SHORTDataW = reader.read_uint16()
                SHORTDataX = reader.read_uint16()
                SHORTDataY = reader.read_uint16()
                SHORTDataZ = reader.read_uint16()

                QUAT_SHORTDataW = (SHORTDataW/32768)-0.5
                QUAT_SHORTDataX = (SHORTDataX/32768)-0.5
                QUAT_SHORTDataY = (SHORTDataY/32768)-0.5
                QUAT_SHORTDataZ = (SHORTDataZ/32768)-0.5

                sums = QUAT_SHORTDataW**2 + QUAT_SHORTDataX**2 + QUAT_SHORTDataY**2 + QUAT_SHORTDataZ**2

                Magnitude = math.sqrt(sums)
                #print("Magnitude", Magnitude)                


                NORMALIZED_W = (QUAT_SHORTDataW/Magnitude)
                NORMALIZED_X = (QUAT_SHORTDataX/Magnitude)
                NORMALIZED_Y = (QUAT_SHORTDataY/Magnitude)
                NORMALIZED_Z = (QUAT_SHORTDataZ/Magnitude)
                    
                             
                BoneData[ANIM].append((NORMALIZED_W,NORMALIZED_X,NORMALIZED_Y,NORMALIZED_Z))
            
                
        elif DataFlags[ANIM] == 16:
            BoneData[ANIM] = []
            for sixteen in range(BoneFrameCounts[ANIM]):
                bSHORTDataW = reader.read_uint16()
                bSHORTDataX = reader.read_uint16()
                bSHORTDataY = 0
                bSHORTDataZ = 0
                
                

                bQUAT_SHORTDataW = (bSHORTDataW/32768)-0.5
                bQUAT_SHORTDataX = (bSHORTDataX/32768)-0.5
                bQUAT_SHORTDataY = (bSHORTDataY/32768)-0.5
                bQUAT_SHORTDataZ = (bSHORTDataZ/32768)-0.5
                
                bsums = bQUAT_SHORTDataW**2 + bQUAT_SHORTDataX**2 + bQUAT_SHORTDataY**2 + bQUAT_SHORTDataZ**2

                bMagnitude = math.sqrt(bsums)
                      


                bNORMALIZED_W = (bQUAT_SHORTDataW/bMagnitude)
                bNORMALIZED_X = (bQUAT_SHORTDataX/bMagnitude)
                bNORMALIZED_Y = 0
                bNORMALIZED_Z = 0
                
                    
                
                
                              
                BoneData[ANIM].append((bNORMALIZED_W,bNORMALIZED_X,bNORMALIZED_Y,bNORMALIZED_Z))
                
                
                
        elif DataFlags[ANIM] == 1:
            BoneData[ANIM] = []
            for one in range(BoneFrameCounts[ANIM]):
                BoneData[ANIM].append((1,0,0,0))
                
        elif DataFlags[ANIM] == 0:
            
        
            BoneData[ANIM] = []
            for zero in range(BoneFrameCounts[ANIM]):
                BoneData[ANIM].append((1,0,0,0))
    #print ("Animation Data",BoneData)
        
    
    
    bpy.context.scene.render.fps = 30
    bpy.context.scene.render.fps_base = 1

    activeobj = bpy.context.active_object
    if activeobj.animation_data:
        activeobj.animation_data.action = None
    newaction= bpy.data.actions.new(name="OMT_Action")
    activeobj.animation_data_create()
    activeobj.animation_data.action= newaction
    armature = activeobj
    bones = armature.pose.bones   
    
    
    for i in range(BoneCount):
        
        if Y2SUP==True:
            if i>=17:
                inx=i+1
            else:
                inx = i 
        else:
            inx=i   
              
        BoneName = str(inx)
        bone = bones[inx]
            
        keyframe_Data = KeyFrames[i+1]      
        anim_data = BoneData[i+1]
                           
        inner_count = 0    
        
        for k in keyframe_Data:

            
            
            bone.rotation_quaternion = (anim_data[inner_count][0], anim_data[inner_count][1], anim_data[inner_count][3], anim_data[inner_count][2])
            bone.keyframe_insert(data_path="rotation_quaternion", frame=k)
            
            inner_count += 1
            
    if CenterImport == True:
        CenterBone= armature.pose.bones[0]
        CenterXYZ= BoneData[0]
        CenterFrames = KeyFrames[0]
        CenterCount = 0
            
            
        for framecenter in CenterFrames:
            CenterBone.location= (CenterXYZ[CenterCount][0],CenterXYZ[CenterCount][1],CenterXYZ[CenterCount][2] - 2.3)
            CenterBone.keyframe_insert(data_path="location", frame=framecenter)
            CenterCount += 1
        
        
                
    
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = FrameCount
    
    
    
    OMT.close()
    return {'FINISHED'} 
