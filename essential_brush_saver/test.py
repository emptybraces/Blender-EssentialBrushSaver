import os
import bpy
relative_asset_path = os.path.join("brushes", "essentials_brushes-mesh_weight.blend", "Brush")
abs_asset_path = os.path.join(bpy.utils.system_resource("DATAFILES"), "assets", "brushes", "essentials_brushes-mesh_weight.blend")
def is_mode_match(brush): return brush.use_paint_weight


attributes = [
    "blend",
    "weight",
    "use_pressure_size",
    "strength",
    "use_pressure_strength",

    "weight_tool",
    "use_frontface",
    "use_accumulate",
    "use_frontface",
    "stroke_method",
    "spacing",
    "use_pressure_spacing",
    "dash_ratio",
    "dash_samples",
    "jitter",
    "use_pressure_jitter",
    "jitter_unit",
    "input_samples",
    "use_smooth_stroke",
    "smooth_stroke_radius",
    "smooth_stroke_factor",

    "curve_preset",
    "falloff_shape",
    "use_frontface_falloff",
    "falloff_angle",
    "cursor_color_add",
    "cursor_overlay_alpha",
    "use_cursor_overlay_override",
    "use_cursor_overlay",
]
