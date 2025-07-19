import os
import bpy
relative_asset_path = os.path.join("brushes", "essentials_brushes-mesh_texture.blend", "Brush")
abs_asset_path = os.path.join(bpy.utils.system_resource("DATAFILES"), "assets", "brushes", "essentials_brushes-mesh_texture.blend")
def is_mode_match(brush): return brush.use_paint_image


attributes = [
    "blend",
    "size",
    "use_pressure_size",
    "strength",
    "use_pressure_strength",
    "color_type",
    "color_ramp.color_mode",
    "color_ramp.interpolation",
    "gradient_stroke_mode",

    "image_tool",
    "use_alpha",
    "use_accumulate",
    "texture_slot.map_mode",
    "texture_slot.angle",
    "texture_slot.use_rake",
    "texture_slot.use_random",
    "texture_slot.random_angle",
    "texture_slot.offset",
    "texture_slot.scale",
    "spacing",
    "stroke_method",
    "use_pressure_spacing",
    "use_space_attenuation",
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
    "cursor_color_add",
    "cursor_overlay_alpha",
    "use_cursor_overlay_override",
    "use_cursor_overlay",
    "texture_overlay_alpha",
    "use_primary_overlay_override",
    "use_primary_overlay",
    "mask_overlay_alpha",
    "use_secondary_overlay_override",
    "use_secondary_overlay",
]
