import numpy as np
import itertools as it
import os
import sys
from itertools import combinations, permutations
# pip install python-sat==0.1.6.dev12
from pysat.solvers import Glucose3

def readMat(path):
    f = open(path, 'rt')
    h, w = [int(x) for x in f.readline().strip().split('\t')]
    assert h > 0 and w > 0
    mat = - np.ones((h, w), dtype=int)
    for ih in range(h):
        iw = 0
        for it in f.readline().strip().split('\t'):
            if it != '.':
                mat[ih][iw] = int(it)
            iw += 1
    f.close()
    return mat

def toCNF(mat, lvars):
    clauses = []
    h, w = mat.shape
    for i in range(h):
        for j in range(w):
            if mat[i][j] >= 0:
                clauses += getClauses(mat, lvars, i, j)
    return clauses

def getClauses(mat, lvars ,ih, iw):  #ih row, iw column
    clauses = []
    #raise NotImplementedError 

    k = mat[ih][iw]
    numk = len((getAllAdjacent(mat, lvars, ih, iw)))
    
    # CASE 1: 
    # Ref: https://www.geeksforgeeks.org/permutation-and-combination-in-python/
    for c1 in it.combinations(getAllAdjacent(mat, -lvars, ih, iw), k+1):
        c1 = [int(x) for x in list(c1)]
        clauses.append(c1)    
    
    # CASE 2:
    for c2 in it.combinations(getAllAdjacent(mat,lvars, ih, iw), numk-k+1):
        c2 = [int(x) for x in list(c2)]
        clauses.append(c2)  
        
    return clauses

def getAllAdjacent(mat, lvars, ih, iw):
    res = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            ii = i + ih
            jj = j + iw
            if validCell(ii, jj, mat.shape) and lvars[ii][jj] not in res:
                res.append(lvars[ii][jj])
    return res

def validCell(i, j, shape):
    return 0 <= i and i < shape[0] and 0 <= j and j < shape[1]

def initVars(mat):
    ivar = 1
    lvars = np.zeros(mat.shape, dtype=np.int32)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            lvars[i, j] = ivar
            ivar += 1
    return lvars, ivar - 1

def solveCNFs(clauses):
    g = Glucose3()
    print(type(clauses[0][0]))
    for it in clauses:
        g.add_clause(it)
    ret, result = g.solve(), None
    if ret:
        result = g.get_model()
    
    return ret, result

def fortmatFilledCell(text, cl_code):
    return '\033[1;37;%dm%s\033[1;0;0m'%(cl_code, text)

if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = sys.argv[2]
    mat = readMat(infile)   
    
    lvars, num = initVars(mat)
    clauses = toCNF(mat, lvars)

    print(clauses)
    ret, res = solveCNFs(clauses)
    print(ret, res)

    vis_str = ''
    with open(outfile, 'wt') as g:
        for ih in range(mat.shape[0]):
            for iw in range(mat.shape[1]):
                txt = ''
                if mat[ih][iw] >= 0:
                    g.write('%d'%(mat[ih][iw]))
                    txt += '%-2d'%(mat[ih, iw])
                else:
                    g.write(' ')
                    txt += '  '

                if lvars[ih][iw] in res:
                    g.write('.')
                    vis_str += fortmatFilledCell(txt, 42)
                else:
                    g.write(' ')
                    vis_str += fortmatFilledCell(txt, 41)
            g.write('\n')
            vis_str += '\n'

    print ('\n=======INPUT=======')

    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i][j] < 0:
                print ('_', end='')
            else:
                print (mat[i][j], end='')
        print ('')
    print ('===================')
    print ('\n=======ANSWER=======')
    print (vis_str,'=====================')