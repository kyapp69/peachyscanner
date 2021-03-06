import unittest
import sys
import os
import numpy as np
from StringIO import StringIO
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from infrastructure.writer import PLYWriter
from infrastructure.gl_point_converter import GLConverter


class StubPointThinner(object):
    def __init__(self, return_object = None):
        self.return_object = return_object
        self.calls = []

    def thin(self, points):
        self.calls.append(points)
        if self.return_object is not None:
            return self.return_object
        else:
            return points

class PointConverterTest(unittest.TestCase):
    def setUp(self):
        self.stub_point_thinner = StubPointThinner()
        self.writer = PLYWriter(GLConverter(), self.stub_point_thinner)

    def test_header_is_correct(self):
        data = np.array([[10, 10], [10, 10]])
        expected_header = """ply
format ascii 1.0
comment made by Peachy Scanner
comment Date Should Go Here
element vertex 4
property float x
property float y
property float z
end_header\n"""
        result = StringIO()
        self.writer.write_polar_points(result, data)

        self.assertTrue(result.getvalue().startswith(expected_header))

    def test_simple_data_set_is_correct(self):
        data = np.array([[10.0, 10.0, 10.0], [20.0, 20.0, 20.0]])
        a_file = StringIO()
        expected_data = [[10, 0, 0], [10, 0, 1], [10, 0, 2], [-20, 0, 0], [-20, 0, 1], [-20, 0, 2]]
        self.writer.write_polar_points(a_file, data)
        result = self.stringIO2float(a_file)
        self.assertEquals(result, expected_data)

    def test_write_cartisien_points_should_thin_data(self):
        data = np.array([[10.0, 10.0, 10.0], [20.0, 20.0, 20.0]])
        expected = np.array([[10.0, 10.0, 10.0]])
        expected_data = [[10.0, 10.0, 10.0]]
        self.stub_point_thinner.return_object = expected

        a_file = StringIO()
        self.writer.write_cartisien_points(a_file, data)
        result = self.stringIO2float(a_file)
        self.assertEquals(result, expected_data)

    def stringIO2float(self, text):
        string = text.getvalue()
        lines = string.split('\n')[9:-1]
        return [[int(float(number)) for number in line.split(' ')] for line in lines]  

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level='INFO')
    unittest.main()
