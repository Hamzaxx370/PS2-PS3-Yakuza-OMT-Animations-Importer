bl_info = {
    "name": "PS2/PS3 OMT",
    "author": "Hamzaxx369",
    "version": (1, 0, 0),
    "blender": (2, 81, 6),
    "location": "File > Import-Export",
    "description": "OMT Animation Importer.Meant to be used along with Gabe Hens's OME Importer",
    "warning": "",
    "doc_url": "",
    "category": "Import",
}


if "bpy" in locals():
    import importlib
    
    if "OMT_import" in locals():
        importlib.reload(OMT_import) 
    if "OMT_AUTH_import" in locals():
        importlib.reload(OMT_AUTH_import) 
    if "OMT_export" in locals():
        importlib.reload(OMT_export) 
    if "MTBW_import" in locals():
        importlib.reload(MTBW_import) 
    if "MTBW_export" in locals():
        importlib.reload(MTBW_export) 
    if "binaryreader" in locals():
        importlib.reload(binaryreader)
  

import bpy
from mathutils import *
from .binary_reader import BinaryReader 

from .OMT_import import import_omt

from .OMT_AUTH_import  import import_omt_auth

from .OMT_export import export_omt

from .MTBW_import import import_MTBW

from .MTBW_export import export_MTBW
  

  
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
import bmesh

   
class ImportOMT(Operator, ImportHelper):
    
    bl_idname = "import_testomt.some_data3333"
    bl_label = "Import Some Data33333"

    
    filename_ext = ".dat"

    filter_glob: StringProperty(
        default="*.dat;*.omt",
        options={'HIDDEN'},
        maxlen=255,  
    )


    CenterImport: BoolProperty(
            name="Import Location Bone Movements",
            description="",
            default=True,
    )
    
    

    def execute(self, context):
        
        return import_omt(context, self.filepath,self.CenterImport)
    
class ImportAUTHOMT(Operator, ImportHelper):
    
    bl_idname = "import_authomt.some_data4444"
    bl_label = "Import Some Data4444"

    
    filename_ext = ".dat"

    filter_glob: StringProperty(
        default="*.dat;*.omt",
        options={'HIDDEN'},
        maxlen=255,  
    )
    
    BodyFaceFix: BoolProperty(
        name="Connect Face And Body",
        description="",
        default=False,
    )
    ExistingArmatures:EnumProperty(
        name="Select Armature",
        description="",
        items = lambda self,context:[(obj.name,obj.name,"")for obj in context.scene.objects if obj.type== 'ARMATURE']
        
    )
    
    def draw(self,context):
        layout = self.layout
        layout.prop(self,"BodyFaceFix")
        if self.BodyFaceFix:
            layout.prop(self,"ExistingArmatures")


    
    

    def execute(self, context):
        
        if self.BodyFaceFix:
            BodyName = self.ExistingArmatures
            BodyArmature = bpy.data.objects.get(BodyName)
        else:
            BodyArmature = "None"
        
        return import_omt_auth(context, self.filepath,BodyArmature)
        
    

    
