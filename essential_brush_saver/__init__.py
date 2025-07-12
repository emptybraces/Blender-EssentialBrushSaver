import sys
import importlib
import bpy
import os
# fmt:off
modules = (
    "essential_brush_saver._preference",
    "essential_brush_saver._config",
    "essential_brush_saver._sculpt_brush",
    "essential_brush_saver._g",
)
for mod_name in modules:
    if mod_name in sys.modules:
        importlib.reload(sys.modules[mod_name])
    else:
        __import__(mod_name)
from . import _config, _preference, _sculpt_brush, _g
# fmt:on

bl_info = {
    "name": "Essential Brush Saver",
    "author": "emptybraces",
    "version": (1, 0, 0),
    "blender": (4, 4, 0),
    "location": "",
    "description": "Save and load settings of essential brushes such as size and strength",
    "warning": "",
    "doc_url": "",
    "category": "",
}


def load():
    current_brush = bpy.context.tool_settings.sculpt.brush
    config = _config.get_data()
    sculpt_data = config.get("sculpt", {})
    load_requests = [key for key in sculpt_data.keys() if bpy.data.brushes.get(key) is None]
    if current_brush and current_brush.name in sculpt_data:
        load_requests.append(current_brush.name)
    # print(bpy.context.mode, current_brush, load_requests)
    if load_requests:
        # print("[Essential Brush Saver] The following warning logs are required to apply brush settings!")
        for key in load_requests:
            result = bpy.ops.brush.asset_activate(
                asset_library_type="ESSENTIALS",
                asset_library_identifier="",
                relative_asset_identifier=os.path.join("brushes", "essentials_brushes-mesh_sculpt.blend", "Brush", key))
            brush = bpy.data.brushes.get(key)
            # print("load", key, result, brush)
            if brush:
                for attr in _sculpt_brush.attributes:
                    if hasattr(brush, attr.split(".")[0]):
                        # print(key, attr, "has attribute, ", sculpt_data[key].get(attr, getattr_nested(brush, attr)))
                        setattr_nested(brush, attr, sculpt_data[key].get(attr, getattr_nested(brush, attr)))
                _g.print("[Essential Brush Saver] Brush param load:", key)
    # for area in bpy.context.screen.areas:
    #     if area.type == 'VIEW_3D':
    #         area.tag_redraw()


def save():
    path = os.path.join(bpy.utils.system_resource("DATAFILES"), "assets", "brushes", "essentials_brushes-mesh_sculpt.blend")
    brush_names = []
    with bpy.data.libraries.load(path, link=False, assets_only=True) as (data_from, data_to):
        brush_names = data_from.brushes[:]
    is_save = False
    for i in brush_names:
        if brush := bpy.data.brushes.get(i):
            is_save = True
            config = _config.get_data()
            brushes = config.setdefault("sculpt", {})
            brush_data = brushes.setdefault(brush.name, {})
            for attr in _sculpt_brush.attributes:
                # if brush == "Paint Soft":
                #     print(brush.name, attr, hasattr(brush, attr.split(".")[0]))
                if hasattr(brush, attr.split(".")[0]):
                    brush_data[attr] = getattr_nested(brush, attr)
                    # print(attr, brush_data[attr])
            _g.print("save: ", brush.name)
    if is_save:
        _config.save()


def on_save_post(dummy):
    run_in_sculpt_mode(save)


def run_in_sculpt_mode(procedure):
    original_objects = bpy.context.selected_objects.copy()
    original_active = bpy.context.active_object
    original_mode = original_active.mode if original_active else "OBJECT"

    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0, 0))
    temp_obj = bpy.context.active_object
    temp_obj.name = "ESSENTIAL_BRUSH_SAVER_TEMP"

    try:
        bpy.ops.object.mode_set(mode="SCULPT")
        procedure()
    finally:
        if original_active:
            for i in original_objects:
                i.select_set(True)
            bpy.context.view_layer.objects.active = original_active
        bpy.ops.object.mode_set(mode=original_mode)
        bpy.data.objects.remove(temp_obj, do_unlink=True)


def delay_start():
    if on_save_post not in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(on_save_post)
    run_in_sculpt_mode(load)
    return None


def setattr_nested(obj, attr_chain, value):
    attrs = attr_chain.split(".")
    for attr in attrs[:-1]:
        if not hasattr(obj, attr):
            return
        obj = getattr(obj, attr)
        if obj is None:
            return
    setattr(obj, attrs[-1], value)


def getattr_nested(obj, attr_chain, default=None):
    attrs = attr_chain.split(".")
    for attr in attrs:
        if not hasattr(obj, attr):
            return default
        obj = getattr(obj, attr)
        if obj is None:
            return default
    return obj


def register():
    _preference.register()
    try:
        if not bpy.app.timers.is_registered(delay_start):
            bpy.app.timers.register(delay_start, first_interval=0.5, persistent=True)
    except Exception as e:
        print(e)


def unregister():
    _preference.unregister()
    try:
        bpy.app.handlers.save_post.remove(on_save_post)
    except ValueError:
        pass
