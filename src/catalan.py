def catalan(n):
    # Base Case
    if n <=1 :
        return 1

    # Catalan(n) is the sum of catalan(i)*catalan(n-i-1)
    res = 0
    for i in range(n):
        res += catalan(i) * catalan(n-i-1)

    return res

if __name__ == "__main__":

	f = open('catalan.txt', 'w+')
	print "Computing the Catalan numbers..."
	# Driver Program to test above function
	for i in range(20):
	    print>> f, str(catalan(i)) +",",
	print "complete!"