class ImportMTBW(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_mtbw.mtbw_data"  
    bl_label = "Import MTBW"

    
    filename_ext = ".MTBW"

    filter_glob: StringProperty(
        default="*.MTBW",
        options={'HIDDEN'},
        maxlen=255,  
    )
    
    ISCUTSCENE: BoolProperty(
        name="Is Cutscene",
        description="",
        default=False,
    )
    SMOLL: BoolProperty(
        name="Scale to OOE",
        description="",
        default=False,
    )
    
    
    
    

    def execute(self, context):
        
        return import_MTBW(context, self.filepath,self.ISCUTSCENE,self.SMOLL)
    
    
    
class ExportMTBW(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_mtbw.mtbw_data"  
    bl_label = "Export MTBW"

    
    filename_ext = ".MTBW"

    filter_glob: StringProperty(
        default="*.MTBW",
        options={'HIDDEN'},
        maxlen=255,  
    )
    
    BIG: BoolProperty(
        name="Scale to PS2",
        description="",
        default=False,
    )
    FLIP: BoolProperty(
        name="Flip to PS2",
        description="",
        default=False,
    )
    
    
    
    
    

    def execute(self, context):
        
        return export_MTBW(context, self.filepath,self.BIG,self.FLIP)
    
class ExportOMT(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_omt.omt_data"  
    bl_label = "Export"

    
    filename_ext = ".dat"

    filter_glob: StringProperty(
        default="*.dat",
        options={'HIDDEN'},
        maxlen=255,  
    )
    
    Scale : bpy.props.FloatVectorProperty(
        name="Center Scale Multiplier (XZY)",
        description="Fixes Center Scale (Use 100 for OOE)",
        default=(1.0,1.0,1.0),
        size=3,
        min = 1.0,
    )
    ScaleHeight : bpy.props.FloatProperty(
        name="Adjust Center Height",
        description="",
        default=0.0,
    )
    DEBULLSHIT: BoolProperty(
        name="Fix DE Center",
        description="",
        default=False,
    )
    ISYACT: BoolProperty(
        name="Export HACT",
        description="",
        default=False,
    )
    
    
    

    def execute(self, context):
        props = context.scene.tool
        PatternData = []
        PatternFrames = []
        for pattern in props.patterns:
            PatternData.append((pattern.lefthand,pattern.righthand,pattern.head))
            PatternData.append((pattern.lefthand+0.10,pattern.righthand+0.10,pattern.head+0.10))
            PatternFrames.append(pattern.frame)
            PatternFrames.append(pattern.frame1)
        
        return export_omt(context, self.filepath,PatternData,PatternFrames,self.Scale,self.ScaleHeight,self.DEBULLSHIT,self.ISYACT)
    
class Patterns(bpy.types.PropertyGroup):
    
    lefthand: bpy.props.FloatProperty(name="Left Hand",default=0.0)
    righthand: bpy.props.FloatProperty(name="Right Hand",default=0.0)
    head: bpy.props.FloatProperty(name="Head",default=0.0)
    frame: bpy.props.FloatProperty(name="Start Frame",default=0)
    frame1: bpy.props.FloatProperty(name="End Frame",default=0)
    
class Properties(bpy.types.PropertyGroup):
    patterns: bpy.props.CollectionProperty(type=Patterns)

class AddPattern(bpy.types.Operator):
    bl_idname = "pattern.add"
    bl_label = "Add Pattern"
    index:bpy.props.IntProperty()
    
        
    
    def execute(self,context):
        props= context.scene.tool
        new = props.patterns.add()
        new.frame= len(props.patterns)
        return {'FINISHED'}

class RemovePattern(bpy.types.Operator):
    bl_idname = "pattern.remove"
    bl_label = "Remove Pattern"
    index= bpy.props.IntProperty()
    def execute(self,context):
        props = context.scene.tool
        
        props.patterns.remove(self.index)
        return {'FINISHED'}

class PatternPan(bpy.types.Panel):
    
    bl_idname = "pattern.stuff"
    bl_label = "Pattern Control"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    
    def draw(self,context):
        layout= self.layout
        props = context.scene.tool
        layout.operator(AddPattern.bl_idname,text="Add Pattern")
        for index,pattern in enumerate(props.patterns):
            box= layout.box()
            box.label(text=f"Pattern {index+1}")
            box.prop(pattern,"lefthand",text="Left Hand Pattern")
            box.prop(pattern,"righthand",text="Right Hand Pattern")
            box.prop(pattern,"head",text="Head Pattern")
            box.prop(pattern,"frame",text="Frame Start")
            box.prop(pattern,"frame1",text="Frame End")
            remove=box.operator(RemovePattern.bl_idname,text="Remove")
            RemovePattern.index = index
            
    

def menu_func_importOMT(self, context):
    self.layout.operator(ImportOMT.bl_idname, text="PS2/PS3 .OMT(Animation)")
    
def menu_func_importAUTHOMT(self, context):
    self.layout.operator(ImportAUTHOMT.bl_idname, text="PS2/PS3 .OMT(Auth Face Animation)")
    
def menu_func_importMTBW(self, context):
    self.layout.operator(ImportMTBW.bl_idname, text="PS2/PS3 .MTBW (Camera Angle)")
    
def menu_func_exportOMT(self, context):
    self.layout.operator(ExportOMT.bl_idname, text="PS2/PS3 OMT Export")
    
def menu_func_exportMTBW(self, context):
    self.layout.operator(ExportMTBW.bl_idname, text="PS2/PS3 MTBW Export")
    
    
    

def register():
    
    bpy.utils.register_class(ImportOMT)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_importOMT)
    
    bpy.utils.register_class(ImportAUTHOMT)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_importAUTHOMT)
    
    bpy.utils.register_class(ImportMTBW)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_importMTBW)
    
    bpy.utils.register_class(ExportOMT)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_exportOMT)
    
    bpy.utils.register_class(ExportMTBW)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_exportMTBW)
    
    bpy.utils.register_class(Patterns)
    bpy.utils.register_class(RemovePattern)
    bpy.utils.register_class(Properties)
    bpy.utils.register_class(AddPattern)
    bpy.utils.register_class(PatternPan)
    bpy.types.Scene.tool = bpy.props.PointerProperty(type=Properties)
    
    


def unregister():
    
    bpy.utils.unregister_class(ImportOMT)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_importOMT)
    
    bpy.utils.unregister_class(ImportAUTHOMT)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_importAUTHOMT)
    
    bpy.utils.unregister_class(ImportMTBW)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_importMTBW)
    
    bpy.utils.unregister_class(ExportOMT)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_exportOMT)
    
    bpy.utils.unregister_class(ExportMTBW)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_exportMTBW)
    
    
    bpy.utils.unregister_class(Patterns)
    bpy.utils.unregister_class(RemovePattern)
    bpy.utils.unregister_class(Properties)
    bpy.utils.unregister_class(AddPattern)
    bpy.utils.unregister_class(PatternPan)
    
    del bpy.types.Scene.tool
    
    
    




