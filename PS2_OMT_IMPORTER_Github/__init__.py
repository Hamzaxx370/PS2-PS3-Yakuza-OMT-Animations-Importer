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
    if "OMT_export" in locals():
        importlib.reload(OMT_export) 
    if "MTBW_import" in locals():
        importlib.reload(MTBW_import) 
    if "binaryreader" in locals():
        importlib.reload(binaryreader)
  

import bpy
from mathutils import *
from .binary_reader import BinaryReader 

from .OMT_import import import_omt

from .OMT_export import export_omt

from .MTBW_import import import_MTBW
  

  
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
            name="Import Center Bone Movements",
            description="",
            default=True,
    )
    Y2Sup: BoolProperty(
            name="Import Yakuza 2 Animations",
            description="",
            default=False,
    )
    
    ShortFrames: BoolProperty(
            name="More Than 255 Frames",
            description="",
            default=False,
    )

    def execute(self, context):
        
        return import_omt(context, self.filepath,self.CenterImport,self.Y2Sup,self.ShortFrames)
    
    
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
    
    
    
    

    def execute(self, context):
        
        return import_MTBW(context, self.filepath)
    
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
    
    
    
    

    def execute(self, context):
        
        return export_omt(context, self.filepath)


def menu_func_importOMT(self, context):
    self.layout.operator(ImportOMT.bl_idname, text="PS2/PS3 .OMT(Animation)")
    
def menu_func_importMTBW(self, context):
    self.layout.operator(ImportMTBW.bl_idname, text="PS2/PS3 .MTBW (Camera Angle)")
    
def menu_func_exportOMT(self, context):
    self.layout.operator(ExportOMT.bl_idname, text="PS2/PS3 OMT Export")
    
    
    

def register():
    
    bpy.utils.register_class(ImportOMT)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_importOMT)
    
    bpy.utils.register_class(ImportMTBW)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_importMTBW)
    
    bpy.utils.register_class(ExportOMT)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_exportOMT)
    


def unregister():
    
    bpy.utils.unregister_class(ImportOMT)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_importOMT)
    
    bpy.utils.unregister_class(ImportMTBW)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_importMTBW)
    
    bpy.utils.unregister_class(ExportOMT)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_exportOMT)
    
    
    




