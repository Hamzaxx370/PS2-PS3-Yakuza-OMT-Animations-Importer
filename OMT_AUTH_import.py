import bpy
from mathutils import *
import math
from .binary_reader import BinaryReader 
import time


def import_omt_auth(context, filepath,BodyArmature):
    
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
    Shared = [(0,9),(1,10),(2,11)]
    
    
    

    for BO in range (AnimKeyFramesCount):
        BonePointer = reader.read_uint32()
        BonePointers.append(BonePointer)
        
    print ("Bone Pointers:" , BonePointers)

    for KO in range (AnimKeyFramesCount):
        KeyFramePointer = reader.read_uint32()
        KeyFramePointers.append(KeyFramePointer)
        
    print ("KeyFrame Pointers:",KeyFramePointers)
    
    for KC in range (AnimKeyFramesCount):
        
        BoneFrameCount = reader.read_uint16()
        BoneFrameCounts.append(BoneFrameCount)
    print ("Individual Bone Frame Count:" ,BoneFrameCounts)
    
    
    
    
    for KFR1 in range(AnimKeyFramesCount):
        reader.seek(KeyFramePointers[KFR1])
        KeyFrames[KFR1] = []
        for KFR2 in range (BoneFrameCounts[KFR1]):
            
            Keyframe = reader.read_uint16()
        
            
            KeyFrames[KFR1].append(Keyframe)
    print ("Keyframes List:",KeyFrames)
    
    for ANIM in range (0,AnimKeyFramesCount,2):
        
        reader.seek(BonePointers[ANIM])
        
        
            
            
        BoneData[ANIM] = []
        for five in range(BoneFrameCounts[ANIM]):
            
            FloatDataX = reader.read_float()
            FloatDataY = reader.read_float()
            FloatDataZ = reader.read_float()
            BoneData[ANIM].append((FloatDataX/100,FloatDataZ/100,FloatDataY/100))
        
        reader.seek(BonePointers[ANIM+1])    
        
        
        BoneData[ANIM+1] = []
        for four in range(BoneFrameCounts[ANIM+1]):
            

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
                
                            
            BoneData[ANIM+1].append((NORMALIZED_W,NORMALIZED_X,NORMALIZED_Y,NORMALIZED_Z))
           
    print(BoneData)
        
        
    
    
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
    
    inx=0  
    for i in range(0,AnimKeyFramesCount,2):
        
        
        
              
        
        bone = bones[inx]
            
        
        keyframe_Data1 = KeyFrames[i+1]        
        
        anim_data1 = BoneData[i+1]
                           
        inner_count = 0    
        
        for k in keyframe_Data1:

            
            
            bone.rotation_quaternion = (anim_data1[inner_count][0], anim_data1[inner_count][1], anim_data1[inner_count][3], anim_data1[inner_count][2])
            bone.keyframe_insert(data_path="rotation_quaternion", frame=k)
            
            inner_count += 1
        inx+=1 
    inx1=0  
    for e in range(0,AnimKeyFramesCount,2):
        
        
         
              
        
        CenterBone = bones[inx1]
            
        keyframe_Data = KeyFrames[e]
            
        anim_data = BoneData[e]
        
                           
        CenterCount = 0
        
        for framecenter in keyframe_Data:
            CenterBone.location= (anim_data[CenterCount][0],anim_data[CenterCount][1],anim_data[CenterCount][2])
            CenterBone.keyframe_insert(data_path="location", frame=framecenter)
            CenterCount += 1
        inx1+=1 
    if BodyArmature != "None":
        for test in range(len(Shared)):
            TOMOVE = armature.pose.bones[Shared[test][0]]
            TOCOPY = BodyArmature.pose.bones[Shared[test][1]]
            Copy = TOMOVE.constraints.new(type='COPY_LOCATION')
            Copy.target = BodyArmature
            Copy.subtarget = TOCOPY.name
            CopyRot = TOMOVE.constraints.new(type='COPY_ROTATION')
            CopyRot.target = BodyArmature
            CopyRot.subtarget = TOCOPY.name
        
            
                    
        
        bpy.context.scene.frame_start = 0
        bpy.context.scene.frame_end = FrameCount
    
    
    
    OMT.close()
    
    return {'FINISHED'} 