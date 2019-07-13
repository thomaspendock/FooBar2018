from math import log

def solution(n, acc=0, log2=lambda x: int(log(x)/log(2))):
    n = int(n)
    # 1 -> 1 (0 steps), 2 -> 1 (1 step), 3 -> 2 -> 1 (2 steps)
    if n < 4: return acc + n - 1 
    # list of largest powers of 2 that divide n, n+1, and n-1
    divs = [n&~(n-1), (n+1)&~n, (n-1)&~(n-2)]
    # retrieve index of largest power of 2: either 0, 1, or -1
    i = divs.index(max(divs))
    if i == 2: i = -1 # -1 is the equivlent index to 2
    # solution(shift n and divide by largest pow of 2, add steps from shifting and halving)
    return solution((n+i)//divs[i], acc=acc + abs(i) + log2(divs[i]))

print(solution('15'))
print(solution('4'))

'''
Fuel Injection Perfection
=========================

Commander Lambda has asked for your help to refine the automatic quantum
antimatter fuel injection system for her LAMBCHOP doomsday device. It's a great
chance for you to get a closer look at the LAMBCHOP - and maybe sneak in a bit
of sabotage while you're at it - so you took the job gladly. 

Quantum antimatter fuel comes in small pellets, which is convenient since the
many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time.
However, minions dump pellets in bulk into the fuel intake. You need to figure
out the most efficient way to sort and shift the pellets down to a single pellet
at a time. 

The fuel control mechanisms have three operations: 

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a
quantum antimatter pellet is cut in half, the safety controls will only allow
this to happen if there is an even number of pellets)

Write a function called answer(n) which takes a positive integer as a string and
returns the minimum number of operations needed to transform the number of
pellets to 1. The fuel intake control panel can only display a number up to 309
digits long, so there won't ever be more pellets than you can express in that
many digits.

For example:
answer(4) returns 2: 4 -> 2 -> 1
answer(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases -- 
Input:
solution.solution('15')
Output:
    5

Input:
solution.solution('4')
Output:
    2

-- Java cases -- 
Input:
Solution.solution('4')
Output:
    2

Input:
Solution.solution('15')
Output:
    5

'''
