import bpy
from .binary_reader import BinaryReader


def import_MTBW(context, filepath):

    MTBW = open (filepath,"rb")
    reader = BinaryReader(MTBW.read())
    reader.seek(32)
    
    DataOffset = reader.read_uint32()+32
    print(DataOffset)
    KeyframeTableOffset = reader.read_uint32()+32
    reader.seek(48)
    FrameCount = reader.read_uint32()
    reader.seek(KeyframeTableOffset)
    Keyframes = {}
    for ducttape in range(3):
        Keyframes[ducttape]=[]
        for i  in range(100000):
            
            Keyframe = reader.read_uint16()
            Keyframes[ducttape].append(Keyframe)
            if i!=0 and Keyframe==0:
                reader.seek(reader.pos()-2)
                break
    print(Keyframes)
    
    reader.seek(DataOffset)
    Data1 = []
    Data2 = []
    Data3 = []
    for e in range(len(Keyframes[0])-1):
        print(reader.pos())
        POSX = reader.read_float()
        POSY = reader.read_float()
        POSZ = reader.read_float()
        pad = reader.read_float()
        Data1.append((POSX,POSZ,POSY))
    for g in range(len(Keyframes[1])-1):
        POSX = reader.read_float()
        POSY = reader.read_float()
        POSZ = reader.read_float()
        pad = reader.read_float()
        Data2.append((POSX,POSZ,POSY))
    for f in range(len(Keyframes[2])-1):
        POSX = reader.read_float()
        POSY = reader.read_float()
        POSZ = reader.read_float()
        pad = reader.read_float()
        Data3.append((POSX,POSY,POSZ))

    
    cameraname = "MTBW"
    MTBWCAM = bpy.data.cameras.new(name = cameraname)
    CAMOBJ = bpy.data.objects.new(f"{cameraname}_CAM",MTBWCAM)
    CAMOBJ.data =MTBWCAM
    bpy.context.collection.objects.link(CAMOBJ)
    
    targetname = (f"MTBWtarget")
    targetobj = bpy.data.objects.new(targetname,None)
    bpy.context.collection.objects.link(targetobj)
    
    lookatthat =  CAMOBJ.constraints.new('TRACK_TO')
    lookatthat.target = targetobj
    lookatthat.track_axis = 'TRACK_NEGATIVE_Z'
    lookatthat.up_axis = 'UP_Y'

    for frames in range(len(Keyframes[0])-1):
        
        pos = Data1[frames]
        bpy.context.scene.frame_set(Keyframes[0][frames])
        CAMOBJ.location = pos
        CAMOBJ.keyframe_insert(data_path="location",frame=(Keyframes[0][frames]))
        
    for frames2 in range(len(Keyframes[1])-1):
        
        target = Data2[frames2]
        bpy.context.scene.frame_set(Keyframes[1][frames2])
        targetobj.location = target
        targetobj.keyframe_insert(data_path="location",frame=(Keyframes[1][frames2]))
    
    bpy.context.scene.camera = CAMOBJ
    
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = FrameCount
    
    MTBW.close()
    return{'FINISHED'} 