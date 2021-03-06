import numpy as np
import logging
import time

logger = logging.getLogger('peachy')

from infrastructure.gl_point_converter import GLConverter

class Writer(object):
    def write_points(self, array):
        pass


class PLYWriter(Writer):

    def __init__(self, point_converter, point_thinner):
        self._point_thinning = point_thinner
        self.point_converter = point_converter

    def write_polar_points(self, outfile, polar_array):
        start = time.time()
        points = self.point_converter.convert(polar_array)
        verticies = points.shape[0]
        header = "ply\nformat ascii 1.0\ncomment made by Peachy Scanner\ncomment Date Should Go Here\nelement vertex {}\nproperty float x\nproperty float y\nproperty float z\nend_header\n".format(str(verticies))

        outfile.write(header)

        for (x, y, z, a, b, c, u, v) in points:
            outfile.write('{} {} {}\n'.format(x, y, z))

        total = time.time() - start

        logger.info('File Written in {:.2f} milliseconds'.format(total * 1000.0))

    def write_cartisien_points(self, outfile, points_xyz):
        start = time.time()
        thinned_points = self._point_thinning.thin(points_xyz)
        points = self.point_converter.convert_xyz(thinned_points)
        verticies = points.shape[0]

        header = "ply\nformat ascii 1.0\ncomment made by Peachy Scanner\ncomment Date Should Go Here\nelement vertex {}\nproperty float x\nproperty float y\nproperty float z\nend_header\n".format(str(verticies))

        outfile.write(header)

        for (x, y, z, a, b, c, u, v) in points:
            outfile.write('{} {} {}\n'.format(x, y, z))

        total = time.time() - start

        logger.info('File Written in {:.2f} milliseconds'.format(total * 1000.0))
