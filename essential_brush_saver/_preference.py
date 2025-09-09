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
        c = self.layout.column(align=True)
        r = c.row()
        r.alignment = "RIGHT"
        r.label(text="DataFile Path: " + _config.get_path_data())
        r.operator(EBS_OT_OpenFolder.bl_idname)
        r = c.row()
        r.alignment = "RIGHT"
        r.operator(EBS_OT_Reset.bl_idname)

        import os
        r = c.row()
        config = _config.get_data()
        path = os.path.join(bpy.utils.system_resource("DATAFILES"), "assets", "brushes")
        for i in (
            ("sculpt", os.path.join(path, "essentials_brushes-mesh_sculpt.blend")),
            ("vertex", os.path.join(path, "essentials_brushes-mesh_vertex.blend")),
            ("weight", os.path.join(path, "essentials_brushes-mesh_weight.blend")),
            ("image", os.path.join(path, "essentials_brushes-mesh_texture.blend")),
        ):
            b = r.box()
            cc = b.column(align=True)
            cc.label(text=i[0] + " brushes:")
            cc.separator()
            brush_dict = config.get(i[0], {})
            savedata_brush_names = brush_dict.keys()
            for brush_name in savedata_brush_names:
                brush = bpy.data.brushes[brush_name, i[1]]
                if brush:
                    # s = cc.row().split(factor=0.9)
                    # s.row().label(text=brush_name)
                    # op = s.row().operator(EBS_OT_Remove.bl_idname, text="X")
                    rr = cc.row(align=True)
                    rr.alignment = "RIGHT"
                    rr.label(text=brush_name)
                    op = rr.operator(EBS_OT_Remove.bl_idname, text="X")
                    op.category = i[0]
                    op.brush_name = brush_name


class EBS_OT_Reset(bpy.types.Operator):
    bl_idname = "ebs.reset"
    bl_label = "Clear Saved Brush Settings"

    def execute(self, context):
        _config.get_data().clear()
        _config.save()
        return {'FINISHED'}


class EBS_OT_Remove(bpy.types.Operator):
    bl_idname = "ebs.remove"
    bl_label = "Remove Saved Brush Settings"
    category: bpy.props.StringProperty()
    brush_name: bpy.props.StringProperty()

    def execute(self, context):
        config = _config.get_data()
        brush_dict = config.get(self.category, {})
        brush_dict.pop(self.brush_name, None)
        _config.save()
        return {'FINISHED'}


class EBS_OT_OpenFolder(bpy.types.Operator):
    bl_idname = "ebs.open_folder"
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
    EBS_OT_Remove,
    EBS_OT_OpenFolder,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
