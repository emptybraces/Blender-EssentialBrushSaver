import bpy
import os
import json
from mathutils import Vector, Color


g_data = {}


def get_data_path():
    config_dir = bpy.utils.user_resource("CONFIG", path="", create=True)
    return os.path.join(config_dir, "Essential_Brush_Saver.json")


def get_data():
    global g_data

    if g_data:
        return g_data
    try:
        path = get_data_path()
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
        if isinstance(obj, (Vector, Color)):
            return list(obj)
        return str(obj)
    try:
        path = get_data_path()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(g_data, f, default=__encoder, indent=2)
    except (OSError, TypeError) as e:
        print(f"[Essential Brush Saver] Failed to save config file: {e}")
