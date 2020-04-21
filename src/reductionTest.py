import unittest
from reduction import reduce_combinator

class ReductionTest(unittest.TestCase):


    def runTest(self):
        #dictionary tests contains combinator strings (key) and expected reduction (value)
        tests = {'.....SKKKxy':'x','..Kxy':'x','....E...SKK..Kxy..Kxyab':'a','....E..Kxy...Sxyzab':'b','....E..Kxy...Sxyz..Kxy...Sxyz':'..xz.yz','..Txy':'.yx','.Mx':'.xx','...Bxyz':'.x.yz','...Sxyz':'..xz.yz','..Wxy':'..xyy','.Ix':'x'}
        print "# Testing reduction"
        for k,v in tests.iteritems():
            print "Testing reduce_combinator( " + str(k) + " )  == " + str(v)

            #assert that number of applies is correct
            self.assertEqual(v.count('.'),len(v)-v.count('.')-1)
            # assert that reduce_combinator returns the expected value
            self.assertEqual(reduce_combinator(k),v)

if __name__ == '__main__':

    unittest.main()
