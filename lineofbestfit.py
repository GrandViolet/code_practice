

from math import *
def main():
    points = get_points()

    a = len(points)
    b = 0
    for point in points:
        b = b + point[0]
    d = 0
    for point in points:
        d = d + point[0]**2
    e = 0
    for point in points:
        e = e + point[1]
    f = 0
    for point in points:
        f = f + point[0]*point[1]
    
    b0 = (e/a) - (b/a) * ((f - ((b * e) / a)) / (d - ((b * b) / a)))
    b1 = (f - ((b * e) / a)) / (d - ((b * b) / a))
    print("\ny = %f + %fx" % (b0,b1))

    errorAmt = error(points,b0,b1)
    print("error: %f\n" % (errorAmt))

    input()
    
def get_points():
    points = []
    for i in range(int(input("\n# of points: "))):
        x = input("\nx%d: " % (i + 1))
        y = input("y%d: " % (i + 1))
        points.append([float(x),float(y)])
    return points

def error(points,b0,b1):
    error = 0
    for point in points:
        error = error + (b0 + (b1 * point[0]) - point[1])**2
    error = sqrt(error)
    return error

main()
