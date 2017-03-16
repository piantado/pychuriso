import unittest
from reduction import reduce_combinator

class ReductionTest(unittest.TestCase):





    def runTest(self):
        #dictionary tests contains combinator strings (key) and expected reduction (value)
        tests = {'.....SKKKxy':'x','..Kxy':'x','....E...SKK..Kxy..Kxyab':'a','....E..Kxy...Sxyzab':'b','....E..Kxy...Sxyz..Kxy...Sxyz':'..xz.yz','..Txy':'.yx','.Mx':'.xx','...Bxyz':'.x.yz','...Sxyz':'..xz.yz','..Wxy':'..xyy','.Ix':'x'}
        print "# Testing reduction"
        for k,v in tests.iteritems():
            #assert that reduce_combinator returns the expected value
            print "Testing: " + str(k) + " == " + str(v)
            self.assertEqual(v.count('.'),len(v)-v.count('.')-1)
            self.assertEqual(reduce_combinator(k),v)

if __name__ == '__main__':

    unittest.main()
