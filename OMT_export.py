import bpy
from mathutils import *
from .binary_reader import BinaryReader 
import math

def export_omt(context, filepath,PatternData,PatternFrames,Scale,ScaleHeight,DEBULLSHIT,ISYACT):
    
    armature = bpy.context.active_object
    bones = armature.pose.bones
    Center = armature.pose.bones[0]
    Ketu = armature.pose.bones[8]
    action = armature.animation_data.action
    
    QUATLIST = {}
    QuatPointerList = {}
    KeyframePointerList = {}
    CenterMovements = []
    DESTUFF = []
    DataFlags = [5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,1,0,0,0,0,0]
    FrameCount = int(action.frame_range[1])
    BoneCount = len(armature.data.bones)-1
    PatternCount = (len(PatternData))
    CenterKeyframes = []
    QUATKeyframes = {}
    
   
    for fcurve in action.fcurves:
        
        if fcurve.data_path == f'pose.bones["{Center.name}"].location':
            for keyframe in fcurve.keyframe_points:
                frame = keyframe.co[0]
                
                if fcurve.array_index == 0:
                    CenterKeyframes.append(int(frame))
                    
                    
    if DEBULLSHIT == True:
        for DE in range(FrameCount+1):
            bpy.context.scene.frame_set(DE)
            KetuLoc = Ketu.location
            DESTUFF.append(KetuLoc.z)
        
                        
                

    

    
    
    for quatkf in range(BoneCount):
        QUATKeyframes[quatkf] = []
        bone1 = bones[quatkf]
        for fcurve1 in action.fcurves:
            
            if fcurve1.data_path == f'pose.bones["{bone1.name}"].rotation_quaternion':
                for keyframe1 in fcurve1.keyframe_points:
                    frame1 = keyframe1.co[0]
                    
                    if fcurve1.array_index == 0:
                        QUATKeyframes[quatkf].append(int(frame1))
                

    

    
    
    
    for CNTR in range(FrameCount+1):
        bpy.context.scene.frame_set(CNTR)
        CenterLoc = Center.location
        CenterMovements.append((CenterLoc.x,((CenterLoc.z)),CenterLoc.y))
        
    for i in range(BoneCount):
        QUATLIST[i] = []
        inx=i
        bone = bones[inx]
        for QR in range(FrameCount+1):
            bpy.context.scene.frame_set(QR)
            quaternion = (bone.rotation_quaternion)
            
            
            sums = (quaternion.w**2) + (quaternion.x**2) + quaternion.y**2 + quaternion.z**2

            Magnitude = 1/(math.sqrt(sums))
            QUATSHORTW = (quaternion.w)*Magnitude
            QUATSHORTX = (quaternion.x)*Magnitude
            QUATSHORTY = (quaternion.y)*Magnitude
            QUATSHORTZ = (quaternion.z)*Magnitude
            
        
            Shortw = int((QUATSHORTW+1)*16384)
            Shortx = int((QUATSHORTX+1)*16384)
            Shorty = int((QUATSHORTY+1)*16384)
            Shortz = int((QUATSHORTZ+1)*16384)
            
            """
            if Shortx==0:
                Shortx=16384
            if Shorty==0:
                Shorty=16384
            if Shortz==0:
                Shortz=16384
            """

            QUATLIST[i].append((Shortw,Shortx,Shortz,Shorty))
            
    
    
    writer = BinaryReader()
    writer.write_uint32(32)
    KeyframePointer=writer.pos()
    writer.write_uint32(0)
    writer.write_uint32(BoneCount+2)
    FlagPointer=writer.pos()
    writer.write_uint32(0)
    writer.write_uint32(FrameCount+1)
    PointertoPointers=writer.pos()
    writer.write_uint32(0)
    writer.write_uint32(BoneCount+1)
    writer.write_uint32(0)
    
    
    CenterPointer = writer.pos()
    for CW in CenterKeyframes:
        writer.write_float(CenterMovements[CW][0]*Scale[0])
        if DEBULLSHIT == True:
            writer.write_float((DESTUFF[CW]*Scale[1])+(ScaleHeight))
        else:
            writer.write_float((CenterMovements[CW][1]*Scale[1])+(ScaleHeight))
        writer.write_float(CenterMovements[CW][2]*Scale[2])
        
    for QW1 in range(BoneCount):
        BoneQuat = QUATLIST[QW1]
        QuatPointerList[QW1] = []
        Pointer = writer.pos()
        QuatPointerList[QW1].append(Pointer)
        for QW2 in QUATKeyframes[QW1]:
            if ISYACT and QW1 in [3,6,14,19]:
                writer.write_uint16(BoneQuat[QW2][0])
                writer.write_uint16(BoneQuat[QW2][1])
            else:
                writer.write_uint16(BoneQuat[QW2][0])
                writer.write_uint16(BoneQuat[QW2][1])
                writer.write_uint16(BoneQuat[QW2][2])
                writer.write_uint16(BoneQuat[QW2][3])
            
    PatternOffset = writer.pos()
    for PF1 in range(PatternCount):
        writer.write_float(PatternData[PF1][0])
        writer.write_float(PatternData[PF1][1])
        if PatternData[PF1][2]==0.0:
            writer.write_float(-0.0)
        else:
            writer.write_float(PatternData[PF1][2])
        
            
    
    writer.align(4)
    KeyframesOffset = writer.pos()
    for KFC in CenterKeyframes:
        if FrameCount>255:
            writer.write_uint16(KFC)
        else:
            writer.write_uint8(KFC)
    for KW1 in range (BoneCount):
        KeyframePointerList[KW1] = []
        Pointer2 = writer.pos()
        KeyframePointerList[KW1].append(Pointer2)
    
        for KW2 in QUATKeyframes[KW1]:
            if FrameCount>255:
                writer.write_uint16(KW2)
            else:
                writer.write_uint8(KW2)
    PatternKyfOffset = writer.pos()
    for PKF in PatternFrames:
        if FrameCount>255:
            writer.write_uint16(int(PKF))
        else:
            writer.write_uint8(int(PKF))
    writer.align(4)
    PointersOffset = writer.pos()
    writer.write_uint32(CenterPointer)
    for QP1 in range(BoneCount):
        writer.write_uint32(QuatPointerList[QP1])
    writer.write_uint32(PatternOffset)
    writer.write_uint32(KeyframesOffset)
    for KP1 in range(BoneCount):
        writer.write_uint32(KeyframePointerList[KP1])
    writer.write_uint32(PatternKyfOffset)
    writer.align(4)
    if FrameCount>255:
        writer.write_uint16(len(CenterKeyframes))
    else:
        writer.write_uint8(len(CenterKeyframes))
    for FC in range(BoneCount):
        if FrameCount>255:
            writer.write_uint16(len(QUATKeyframes[FC]))
        else:
            writer.write_uint8(len(QUATKeyframes[FC]))
    if FrameCount>255:
        writer.write_uint16(len(PatternFrames))
    else:
        writer.write_uint8(len(PatternFrames))
    writer.align(4)
    FlagOffset = writer.pos()
    lenf = 0
    writer.write_uint8(5)
    lenf+=1
    for FLGS in range(BoneCount-1):
        lenf+=1
        if ISYACT and FLGS in [2,5,13,18]:
            writer.write_uint8(16)
        else:
            writer.write_uint8(4)
    writer.write_uint8(1)
    writer.align(16)
    
    writer.seek(KeyframePointer)
    writer.write_uint32(KeyframesOffset)
    writer.seek(PointertoPointers)
    writer.write_uint32(PointersOffset)
    writer.seek(FlagPointer)
    writer.write_uint32(FlagOffset)
            
   
    
    OMT = open(filepath, 'wb')
    OMT.write(writer.buffer())
    OMT.close()

    
                
    return{'FINISHED'} 