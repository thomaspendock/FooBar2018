from fractions import Fraction

def floor_sum(n, ratio):
    '''
    Returns sum( [ floor(i * ratio) for i in range(n) ] ).
    IE returns floor(ratio * 1) + floor(ratio * 2) + ... + floor(ratio * n).
    '''
    if n <= 0: return 0
    arth_sum = lambda x: int(x * (x + 1) / 2)
    
    frac = ratio - int(ratio)
    fsum = arth_sum(n) * int(ratio)

    height = int(n*frac)
    fsum += n*height

    new_ratio = 1/frac
    new_frac = new_ratio - int(new_ratio)
    
    fsum -= arth_sum(height) * int(new_ratio)
    fsum -= floor_sum(height, new_frac)
    return fsum
    

def solution(n):
    rt = "141421356237309504880168872420969807856967187537694807317667973"+\
          "79907324784621070388503875343276415727350138462309122970249248"+\
          "36055850737212644121497099935831413222665927505592755799950501"+\
          "15278206057147010955997160597027453459686201472851741864088919"+\
          "86095523292304843087143214508397626036279952514079896872533965"+\
          "46331808829640620615258352395054745750287759961729835575220337"+\
          "53185701135437460340849884716038689997069900481503054402779031"+\
          "64542478230684929369186215805784631115966687130130156185689872"+\
          "37235288509264861249497715421833420428568606014682472077143585"+\
          "48741556570696776537202264854470158588016207584749226572260020"+\
          "8558446652145839"

    ratio = Fraction(int(rt), 10**(len(rt)-1))
    return str(floor_sum(int(n), ratio))

print(solution(77))


'''
Dodge the Lasers!
=================

Oh no! You've managed to escape Commander Lambdas collapsing space station in an
escape pod with the rescued bunny prisoners - but Commander Lambda isnt about to
let you get away that easily. She's sent her elite fighter pilot squadron after
you - and they've opened fire!

Fortunately, you know something important about the ships trying to shoot you
down. Back when you were still Commander Lambdas assistant, she asked you to
help program the aiming mechanisms for the starfighters. They undergo rigorous
testing procedures, but you were still able to slip in a subtle bug. The
software works as a time step simulation: if it is tracking a target that is
accelerating away at 45 degrees, the software will consider the targets
acceleration to be equal to the square root of 2, adding the calculated result
to the targets end velocity at each timestep. However, thanks to your bug,
instead of storing the result with proper precision, it will be truncated to an
integer before adding the new velocity to your current position.  This means
that instead of having your correct position, the targeting software will
erringly report your position as sum(i=1..n, floor(i*sqrt(2))) - not far enough
off to fail Commander Lambdas testing, but enough that it might just save your
life.

If you can quickly calculate the target of the starfighters' laser beams to know
how far off they'll be, you can trick them into shooting an asteroid, releasing
dust, and concealing the rest of your escape.  Write a function solution(str_n)
which, given the string representation of an integer n, returns the sum of
(floor(1*sqrt(2)) + floor(2*sqrt(2)) + ... + floor(n*sqrt(2))) as a string. That
is, for every number i in the range 1 to n, it adds up all of the integer
portions of i*sqrt(2).

For example, if str_n was "5", the solution would be calculated as
floor(1*sqrt(2)) +
floor(2*sqrt(2)) +
floor(3*sqrt(2)) +
floor(4*sqrt(2)) +
floor(5*sqrt(2))
= 1+2+4+5+7 = 19
so the function would return "19".

str_n will be a positive integer between 1 and 10^100, inclusive. Since n can be
very large (up to 101 digits!), using just sqrt(2) and a loop won't work.
Sometimes, it's easier to take a step back and concentrate not on what you have
in front of you, but on what you don't.

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases -- 
Input:
Solution.solution('77')
Output:
    4208

Input:
Solution.solution('5')
Output:
    19

-- Python cases -- 
Input:
solution.solution('77')
Output:
    4208

Input:
solution.solution('5')
Output:
    19
'''
