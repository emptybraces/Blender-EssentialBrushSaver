import importlib
import bpy
import os
from . import (
    _preference,
    _config,
    _b_sculpt,
    _b_vertex,
    _b_weight,
    _b_image,
    _g,
)
for m in (
    _preference,
    _config,
    _b_sculpt,
    _b_vertex,
    _b_weight,
    _b_image,
    _g,
):
    importlib.reload(m)

bl_info = {
    "name": "Essential Brush Saver",
    "author": "emptybraces",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "",
    "description": "Automatically save and load essential brush settings",
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
            if "CANCELLED" in result:
                return False
            brush = next((b for b in bpy.data.brushes if b.name == key and module.is_mode_match(b)), None)
            if brush:
                for attr in module.attributes:
                    if hasattr(brush, attr.split(".")[0]):
                        # print(key, attr, "has attribute, ", sculpt_data[key].get(attr, getattr_nested(brush, attr)))
                        setattr_nested(brush, attr, data[key].get(attr, getattr_nested(brush, attr)))
                _g.print("[Essential Brush Saver] Load:", module.__name__.split(".")[-1], key, result)
        return True
    config = _config.get_data()
    bpy.ops.object.mode_set(mode="SCULPT")
    if not __load(_b_sculpt, config.get("sculpt", {})):
        return False
    bpy.ops.object.mode_set(mode="VERTEX_PAINT")
    if not __load(_b_vertex, config.get("vertex", {})):
        return False
    bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
    if not __load(_b_weight, config.get("weight", {})):
        return False
    bpy.ops.object.mode_set(mode="TEXTURE_PAINT")
    if not __load(_b_image, config.get("image", {})):
        return False
    return True


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
                _g.print("[Essential Brush Saver] Save: ", module.__name__.split(".")[-1], brush.name)
        return r
    r = False
    config = _config.get_data()
    bpy.ops.object.mode_set(mode="SCULPT")
    r |= __save(_b_sculpt, config.setdefault("sculpt", {}))
    bpy.ops.object.mode_set(mode="VERTEX_PAINT")
    r |= __save(_b_vertex, config.setdefault("vertex", {}))
    bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
    r |= __save(_b_weight, config.setdefault("weight", {}))
    bpy.ops.object.mode_set(mode="TEXTURE_PAINT")
    r |= __save(_b_image, config.setdefault("image", {}))
    if r:
        _config.save()
    return True


def on_save_post(dummy):
    saveload_procedure(save)


def saveload_procedure(procedure):
    # 状態を保存
    original_objects = list(bpy.context.view_layer.objects.selected)
    original_active = bpy.context.view_layer.objects.active
    original_mode = original_active.mode if original_active else "OBJECT"
    # オブジェクトモードで行うこと
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    for obj in bpy.data.objects:
        obj.select_set(False)
    bpy.context.view_layer.objects.active = None
    # ダミーオブジェクト作成
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0, 0))
    temp_obj = bpy.context.active_object
    temp_is_cube = temp_obj and temp_obj.type == "MESH" and len(temp_obj.data.vertices) == 8
    if temp_is_cube:
        temp_obj.name = "ESSENTIAL_BRUSH_SAVER_TEMP"

    try:
        r = procedure()
    finally:
        if original_active:
            for i in original_objects:
                i.select_set(True)
            bpy.context.view_layer.objects.active = original_active
        if bpy.context.mode != original_mode:
            bpy.ops.object.mode_set(mode=original_mode)
        if temp_is_cube:
            bpy.data.objects.remove(temp_obj, do_unlink=True)
        return r


def delay_start():
    if on_save_post not in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(on_save_post)
    if not saveload_procedure(load):
        print("[Essential Brush Saver] Retry loading...")
        return 1.0
    print("[Essential Brush Saver] Load finished!")
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
            bpy.app.timers.register(delay_start, first_interval=1.5, persistent=True)
    except Exception as e:
        print(e)


def unregister():
    _preference.unregister()
    try:
        bpy.app.handlers.save_post.remove(on_save_post)
    except ValueError:
        pass
