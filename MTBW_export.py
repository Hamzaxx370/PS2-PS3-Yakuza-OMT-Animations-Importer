import bpy
from mathutils import *
from .binary_reader import BinaryReader 
import math

def export_MTBW(context, filepath,BIG,FLIP):
    
    Camera = bpy.context.active_object
    if BIG:
        scale = 10
    else:
        scale =1
    if FLIP:
        flip = -1
    else:
        flip =1
    action = Camera.animation_data.action
    LocKeyFrames = []
    RotKeyFrames = []
    FovKeyFrames = []
    FrameCount = int(action.frame_range[1])
    LocAnim = []
    RotAnim = []
    FovAnim = []
    
    

    for fcurve in action.fcurves:
        
        if fcurve.data_path == "location":
            for keyframe in fcurve.keyframe_points:
                frame = keyframe.co[0]
                
                if fcurve.array_index == 0:
                    LocKeyFrames.append(int(frame))
    
    for fcurve in action.fcurves:
        
        if fcurve.data_path == "rotation_quaternion":
            for keyframe in fcurve.keyframe_points:
                frame = keyframe.co[0]
                
                if fcurve.array_index == 0:
                    RotKeyFrames.append(int(frame))
    print(LocKeyFrames,RotKeyFrames)
    
    for LOC in range(FrameCount+1):
        bpy.context.scene.frame_set(LOC)
        LOCATION = Camera.location
        LocAnim.append(((LOCATION.x*scale),((LOCATION.z*scale)),LOCATION.y*scale))
    
    for LEN in range(FrameCount+1):
        bpy.context.scene.frame_set(LEN)
        LENS = Camera.data.lens
        SnsorWidth = Camera.data.sensor_width
        radian = 2*math.degrees(math.atan((6*SnsorWidth)/ (LENS)))
        Degree = radian
        FovAnim.append(int((Degree*100)))
    
    print(FovAnim)
    
    for ROT in range(FrameCount+1):
        bpy.context.scene.frame_set(ROT)
        ROTATION = Camera.rotation_quaternion
        CAMLOC = Camera.location
        INVROT = ROTATION
        TARGETFACE = INVROT @ Vector((0.0,0.0,1.0))
        distance = -2
        targetloc = CAMLOC + TARGETFACE * distance
        RotAnim.append(((targetloc[0]*scale)*flip,(targetloc[1]*scale)*flip,(targetloc[2]*scale)))
    
    writer = BinaryReader()
    writer.write_str("MTBW")
    writer.write_uint32(1)
    writer.pad(24)
    writer.write_uint32(32)
    writer.write_uint32(0)
    writer.write_uint32(3)
    writer.pad(4)
    writer.write_uint32(FrameCount+1)
    writer.write_uint32(1)
    writer.write_uint32(0)
    writer.write_uint32(11)
    Count = 0
    for i in LocKeyFrames:
        writer.write_float(LocAnim[i][0]*flip)
        writer.write_float(LocAnim[i][1])
        writer.write_float(LocAnim[i][2]*flip)
        writer.pad(4)
        Count+=1
    for f in RotKeyFrames:
        writer.write_float(RotAnim[f][0])
        writer.write_float(RotAnim[f][2])
        writer.write_float(RotAnim[f][1])
        writer.write_float(0)
        Count+=1
        
    FOVCOUNT = 0
    for g in range(FrameCount+1):
        writer.pad(4)
        writer.write_uint32(FovAnim[g])
        writer.pad(8)
        Count+=1
        FOVCOUNT +=1
    KeyFrameOffset = writer.pos()-32
    for key1 in LocKeyFrames:
        writer.write_uint16(key1)
    for key2 in RotKeyFrames:
        writer.write_uint16(key2)
    for key3 in range(FOVCOUNT):
        writer.write_uint16(key3)
    writer.align(0x10)
    writer.seek(36)
    writer.write_uint32(KeyFrameOffset)
    writer.seek(56)
    writer.write_uint32(Count)
    MTBW = open(filepath, 'wb')
    MTBW.write(writer.buffer())
    MTBW.close()

    return{'FINISHED'} 