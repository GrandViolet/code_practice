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

    max = 11 # maximum recursion depth to try and search for

    nums = []
    search = 0

    print()

    i = 0
    while search <= max:
        check = True

        if search > 3:
            lstI = list(str(i))

            for j in range(len(lstI)):
                if (lstI[j] == "0") or (lstI[j] == "1"):
                    check = False
                    lstI[j] = "2"

            i = int("".join(lstI))

            for j in range(len(lstI) - 1):
                if int(lstI[j + 1]) < int(lstI[j]):
                    check = False
                    lstI[j + 1] = lstI[j]

            i = int("".join(lstI))
            
        if check == True:
            steps = mult_digits(i)

            if steps == search:
                nums.append(i)
                search += 1
            
            i += 1
            
            sys.stdout.write("\r{0}".format("Searching...   (\x1b[7;32m %d \x1b[0m)   #%d found: %d   %.2fs" % (i - 1, search - 1, nums[-1], time.time() - start)))
        
        else:
            sys.stdout.write("\r{0}".format("Searching...   (\x1b[31m %d \x1b[0m)   #%d found: %d   %.2fs" % (i - 1, search - 1, nums[-1], time.time() - start)))

    print("\nIn the range from 0 to %d:" % (i - 1))

    for k in range(len(nums)):
        print("%d took %d steps" % (nums[k], search + k - len(nums)))

    print("Operation length: %.3f seconds\n" % (time.time() - start))

def mult_digits(num):
    if len(str(num)) == 1:
        return 0

    product = 1
    for i in str(num):
        product *= int(i)
    
    steps = mult_digits(product) + 1

    return steps

main()    