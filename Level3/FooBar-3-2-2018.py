from fractions import Fraction

def copy(matrix):
    '''Returns an identical copy of a matrix'''
    i = 0
    return [[matrix[j][i] for i in range(len(matrix))]
                          for j in range(len(matrix[i])) ]

def multiply(m1, m2):
    '''Returns matrix mulptilation of m1*m2'''
    return [[sum(a*b for a,b in zip(m1Row,m2Col))
             for m2Col in zip(*m2)] for m1Row in m1]

def newMatrix(numRows, numCols):
    '''Returns a size*size 0 matrix (a blank matrix)'''
    return [[0]*numCols for i in range(numRows)]

def identityMinus(m):
    '''Returns I - m'''
    size = len(m)
    result = newMatrix(size, size)
    for r in range(size):
        for c in range(size):
            result[r][c] = Fraction(-m[r][c].numerator, m[r][c].denominator)
            if c == r: result[r][c] += 1
    return result

def inverse(m):
    '''Calculates the inverse of matrix m'''
    n = len(m)
    table = newMatrix(n, n*2)

    # Set up [A|I]
    for r in range(n):
        for c in range(n):
            table[r][c] = m[r][c]
        table[r][r+n] = 1 # add entry of I
        
    # pivoting
    for r in range(n):

        # divide current row by pivot value
        scalar = table[r][r]
        for c in range(2*n):
            table[r][c] /= scalar

        # substract the current row to all above and below rows
        for c in range(n):
            if c == r: continue
            
            scalar = table[c][r]
            for k in range(2*n):
                table[c][k] -= scalar * table[r][k]

    # extact the right half (left half is identity)
    inv = [table[r][n:] for r in range(n)]
    return inv


def putOnes(m):
    '''Add a 1 to each terminal row to represent an absorbing state'''
    new = []
    for r in range(len(m)):
        row = [x for x in m[r]]
        if sum(row) == 0: #indicator of terminal row
            row[r] = 1
        new.append(row)
    return new

def swap(m, upper, lower):
    '''Swaps two rows of an adjancency matrix'''
    size = len(m)
    new = newMatrix(size, size)
    orig = [x for x in range(size)]
    order = swapOrder(orig, upper, lower)
    # re locate each entry according to new entry
    for r in range(size):
        for c in range(size):
            new[r][c] = m[order.index(r)][order.index(c)]
    return new

def swapOrder(order, upper, lower):
    '''Swaps two values in list
       order: the current ordering of states along column and row
       upper: upper row to be swapped
       lower: lower row to be swapped'''
    new = [x for x in order]
    tempUpper = new[upper]
    tempLower = new[lower]
    new[upper] = tempLower
    new[lower] = tempUpper
    return new
    
def shift(m):
    '''Shifts the rows down by one of an adjancency matrix'''
    size = len(m)
    new = newMatrix(size, size)
    for r in range(size):
        row = [0 for i in range(size)]
        for c in range(size):
            # wrap entry to front of the row
            if c == size-1:
                row[0] = m[r][c]
            # move entry to the left
            else:
                row[c+1] = m[r][c]
        # wrap row to index 0 if it is at the bottom
        if r == size-1:
            new[0] = row
        # move row down
        else:
            new[r+1] = row
    return new

def shiftOrder(order):
    '''shift a given order of numbers (in a list) down by 1'''
    new = [x for x in range(len(order))] #blank
    for i in range(len(order)):
        if i == len(order) -1:
            new[0] = order[i]
        else:
            new[i+1] = order[i]
    return new

def standardize(m):
    '''return the standard form matrix of m:
       |I|0|
       |R|Q| is the standard form'''
    n = len(m)
    standard = copy(m)
    ordering = [x for x in range(len(m))]

    #swap terminals until all terminals are at the bottom
    numSwaps = 0
    for r in range(n-1, -1, -1): # start at bottom row
        if sum(m[r]) == 0:
            standard = swap(standard, r, n-1-numSwaps)
            ordering = swapOrder(ordering, r, n-1-numSwaps)
            numSwaps += 1
            
    # shift terminals to top
    for r in range(n-1, -1, -1):
        if sum(m[r]) == 0:
            ordering = shiftOrder(ordering)
            standard = shift(standard)

    standard = putOnes(standard)

    # make every number a fraction
    for r in range(n):
        total = sum(standard[r])
        for c in range(n):
            standard[r][c] = Fraction(standard[r][c], total)

    return [standard, ordering]
    
def getFundemental(Q):
    '''Calculates the fundemental matrix of the standard form matrix'''
    #F = (I - Q)**-1
    return inverse(identityMinus(Q))
       
def getR(m):
    '''Returns R from the standard form matrix'''
    n = len(m)
    for r in range(n):
        if m[r][r] != 1:
            #return bottom left matrix
            return [ x[0:r] for x in m[r:] ]
    
def getQ(m):
    '''Returns Q from the standard form matrix'''
    n = len(m)
    for r in range(n):
        if m[r][r] != 1:
            #retrun bottom right matrix
            return [ x[r:] for x in m[r:] ]
      
def getLimitingMatrix(m, numTerminals):
    '''Find the limiting matrix of m'''
    standardMatrix, ordering = standardize(m)
    R = getR(standardMatrix)
    Q = getQ(standardMatrix)
    F = getFundemental(Q)
    FR = multiply(F, R)

    # construct limiting matrix by combining:
    # | I  0 | 
    # | FR 0 |
    size = len(m)
    limiting = newMatrix(size, size)
    for i in range(numTerminals):
        limiting[i][i] = 1
    for i in range(numTerminals, size):
        row = FR[i-numTerminals]
        for x in range(len(row)):
            limiting[i][x] = row[x]
    
    return limiting, ordering

def getProbs(limiting, ordering, numTerminals):
    '''Extracts the probabilites from the limiting matrix (starting at state 0)'''
    state0index = ordering.index(0)
    # traverse entries of the state0 row and collect probabilities
    probs = [limiting[state0index][i] for i in range(numTerminals)]
    normProbs = normalizeProbs(probs)
    return normProbs

def gcd(a, b):
    if b == 0: return a
    else: return gcd(b, a % b)

def lcm(x, y):
   m = (x*y)//gcd(x,y)
   return m

def lcmList(l):
    '''least common divisor for a list of numbers'''
    if(len(l) == 1): return l[0]
    m = lcm(l[0], l[1])
    #accumlative lcm
    for i in range(2, len(l)):
        m = lcm(m, l[i])
    return m

def normalizeProbs(probs):
    '''Find greatest common denominator and return the probs in desired format'''
    LCM = lcmList([fraction.denominator for fraction in probs])
    normalized = [fraction.numerator * LCM // fraction.denominator for fraction in probs]
    normalized.append(LCM)
    
    return normalized

def answer(m):
    '''Find the limiting matrix of m and returns probabilties from state 0 row'''
    if sum(m[0]) == 0: return [1, 1]

    numTerminals = sum([1 for row in m if sum(row) == 0])
    limiting, ordering = getLimitingMatrix(m, numTerminals)
    probs = getProbs(limiting, ordering, numTerminals)
    return probs

###  Test Cases ###

assert (
    answer([
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]) == [7, 6, 8, 21]
)
 
assert (
    answer([
        [0, 1, 0, 0, 0, 1],
        [4, 0, 0, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]) == [0, 3, 2, 9, 14]
)
 

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
    

