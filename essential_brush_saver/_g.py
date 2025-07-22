import bpy
import builtins
log = 1


def print(*args):
    if log:
        builtins.print(*args)
