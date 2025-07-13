import sys
import importlib
import bpy
import os
# fmt:off
modules = (
    "essential_brush_saver._preference",
    "essential_brush_saver._config",
    "essential_brush_saver._sculpt_brush",
    "essential_brush_saver._vertex_brush",
    "essential_brush_saver._g",
)
for mod_name in modules:
    if mod_name in sys.modules:
        importlib.reload(sys.modules[mod_name])
    else:
        __import__(mod_name)
from . import _config, _preference, _g, _sculpt_brush, _vertex_brush
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
    def __load(module, data):
        # print("[Essential Brush Saver] The following warning logs are required to apply brush settings!")
        for key in data.keys():
            result = bpy.ops.brush.asset_activate(
                asset_library_type="ESSENTIALS",
                asset_library_identifier="",
                relative_asset_identifier=os.path.join(module.relative_asset_path, key))
            brush = next((b for b in bpy.data.brushes if b.name == key and module.is_mode_match(b)), None)
            if brush:
                for attr in module.attributes:
                    if hasattr(brush, attr.split(".")[0]):
                        # print(key, attr, "has attribute, ", sculpt_data[key].get(attr, getattr_nested(brush, attr)))
                        setattr_nested(brush, attr, data[key].get(attr, getattr_nested(brush, attr)))
                _g.print("[Essential Brush Saver] load:", module.__name__.split(".")[-1], key, result)
    config = _config.get_data()
    __load(_sculpt_brush, config.get("sculpt", {}))
    __load(_vertex_brush, config.get("vertex", {}))


def save():
    def __save(module, data):
        brush_names = []
        with bpy.data.libraries.load(module.abs_asset_path, link=False, assets_only=True) as (data_from, data_to):
            brush_names = data_from.brushes[:]
        r = False
        for brush_name in brush_names:
            brush = next((b for b in bpy.data.brushes if b.name == brush_name and module.is_mode_match(b)), None)
            if brush:
                r = True
                brush_data = data.setdefault(brush.name, {})
                for attr in module.attributes:
                    if hasattr(brush, attr.split(".")[0]):
                        brush_data[attr] = getattr_nested(brush, attr)
                        # print(attr, brush_data[attr])
                _g.print("[Essential Brush Saver] save: ", module.__name__.split(".")[-1], brush.name)
        return r
    r = False
    config = _config.get_data()
    r |= __save(_sculpt_brush, config.setdefault("sculpt", {}))
    r |= __save(_vertex_brush, config.setdefault("vertex", {}))
    print(r)
    if r:
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
            bpy.app.timers.register(delay_start, first_interval=1.0, persistent=True)
    except Exception as e:
        print(e)


def unregister():
    _preference.unregister()
    try:
        bpy.app.handlers.save_post.remove(on_save_post)
    except ValueError:
        pass
