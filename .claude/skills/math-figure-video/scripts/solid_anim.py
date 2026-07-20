"""Parametric solid animation for math-figure videos (Manim).

Renders an n-gonal pyramid net that folds up into a solid and rotates,
on a transparent background so it can be composited over footage.

Generalized from the working square-pyramid prototype. Extend here for
prisms / cross-sections / labels (see TODOs at the bottom).

Usage (inside the manim venv):
    /tmp/manim-venv/bin/manim -qm -t --format=mov --fps 30 -r 1000,1000 \
        solid_anim.py SolidAnim
Parameters are read from environment variables so the CLI stays simple:
    SIDES=4       number of base sides (3=triangular, 4=square, 5,6,...)
    HEIGHT=1.25   apex height as a multiple of the base apothem
    ACTIONS=fold,rotate   comma list: fold, rotate (order fixed: fold then rotate)
"""
import os
import numpy as np
from manim import *

SIDES = int(os.environ.get("SIDES", "4"))
HEIGHT_K = float(os.environ.get("HEIGHT", "1.25"))
ACTIONS = os.environ.get("ACTIONS", "fold,rotate").split(",")

GOLD = ["#F5D68C", "#ECCB80", "#FADE96", "#E6C478", "#F0CE86", "#E2BE74"]


def rodrigues(u, theta):
    u = u / np.linalg.norm(u)
    K = np.array([[0, -u[2], u[1]], [u[2], 0, -u[0]], [-u[1], u[0], 0]])
    return np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)


class SolidAnim(ThreeDScene):
    def construct(self):
        n = SIDES
        R = 2.0                                   # circumradius of base polygon
        ang0 = np.pi / 2 - np.pi / n              # orient a flat edge toward viewer
        V = [np.array([R * np.cos(ang0 + 2 * np.pi * i / n),
                       R * np.sin(ang0 + 2 * np.pi * i / n), 0]) for i in range(n)]
        apothem = R * np.cos(np.pi / n)
        h = HEIGHT_K * apothem
        apex_top = np.array([0, 0, h])

        self.set_camera_orientation(phi=58 * DEGREES, theta=-90 * DEGREES, zoom=1.0)

        base = Polygon(*V, color="#E9C980", fill_color="#785C28",
                       fill_opacity=0.30, stroke_width=3)
        self.add(base)

        fold = ValueTracker(0.0)
        faces = []
        for k in range(n):
            A, B = V[k], V[(k + 1) % n]
            mid = (A + B) / 2.0
            outward = mid / np.linalg.norm(mid)
            L = np.linalg.norm(apex_top - mid)          # slant height
            flat_apex = mid + outward * L
            u = (B - A) / np.linalg.norm(B - A)
            v0, v1 = flat_apex - A, apex_top - A
            v0p = v0 - np.dot(v0, u) * u
            v1p = v1 - np.dot(v1, u) * u
            ang = np.arccos(np.clip(np.dot(v0p, v1p) /
                                    (np.linalg.norm(v0p) * np.linalg.norm(v1p)), -1, 1))
            if np.dot(np.cross(v0p, v1p), u) < 0:
                ang = -ang

            face = Polygon(A, B, flat_apex, color="#E9C980",
                           fill_color=GOLD[k % len(GOLD)], fill_opacity=0.9, stroke_width=3)

            def upd(m, A=A, B=B, u=u, v0=v0, ang=ang):
                apex = A + rodrigues(u, fold.get_value() * ang) @ v0
                m.set_points_as_corners([A, B, apex, A])
            face.add_updater(upd)
            faces.append(face)
            self.add(face)

        self.wait(0.6)
        if "fold" in ACTIONS:
            self.play(fold.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
        else:
            fold.set_value(1.0)
        self.wait(0.3)
        for f in faces:
            f.clear_updaters()
        if "rotate" in ACTIONS:
            self.begin_ambient_camera_rotation(rate=2 * PI / 6.0)
            self.wait(6.0)
            self.stop_ambient_camera_rotation()
        self.wait(0.4)

# TODO (complete later):
#  - prisms: extrude the base polygon by height instead of coning to an apex
#  - cross-section: intersect the solid with a plane and highlight the section
#  - labels: VertexLabels / edge dimensions via MathTex on vertices/edges
