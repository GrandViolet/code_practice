"""
DigitMultiplication.py

Find the smallest numbers with a certain digit multiplication chain length

V. Buckley
07.03.2024
"""

import time
import sys

def main():
    start = time.time()

    max = int(input()) # maximum recursion depth to try and search for

    nums = []
    search = 0

    print()

    i = 0
    while search <= max:
        check = True

        if search > 3:
            lstI = list(str(i)) # turn i into a list of strings

            for j in range(len(lstI)): # make sure i does not contain a 0 or a 1
                if (lstI[j] == "0") or (lstI[j] == "1"):
                    check = False
                    lstI[j] = "2"

            for j in range(len(lstI) - 1): # make sure i has digits in ascending order
                if int(lstI[j + 1]) < int(lstI[j]):
                    check = False
                    lstI[j + 1] = lstI[j]

            i = int("".join(lstI)) # turn i back into an int
            
        if check == True:
            steps = mult_digits(i)

            sys.stdout.write("\r{0}".format("Searching...   ( %d )   %.2fs" % (i, time.time() - start)))

            if steps == search:
                nums.append(i)

                print("\n%d took %d steps\n" % (i, search))
                
                search += 1

            i += 1
            

    print("\nIn the range from 0 to %d:\n" % (i - 1))

    for k in range(len(nums)):
        print("%d took %d steps" % (nums[k], search + k - len(nums)))

    print("\n" + str(nums) + "\n")
    print("Operation length: %f seconds\n" % (time.time() - start))

def mult_digits(num):
    if len(str(num)) == 1:
        return 0

    product = 1
    for i in str(num):
        product *= int(i)
    
    steps = mult_digits(product) + 1

    return steps

main()    