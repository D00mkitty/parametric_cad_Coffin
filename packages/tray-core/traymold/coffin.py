"""Clamp layout shared by the coffin solids, validation and print plan."""
from math import hypot

from .derive import forming_gap


def clamp_centres(params):
    spec = params.tray.profile
    vertices = spec.vertices()
    holes = params.features.clamp_holes
    distance = (spec.rim_offset + forming_gap(params)
                + params.mold.female_entry_blend_bottom.size + holes.inset)
    points = []
    for index in (1, 2, 4, 5):
        x, y = vertices[index]
        u, v = vertices[(index + 1) % 6]
        length = hypot(u-x, v-y)
        points.append(((x+u)/2 + distance*(v-y)/length,
                       (y+v)/2 - distance*(u-x)/length))
    if holes.pattern == "four_corners":
        return points
    return [points[0], points[2]] if holes.diagonal == "nw_se" else [points[1], points[3]]
