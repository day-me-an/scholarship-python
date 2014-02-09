import unittest
import rhul

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.pg = rhul.PositionGenerator()

    #def test_previous_enforced(self):
    #    self.assertRaises(ValueError, self.pg.generate, 10)

    def test_one_coin(self):
        positions = self.pg.generate(1)
        self.assertEqual(positions, [[1]])

    def test_coins2_whole_pile(self):
        positions = self.pg.generate(2)
        self.assertTrue([2] in positions)

    def test_coins2_split(self):
        positions = self.pg.generate(2)
        self.assertTrue([1,1] in positions)        

if __name__ == '__main__':
    unittest.main() 
