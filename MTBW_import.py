import bpy
from .binary_reader import BinaryReader
import math
import mathutils

def import_MTBW(context, filepath,ISCUTSCENE):

    MTBW = open (filepath,"rb")
    reader = BinaryReader(MTBW.read())
    reader.seek(32)
    
    DataOffset = reader.read_uint32()+32
    print(DataOffset)
    KeyframeTableOffset = reader.read_uint32()+32
    reader.seek(48)
    FrameCount = reader.read_uint32()
    reader.seek(60)
    Flag = reader.read_uint32()
    reader.seek(KeyframeTableOffset)
    Keyframes = {}
    for ducttape in range(3):
        Keyframes[ducttape]=[]
        for i  in range(100000):
            
            Keyframe = reader.read_uint16()
            Keyframes[ducttape].append(Keyframe)
            if i!=0 and Keyframe==(FrameCount-1):
                break
    print(Keyframes)
    
    reader.seek(DataOffset)
    Data1 = []
    Data2 = []
    Data3 = []
    for e in range(len(Keyframes[0])):
        print(reader.pos())
        POSX = reader.read_float()
        POSY = reader.read_float()
        POSZ = reader.read_float()
        pad = reader.read_float()
        Data1.append((POSX,POSZ,POSY))
    for g in range(len(Keyframes[1])):
        POSX = reader.read_float()
        POSY = reader.read_float()
        POSZ = reader.read_float()
        QUAT = reader.read_float()
        Data2.append((POSX,POSY,POSZ,QUAT))
    for f in range(len(Keyframes[2])):
        reader.read_uint32()
        FOVVAL = reader.read_uint32()
        reader.read_bytes(8)
        Data3.append(FOVVAL/100)

    if bpy.context.active_object and bpy.context.active_object.select_get():
        CAMOBJ = bpy.context.active_object
        if CAMOBJ.animation_data:
            CAMOBJ.animation_data_clear()
            CAMOBJ.data.animation_data_clear()
        
    else:
        cameraname = "MTBW"
        MTBWCAM = bpy.data.cameras.new(name = cameraname)
        CAMOBJ = bpy.data.objects.new(f"{cameraname}_CAM",MTBWCAM)
        CAMOBJ.data =MTBWCAM
        bpy.context.collection.objects.link(CAMOBJ)

    

    for frames in range(len(Keyframes[0])):
        
        pos = Data1[frames]
        bpy.context.scene.frame_set(Keyframes[0][frames])
        CAMOBJ.location = pos
        CAMOBJ.keyframe_insert(data_path="location",frame=(Keyframes[0][frames]))
        
    if CAMOBJ.type == 'CAMERA':
        SnsorWidth = CAMOBJ.data.sensor_width
        for frames3 in range(len(Keyframes[2])):
            if Data3[frames3]==0:
                pass
            else: 
                FOV = (SnsorWidth/2)/math.tan(math.radians(Data3[frames3])/2)
                bpy.context.scene.frame_set(Keyframes[2][frames3])
                if ISCUTSCENE:
                    CAMOBJ.data.lens= FOV
                else:
                    CAMOBJ.data.lens= FOV*2
                CAMOBJ.data.keyframe_insert(data_path="lens",frame=(Keyframes[2][frames3]))
                
    for frames2 in range(len(Keyframes[1])):
        
        target = (Data2[frames2][0],Data2[frames2][2],Data2[frames2][1])
        Quat = (Data2[frames2][0],Data2[frames2][1],Data2[frames2][3],Data2[frames2][2])
        bpy.context.scene.frame_set(Keyframes[1][frames2])
        LOC = CAMOBJ.location
        Direction = (mathutils.Vector(target) - LOC)*(-1)
        Direction.normalize()
        quat = Direction.to_track_quat('Z','Y')

        if Flag == 11:
            CAMOBJ.rotation_mode = 'QUATERNION'
            CAMOBJ.rotation_quaternion = quat
            CAMOBJ.keyframe_insert(data_path="rotation_quaternion",frame=(Keyframes[1][frames2]))
        
        else:
            CAMOBJ.rotation_mode = 'QUATERNION'
            CAMOBJ.rotation_quaternion = Quat
            CAMOBJ.keyframe_insert(data_path="rotation_quaternion",frame=(Keyframes[1][frames2]))
            
        
        
    
    bpy.context.scene.camera = CAMOBJ
    
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = FrameCount
    
    MTBW.close()
    return{'FINISHED'} 