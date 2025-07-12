import sys
import importlib
import bpy
# fmt:off
modules = (
    "essential_brush_saver._config",
)
for mod_name in modules:
    if mod_name in sys.modules:
        importlib.reload(sys.modules[mod_name])
    else:
        __import__(mod_name)
from . import _config
# fmt:on


class EBS_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout.row()
        layout.alignment = "RIGHT"
        layout.operator(EBS_OT_Reset.bl_idname)


class EBS_OT_Reset(bpy.types.Operator):
    bl_idname = "ebs.reset"
    bl_label = "Clear Saved Brush Settings"

    def execute(self, context):
        _config.get_data().clear()
        _config.save()
        return {'FINISHED'}


classes = (
    EBS_AddonPreferences,
    EBS_OT_Reset,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
