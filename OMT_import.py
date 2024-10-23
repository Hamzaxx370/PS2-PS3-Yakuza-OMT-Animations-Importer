import bpy
from mathutils import *
import math
from .binary_reader import BinaryReader 
import time


def import_omt(context, filepath,CenterImport):
    OMT = open (filepath,"rb")
    reader = BinaryReader(OMT.read())
    AnimDataOffset = reader.read_uint32()
    AnimKeyFramesOffset = reader.read_uint32()
    AnimKeyFramesCount = reader.read_uint32()
    AnimTypeFlagsOffset = reader.read_uint32()
    FrameCount = reader.read_uint32()
    if FrameCount>255:
        ShortFrames = True
    else:
        ShortFrames = False
    AnimDataBoneOffsets = reader.read_uint32()
    BoneCount = reader.read_uint32()
    print ("Header Info:",AnimDataOffset,AnimKeyFramesOffset,AnimKeyFramesCount,AnimTypeFlagsOffset,FrameCount,AnimDataBoneOffsets,BoneCount)
    reader.seek(AnimDataBoneOffsets)
    BonePointers = []
    KeyFramePointers = []
    BoneFrameCounts = []
    DataFlags = []
    DataFlags1  = []
    KeyFrames = {}
    BoneData = {}
    ArrangedBoneData = {}
    ArrangedKeyframes = {}
    LocCount = 0
    
    

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
    reader.seek(AnimTypeFlagsOffset)
    
    Zeroes = 0
    for FLG in range (BoneCount):
        Flag = reader.read_uint8()
        print(Flag)
        if Flag == 5:
            DataFlags.append(Flag)
            DataFlags1.append(Flag)
            DataFlags1.append(4)
        elif Flag == 0:
            Zeroes+=1
            DataFlags.append(Flag)
            
            
            
        
        else:
            DataFlags.append(Flag)
            DataFlags1.append(Flag)
    #print ("Animation Data Flags:",DataFlags)
    DataFlags.append(1)
    DataFlags1.append(1)
    DataFlags.append(1)
    DataFlags1.append(1)
    
    
    
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
    print(DataFlags,DataFlags1)
    
    for ANIM in range (AnimKeyFramesCount):
        print(ANIM)
        reader.seek(BonePointers[ANIM])
        
        if DataFlags1[ANIM] == 5:
            
            
            BoneData[ANIM] = []
            for five in range(BoneFrameCounts[ANIM]):
                
                FloatDataX = reader.read_float()
                FloatDataY = reader.read_float()
                FloatDataZ = reader.read_float()
                BoneData[ANIM].append((FloatDataX,FloatDataZ,FloatDataY))
        
            
                
        elif DataFlags1[ANIM] == 4:
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
            
                
        elif DataFlags1[ANIM] == 16:
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
                
                
                
        elif DataFlags1[ANIM] == 1:
            BoneData[ANIM] = []
            for one in range(BoneFrameCounts[ANIM]):
                BoneData[ANIM].append((1,0,0,0))
                
        elif DataFlags1[ANIM] == 0:
            BoneData[ANIM] = []
            for zero in range(BoneFrameCounts[ANIM]):
                BoneData[ANIM].append((1,0,0,0))
            
        
           
                
                
    #print ("Animation Data",BoneData)
    Count = 0
    CountData = 0
    
    for ARNG in range(BoneCount-Zeroes):
        if DataFlags[Count] == 5:
            ArrangedBoneData[Count] = [[],[]]
            ArrangedKeyframes[Count] = [[],[]]
            ArrangedBoneData[Count][0].extend(BoneData[CountData])
            ArrangedKeyframes[Count][0].extend(KeyFrames[CountData])
            ArrangedBoneData[Count][1].extend(BoneData[CountData+1])
            ArrangedKeyframes[Count][1].extend(KeyFrames[CountData+1])
            Count+=1
            CountData+=2
        elif DataFlags[Count] == 0:
            Count+=1
            ArrangedBoneData[Count] = [[],[]]
            ArrangedKeyframes[Count] = [[],[]]
            ArrangedBoneData[Count][1].extend(BoneData[CountData])
            ArrangedKeyframes[Count][1].extend(KeyFrames[CountData])
            Count+=1
            CountData+=1
        
        else:
            ArrangedBoneData[Count] = [[],[]]
            ArrangedKeyframes[Count] = [[],[]]
            ArrangedBoneData[Count][1].extend(BoneData[CountData])
            ArrangedKeyframes[Count][1].extend(KeyFrames[CountData])
            Count+=1
            CountData+=1
    
            
        
    
    
    bpy.context.scene.render.fps = 30
    bpy.context.scene.render.fps_base = 1

    activeobj = bpy.context.active_object
    if activeobj.animation_data:
        activeobj.animation_data_clear()
        activeobj.data.animation_data_clear()
        for clearloc in activeobj.pose.bones:
            clearloc.location=[0.0,0.0,0.0]
    newaction= bpy.data.actions.new(name="OMT_Action")
    activeobj.animation_data_create()
    activeobj.animation_data.action= newaction
    armature = activeobj
    bones = armature.pose.bones   
    
    
    for i in range(BoneCount-Zeroes):
   
        
        inx=i
        if DataFlags[i]==0:
            pass
        else:
        
              
            BoneName = str(inx)
            bone = bones[inx]
        
            
            keyframe_Data = ArrangedKeyframes[i][1]
            anim_data = ArrangedBoneData[i][1]
            
                            
            inner_count = 0 
            inner_count1 = 0
            
            for k in keyframe_Data:

                
                
                bone.rotation_quaternion = (anim_data[inner_count][0], anim_data[inner_count][1], anim_data[inner_count][3], anim_data[inner_count][2])
                bone.keyframe_insert(data_path="rotation_quaternion", frame=k)
                
                inner_count += 1
            if DataFlags[i] == 5 and CenterImport == True :
                keyframe_Data1 = ArrangedKeyframes[i][0]
                anim_data1 = ArrangedBoneData[i][0]
                for k1 in keyframe_Data1:
                    if inx==0:
                        scale=10.46
                    else:
                        scale=0
                    bone.location= (anim_data1[inner_count1][0],anim_data1[inner_count1][1],anim_data1[inner_count1][2] - scale)
                    bone.keyframe_insert(data_path="location", frame=k1)
                    inner_count1 += 1
                
    """
    if CenterImport == True:
        CenterBone= armature.pose.bones[0]
        CenterXYZ= BoneData[0]
        CenterFrames = KeyFrames[0]
        CenterCount = 0
            
            
        for framecenter in CenterFrames:
            CenterBone.location= (CenterXYZ[CenterCount][0],CenterXYZ[CenterCount][1],CenterXYZ[CenterCount][2] - 2.3)
            CenterBone.keyframe_insert(data_path="location", frame=framecenter)
            CenterCount += 1
    """       
        
                
    
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = FrameCount
    
    
    
    OMT.close()
    return {'FINISHED'} 