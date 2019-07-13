from fractions import Fraction

def printMatrix(matrix):
    for row in matrix: print(row)

def multiply(m1, m2):
    # iterate through rows of X
    for i in range(len(m1)):
   # iterate through columns of Y
       for j in range(len(m2[0])):
       # iterate through rows of Y
           for k in range(len(m2)):
               result[i][j] += m1[i][k] * m2[k][j]
            
def power(m, p):
    product = m
    for i in range(p-1):
        product = multiply(product, m)
    return product

def dot(v1, v2):
    return sum([v1[i]*v2[i] for i in range(len(v1))])

def colVector(m, index):
    return [m[r][index] for r in range(len(m))]


def putOnes(m):
    new = []
    for r in range(len(m)):
        row = [x for x in m[r]]
        if isTerminal(m, r):
            row[r] = 1
        new.append(row)
    return new

def setFractions(m):
    new = []
    for r in range(len(m)):
        d = sum(m[r])
        new.append([ e/d for e in m[r] ])
    return new

def isTerminal(m, index):
    v = m[index]
    print(v)
    for i in range(len(v)):
        if v[i] != 0:
            if not (index == i and v[i] == 1):
                return False
    return True

def getProbs(matrix, rowNum, ref):
    probs = []
    for r in range(len(matrix)):
        if isTerminal(ref, r):
            probs.append(matrix[rowNum][r])
    return probs

def hasTerminal(m):
    for i in range(len(m)):
        if isTerminal(m, 1): return True
    return False

def toFractions(probs):
    fracs = []
    for prob in probs:
        mult = 1
        while round(mult * prob) != round(mult * prob, 10):
            mult += 1
        n = mult * prob
        d = mult
        fracs.append([int(round(n)), int(round(d))])
    return fracs

def gcd(a, b):
    if b == 0: return a
    else: return gcd(b, a % b)


def lcm(x, y):
   m = (x*y)//gcd(x,y)
   return m

def lcmList(l):
    if(len(l) == 1): return l[0]
    m = lcm(l[0], l[1])
    for i in range(2, len(l)):
        m = lcm(m, l[i])
    return m
def transpose(matrix):
    i= 0
    return [[matrix[i][j] for i in range(len(matrix))]
                          for j in range(len(matrix[i])) ]
def answer(m):
    
    n = putOnes(m)
    fracMatrix = setFractions(n)

    powMatrix = power(fracMatrix, 2000)
    prob = getProbs(powMatrix, 0, m)
    print(prob)
    probs = toFractions(prob)
    print(probs)
    lcm = lcmList([x[1] for x in probs])
    final = [ int(x[0] * lcm/x[1]) for x in probs ]
    final.append(lcm)
    return final
        
m = [[8, 1, 1],
     [2, 7, 1],
     [3, 1, 6]]

m1 = [[1, 1], [4, 1]]
m2 = [[0, 1, 0, 0, 0, 1],
      [4, 0, 0, 3, 2, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0]]


M  = [[0, 2, 1, 0, 0],
      [0, 0, 0, 3, 4],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0]]

print(answer(m2))

'''
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the
exotic matter involved. It starts as raw ore, then during processing, begins
randomly changing between forms, eventually reaching a stable form. There may be
multiple stable forms that a sample could ultimately reach, not all of which are
useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation
efficiency by predicting the end state of a given ore sample. You have carefully
studied the different structures that the ore can take and which transitions it
undergoes. It appears that, while random, the probability of each structure
transforming is fixed. That is, each time the ore is in 1 state, it has the same
probabilities of entering the next state (which might be the same state).  You
have recorded the observed transitions in a matrix. The others in the lab have
hypothesized more exotic forms that the ore can become, but you haven't seen all
of them.

Write a function answer(m) that takes an array of array of nonnegative ints
representing how many times that state has gone to the next state and return an
array of ints for each terminal state giving the exact probabilities of each
terminal state, represented as the numerator for each state, then the
denominator for all of them at the end and in simplest form. The matrix is at
most 10 by 10. It is guaranteed that no matter which state the ore is in, there
is a path from that state to a terminal state. That is, the processing will
always eventually end in a stable state. The ore starts in state 0.
The denominator will fit within a signed 32-bit integer during the calculation,
as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].
'''
    

