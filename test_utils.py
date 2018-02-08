# test_utils.py
# Author: Sébastien Combéfis
# Version: February 8, 2018

import unittest
import utils

class TestUtils(unittest.TestCase):
    def test_fact(self):

        self.assertEqual( utils.fact(1), 1)
        self.assertEqual(utils.fact(4), 24)
        with self.assertRaises(ValueError):
            utils.fact(-1)
    
    def test_roots(self, a, b, c):
        d = ((b**2) - (4 * a * c))
        x1 = (-b + ((d) ^ (1 / 2))) / 2 * a
        x2 = (-b - ((d) ^ (1 / 2))) / 2 * a
        if d > 0:
            self.assertEqual( utils.roots(a,b,c),(x1,x2), "Check")
        if d == 0:
            self.assertEqual(utils.roots(a, b, c), (x1))
        else:
            self.assertEqual(utils.roots(a, b, c),())
        pass
    
    def test_integrate(self, function, lower, upper):
        x = lower
        while x <= upper:
            intg = intg + eval(function)
            x+=1
        self.assertEqual(utils.integrate, intg )
        pass

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    runner = unittest.TextTestRunner()
    exit(not runner.run(suite).wasSuccessful())
