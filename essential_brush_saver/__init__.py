import os
if "bpy" in locals():
    import importlib
    for m in [
        _preference,
        _config,
        _b_sculpt,
        _b_vertex,
        _b_weight,
        _b_image,
        _g,
    ]:
        importlib.reload(m)
else:
    import bpy
    from . import (
        _preference,
        _config,
        _b_sculpt,
        _b_vertex,
        _b_weight,
        _b_image,
        _g,
    )

bl_info = {
    "name": "Essential Brush Saver",
    "author": "emptybraces",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "",
    "description": "Automatically save and load essential brush settings",
    "warning": "",
    "doc_url": "",
    "category": "",
}


ignore_brush_properties = [
    "name",
    "use_fake_user",
    "use_extra_user",
    "is_runtime_data",
    "asset_data",
]


def load():
    def __load(brush_category, relative_path, attr_use_mode):
        # print("[Essential Brush Saver] The following warning logs are required to apply brush settings!")
        config = _config.get_data()
        brush_dict = config.get(brush_category, {})
        print(brush_category, brush_dict.keys())
        for brush_name in brush_dict.keys():
            result = bpy.ops.brush.asset_activate(
                asset_library_type="ESSENTIALS",
                asset_library_identifier="",
                relative_asset_identifier=os.path.join(relative_path, brush_name))
            _g.print("[Essential Brush Saver] Load:", brush_category, brush_name, result)
            if "CANCELLED" in result:
                return False
            brush = next((b for b in bpy.data.brushes if b.name == brush_name and getattr(b, attr_use_mode, False)), None)
            if brush:
                data = brush_dict[brush_name]
                for p in brush.bl_rna.properties:
                    if not p.is_readonly and p.identifier not in ignore_brush_properties:
                        # POINTERがNoneの値は書き込みしないようにしてる
                        if (value := data.get(p.identifier, None)) is None:
                            continue
                        # b = C.tool_settings.sculpt.brush
                        # {prop.identifier: (getattr(b, prop.identifier), prop.subtype) for prop in b.bl_rna.properties if not prop.is_readonly and prop.type == "POINTER"}
                        if p.identifier == "texture" or p.identifier == "mask_texture":
                            setattr(brush, p.identifier, bpy.data.textures.get(value))
                            continue
                        if p.identifier == "paint_curve":
                            setattr(brush, p.identifier, bpy.data.paint_curves.get(value))
                            continue
                        setattr(brush, p.identifier, value)
        return True
    # --
    bpy.ops.object.mode_set(mode="SCULPT")
    if not __load("sculpt", os.path.join("brushes", "essentials_brushes-mesh_sculpt.blend", "Brush"), "use_paint_sculpt"):
        _g.print("[Essential Brush Saver] Failed to load any sculpt brush")
        return False
    bpy.ops.object.mode_set(mode="VERTEX_PAINT")
    if not __load("vertex", os.path.join("brushes", "essentials_brushes-mesh_vertex.blend", "Brush"), "use_paint_vertex"):
        _g.print("[Essential Brush Saver] Failed to load any vertex paint brush")
        return False
    bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
    if not __load("weight", os.path.join("brushes", "essentials_brushes-mesh_weight.blend", "Brush"), "use_paint_weight"):
        _g.print("[Essential Brush Saver] Failed to load any weight paint brush")
    bpy.ops.object.mode_set(mode="TEXTURE_PAINT")
    if not __load("image", os.path.join("brushes", "essentials_brushes-mesh_texture.blend", "Brush"), "use_paint_image"):
        _g.print("[Essential Brush Saver] Failed to load any image paint brush")
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
    original_objects = [i for i in bpy.context.view_layer.objects.selected if i != None]
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
    # 確実に大丈夫かどうか念のために確認
    temp_is_cube = temp_obj and temp_obj.type == "MESH" and len(temp_obj.data.vertices) == 8
    if temp_is_cube:
        temp_obj.name = "ESSENTIAL_BRUSH_SAVER_TEMP"

    r = False
    try:
        if temp_is_cube:
            r = procedure()
    except Exception as e:
        print(f"[Essential Brush Saver] Exception during save/load procedure: {e}")
        r = False
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


load_retry_cnt = 0


def delay_start():
    if on_save_post not in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(on_save_post)
    if not saveload_procedure(load):
        global load_retry_cnt
        load_retry_cnt += 1
        print(f"[Essential Brush Saver] Retry loading...{load_retry_cnt}")
        if load_retry_cnt == 20:
            print("[Essential Brush Saver] Too many load failures. Something is wrong, aborting.")
            return None
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
