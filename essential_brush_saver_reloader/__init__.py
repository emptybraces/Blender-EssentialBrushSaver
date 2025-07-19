import bpy
bl_info = {
    "name": "Essential Brush Saver reloader",
    "author": "emptybraces",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "",
}

addon_name = "essential_brush_saver"
addon_path = "C:/user/projects/github_blender_EssentialBrushSaver/essential_brush_saver.zip"


class OT_Essential_Brush_Saver_Reinstall(bpy.types.Operator):
    bl_idname = "ebs.reinstall"
    bl_label = "Reinstall"

    def execute(self, context):
        if addon_name in context.preferences.addons.keys():
            bpy.ops.preferences.addon_remove(module=addon_name)
            bpy.ops.preferences.addon_refresh()
        bpy.ops.preferences.addon_install(filepath=addon_path)
        bpy.ops.preferences.addon_refresh()
        bpy.ops.preferences.addon_enable(module=addon_name)
        bpy.ops.preferences.addon_refresh()
        self.report({"INFO"}, "[Essential_Brush_Saver] reinstalled!")
        return {'FINISHED'}


addon_keymaps = []


def register():
    bpy.utils.register_class(OT_Essential_Brush_Saver_Reinstall)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(OT_Essential_Brush_Saver_Reinstall.bl_idname, 'Q', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(OT_Essential_Brush_Saver_Reinstall)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
