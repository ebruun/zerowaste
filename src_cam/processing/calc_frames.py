# PYTHON IMPORTS
import numpy as np
import cv2 as cv

# COMPAS IMPORTS
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Transformation

# LOCAL IMPORTS
from src_cam.utility.io import _create_file_path


def _xyz_data(pointcloud):
    print("-- --get xyx pointcloud data")
    data = pointcloud.copy_data("xyz")

    return data


def _unit_vec(p1, p2):
    v = p1 - p2
    v = v / np.linalg.norm(v)
    return v


def _calc_unit_vec(points_corners):
    print("-- --calculate unit vectors")
    vec_x_1 = _unit_vec(points_corners[1], points_corners[0])
    # vec_x_2 = _unit_vec(points_corners[3], points_corners[2])
    vec_y_1 = _unit_vec(points_corners[2], points_corners[0])
    # vec_y_2 = _unit_vec(points_corners[3], points_corners[1])

    return vec_x_1, vec_y_1


def _member_frame(point, x, y):
    print("-- --make COMPAS frame")

    F = Frame(
        Point(0, 0, 0) + point.tolist(),
        Vector(0, 0, 0) + x.tolist(),
        Vector(0, 0, 0) + y.tolist(),
    )

    return F


def calc_frames(pointcloud, features):
    print("\nCALCULATE MEMBER FRAMES")
    data = _xyz_data(pointcloud)

    rectangles, midpoints = features

    frames = []
    for i, (rectangle, midpoint) in enumerate(zip(rectangles, midpoints)):
        print("\n--rectangle", i)

        xyz_points_mid = data[midpoint[1], midpoint[0]]
        xyz_points_corners = data[rectangle[:, 1], rectangle[:, 0]]

        vec_x, vec_y = _calc_unit_vec(xyz_points_corners)

        # invert vectors so tcp rotate 180
        F = _member_frame(xyz_points_mid, -vec_x, -vec_y)
        frames.append(F)

    return frames


if __name__ == "__main__":
    pass
