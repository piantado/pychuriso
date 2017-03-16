import unittest
from reduction import reduce_combinator

class ReductionTest(unittest.TestCase):
    def runTest(self):
        #dictionary tests contains combinator strings (key) and expected reduction (value)
        tests = {'.....SKKKxy':'x','..Kxy':'x','....E.....SKKKxy..Kxyab':'a','....E.....KxySxyzab':'b','....E.......KxySxyzKxySxyz':'Sxyz','..Txy':'.yx','.Mx':'.xx','...Bxyz':'.x.yz','...Sxyz':'..xz.yz','..Wxy':'.xyy','.Ix':'x'}
        print "# Testing reduction"
        for k,v in tests.iteritems():
            #assert that reduce_combinator returns the expected value
            self.assertEqual(reduce_combinator(k),v)

if __name__ == '__main__':
    unittest.main()
