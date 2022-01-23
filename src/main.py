#!/usr/bin/env python3

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from math import pi, cos, sin

from cv2 import imshow, cvtColor, COLOR_RGB2BGR, waitKey
from numpy import linspace, array, zeros, float32


def slices(level, size):
    point = array([level / 255] * 3)  # Точка на диагонали уровней серого
    perpendicular = array([1.0] * 3)  # Нормаль к плоскости сечения

    indexes = array([
        (i, j, -(perpendicular[0] * (i - point[0]) +
                 perpendicular[1] * (j - point[1])) / perpendicular[2] + point[2])
        for i in linspace(0, 1, size) for j in linspace(0, 1, size)
    ])

    cube_mat = array([
        (idx[0], idx[1], idx[2], 1) if 0 <= idx[2] <= 1 else \
            (level / 255, level / 255, level / 255, 1) for idx in indexes
    ])

    a = pi / 4
    b = -pi / 5

    # Матрица поворота
    rotation_mat = array([
        [cos(b), 0, -sin(b), 0],
        [0, 1, 0, 0],
        [sin(b), 0, cos(b), 0],
        [0, 0, 0, 1],
    ]) @ array([
        [cos(a), sin(a), 0, 0],
        [-sin(a), cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    rotated_mat = (rotation_mat.dot(cube_mat.T)).T  # Поворот сечения

    image = zeros((size, size, 3))

    # Заполнение цветов
    for i in range(size ** 2):
        image[int(size / 2 + rotated_mat[i][2] * size / 2),
              int(size / 2 + rotated_mat[i][1] * size / 2), 0] = cube_mat[i][0]
        image[int(size / 2 + rotated_mat[i][2] * size / 2),
              int(size / 2 + rotated_mat[i][1] * size / 2), 1] = cube_mat[i][1]
        image[int(size / 2 + rotated_mat[i][2] * size / 2),
              int(size / 2 + rotated_mat[i][1] * size / 2), 2] = cube_mat[i][2]

    # Отрисовка изображения
    image = cvtColor(image.astype(float32), COLOR_RGB2BGR)
    imshow('RGB cube slice', image)
    waitKey()


desc_str = r"""Color cube slicing."""


def parse_args():
    parser = ArgumentParser(prog='color-cube-slicer',
                            formatter_class=RawDescriptionHelpFormatter,
                            description=desc_str)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v0.1')
    parser.add_argument('-l', '--level', type=int, default=128,
                        help=r'level of section (default: %(default)s)')
    parser.add_argument('-s', '--size', type=int, default=256,
                        help=r'size of cube in pixels (default: %(default)s)')
    return parser.parse_args()


def main():
    args = parse_args()
    slices(args.level, args.size)


if __name__ == "__main__":
    main()
