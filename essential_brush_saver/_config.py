import bpy
import os
import json
from mathutils import Vector, Color
g_data = {}


def get_path_dir():
    # エクステンションでの保存先
    path = __package__ if __package__ != "essential_brush_saver" else "bl_ext.user_default.essential_brush_saver"
    return bpy.utils.extension_path_user(path, create=True)
    # アドオンでの保存先
    # return bpy.utils.user_resource("SCRIPTS", path=f"addons/{__package__}", create=True)


def get_path_data():
    return os.path.join(get_path_dir(), "Essential_Brush_Saver.json")


def get_data():
    global g_data

    if g_data:
        return g_data
    try:
        path = get_path_data()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                g_data = json.load(f)
        else:
            g_data = {}
    except (json.JSONDecodeError, OSError) as e:
        print(f"[Essential Brush Saver] Failed to load config file: {e}")
    return g_data


def save():
    def __encoder(obj):
        if isinstance(obj, (Vector, Color, bpy.types.bpy_prop_array)):
            return list(obj)
        return str(obj)
    try:
        path = get_path_data()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(g_data, f, default=__encoder, indent=2)
    except (OSError, TypeError) as e:
        print(f"[Essential Brush Saver] Failed to save config file: {e}")
