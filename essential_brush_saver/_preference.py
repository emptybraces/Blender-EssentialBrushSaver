if "bpy" in locals():
    import importlib
    for m in [
        _config,
        _g,
    ]:
        importlib.reload(m)
else:
    import bpy
    from . import (
        _config,
        _g,
    )


class EBS_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        r = self.layout.row()
        r.alignment = "RIGHT"
        r.operator(EBS_OT_Reset.bl_idname)
        r = self.layout.row()
        r.alignment = "RIGHT"
        r.label(text="DataFile Path: " + _config.get_path_data())
        r.operator(EBS_OT_OpenFolder.bl_idname)


class EBS_OT_Reset(bpy.types.Operator):
    bl_idname = "ebs.reset"
    bl_label = "Clear Saved Brush Settings"

    def execute(self, context):
        _config.get_data().clear()
        _config.save()
        return {'FINISHED'}


class EBS_OT_OpenFolder(bpy.types.Operator):
    bl_idname = "ebs.openfolder"
    bl_label = "Open Folder"

    def execute(self, context):
        import platform
        system = platform.system()
        path = _config.get_path_dir()
        if system == "Windows":
            import os
            os.startfile(path)
        elif system == "Darwin":
            import subprocess
            subprocess.Popen(["open", path])
        elif system == "Linux":
            import subprocess
            subprocess.Popen(["xdg-open", path])
        else:
            print(f"Unsupported OS: {system}")
        return {'FINISHED'}


classes = (
    EBS_AddonPreferences,
    EBS_OT_Reset,
    EBS_OT_OpenFolder,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
