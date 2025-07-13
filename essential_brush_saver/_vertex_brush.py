import os
import bpy
relative_asset_path = os.path.join("brushes", "essentials_brushes-mesh_vertex.blend", "Brush")
abs_asset_path = os.path.join(bpy.utils.system_resource("DATAFILES"), "assets", "brushes", "essentials_brushes-mesh_vertex.blend")
def is_mode_match(brush): return brush.use_paint_vertex


attributes = [
    "blend",
    "size",
    "use_pressure_size",
    "strength",
    "use_pressure_strength",
    "vertex_tool",
    "use_alpha",
    "use_accumulate",
    "use_frontface",
    "color",
    "secondary_color",
    "texture_slot.map_mode",
    "texture_slot.angle",
    "texture_slot.use_rake",
    "texture_slot.use_random",
    "texture_slot.random_angle",
    "texture_slot.offset",
    "texture_slot.scale",
    "stroke_method",
    "rate",
    "jitter",
    "use_pressure_jitter",
    "jitter_unit",
    "input_samples",
    "smooth_stroke_radius",
    "smooth_stroke_factor",
    "use_smooth_stroke",
    "curve_preset",
    "falloff_shape",
    "falloff_angle",
    "use_frontface_falloff",
    "cursor_overlay_alpha",
    "texture_overlay_alpha",
    "cursor_color_add",
    "use_cursor_overlay_override",
    "use_cursor_overlay",
    "use_primary_overlay_override",
    "use_primary_overlay",
]
