import unittest
import tiledimage

class TiledImageTest(unittest.TestCase):
	def test_computePadding(self):
		self.assertTrue(tiledimage.computePadding(10,2)==0)
		self.assertTrue(tiledimage.computePadding(11,5)==4)
	def test_computecomputeNumberOfTiles(self):
		self.assertTrue(tiledimage.computeNumberOfTiles(10,2) == 5)
		self.assertTrue(tiledimage.computeNumberOfTiles(11,2) == 6)
		self.assertTrue(tiledimage.computeNumberOfTiles(9,2) == 5)
		with self.assertRaises(ValueError):
			tiledimage.computeNumberOfTiles(2,11)

if __name__ == '__main__':
	unittest.main()