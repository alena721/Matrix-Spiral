import asyncio
import unittest

from matrix import MatrixError, get_matrix, parse_matrix, spiral_traversal

SOURCE_URL = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
TRAVERSAL = [10, 50, 90, 130, 140, 150, 160, 120, 80, 40, 30, 20, 60, 100, 110, 70]
TABLE = ("| 10 | 20 | 30 | 40 |\n| 50 | 60 | 70 | 80 |\n"
         "| 90 | 100 | 110 | 120 |\n| 130 | 140 | 150 | 160 |")


class TestSpiral(unittest.TestCase):
    def test_traversal_from_task(self):
        self.assertEqual(spiral_traversal(parse_matrix(TABLE)), TRAVERSAL)

    def test_other_sizes(self):
        self.assertEqual(spiral_traversal([[7]]), [7])
        self.assertEqual(spiral_traversal([[1, 2], [3, 4]]), [1, 3, 4, 2])
        self.assertEqual(spiral_traversal([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                         [1, 4, 7, 8, 9, 6, 3, 2, 5])

    def test_empty_matrix(self):
        self.assertEqual(spiral_traversal([[]]), [])


class TestParse(unittest.TestCase):
    def test_not_square(self):
        with self.assertRaises(MatrixError):
            parse_matrix("| 1 | 2 | 3 |")

    def test_empty(self):
        with self.assertRaises(MatrixError):
            parse_matrix("")


class TestGetMatrix(unittest.TestCase):
    def test_empty_url(self):
        with self.assertRaises(MatrixError):
            asyncio.run(get_matrix(""))

    def test_connection_refused(self):
        with self.assertRaises(MatrixError):
            asyncio.run(get_matrix("http://127.0.0.1:1/matrix.txt"))

    def test_from_source(self):
        self.assertEqual(asyncio.run(get_matrix(SOURCE_URL)), TRAVERSAL)


