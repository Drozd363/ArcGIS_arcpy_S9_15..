import numpy as np

def modelMatrix(inMatrix, sequence):
    """
    Finds a transformation vector in 2D.

    inMatrix: dictionary of transformation matrix
    inMatrix = {'R':(angle),'T':( T_x, T_y),'S':( S_x, S_y),'V':(x,y)}
    sequence: string of operation, like 'SRT' were T - first, S - last operation
    returns: tuple of transformed vector
    """
    v = np.append(np.array(inMatrix['V']), 1)
    v = np.matrix([v]).transpose()
    rt = inMatrix['R']
    st = inMatrix['S']
    tt = inMatrix['T']
    r = np.matrix([[np.cos(np.radians(rt)), -np.sin(np.radians(rt)), 0], [np.sin(np.radians(rt)), np.cos(np.radians(rt)), 0],
         [0, 0, 1]])
    s = np.matrix([[st[0], 0, 0], [0, st[1], 0], [0, 0, 1]])
    t = np.matrix([[1, 0, tt[0]], [0, 1, tt[1]], [0, 0, 1]])
    dictmatrix = {'R': r, 'T': t, 'S': s}
    vect = 1
    for i in sequence:
        matr = dictmatrix[i]
        vect = vect*matr
    outvector = np.ravel(vect*v)
    outtuple = (outvector[0], outvector[1], outvector[2])
    return outtuple




# uncomment test when you ready

if __name__ == '__main__':

    inMatrix1 = {'R':(33),'T':(1.0,2.0),'S':(2.0,1.2),'V':(1,2)}
    inMatrix2 = {'R':(16),'T':(1.0,2.0),'S':(1.0,2.0),'V':(1,2)}
    print ""

    firstTest = modelMatrix(inMatrix1,'SRT')
    assert -1.05 <= firstTest[0] and -0.95 >= firstTest[0] and 5.25 <= firstTest[1] and 5.4 >= firstTest[1]
    print "1. 'R':(33),'T':(1.0,2.0),'S':(2.0,1.2),'V':(1,2)" + " Result is: " + str(firstTest)

    print ""

    secondTest = modelMatrix(inMatrix2,'TRS')
    assert 0.8 <= secondTest[0] and 0.91 >= secondTest[0] and 6.06 <= secondTest[1] and 6.18 >= secondTest[1]
    print "2. 'R':(33),'T':(1.0,2.0),'S':(2.0,1.2),'V':(1,2)" + " Result is: " + str(secondTest)
