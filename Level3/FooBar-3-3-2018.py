def answer(n):
    calls = {} # store previous function calls in memory
    
    def steps(bricks_left, lo, hi, total=0):
        ''' # of steps given: bricks left, min step size, max steps size'''
        if bricks_left == 0 or lo == hi:
            return 1 # 1 choice for step size
        if lo > hi:
            return 0 # this isn't possible: no combos
        for step_size in range(lo, hi+1):
            # new min has to be 1 greater than step, new max = leftover bricks
            step_range = step_size + 1, bricks_left - step_size
            
            # use memory to quickly return or calculate and update the memory
            num_steps = calls[step_range] if step_range in calls \
                        else steps(step_range[1], *step_range)
            calls[step_range] = num_steps
            
            total += num_steps
        return total
    
    # the first step is between 1 and half the available bricks
    # (if more than half is used then the second step will be less than first)
    return steps(n, 1, (n - 1)//2)

### Test cases ###
assert(answer(3)==1)
assert(answer(200)==487067745)
print("All test cases passed.")


'''
The Grandest Staircase Of Them All
==================================

With her LAMBCHOP doomsday device finished, Commander Lambda is preparing for
her debut on the galactic stage - but in order to make a grand entrance, she
needs a grand staircase! As her personal assistant, you've been tasked with
figuring out how to build the best staircase EVER.

Lambda has given you an overview of the types of bricks available, plus a
budget. You can buy different amounts of the different types of bricks (for
example, 3 little pink bricks, or 5 blue lace bricks). Commander Lambda wants to
know how many different types of staircases can be built with each amount of
bricks, so she can pick the one with the most options.

Each type of staircase should consist of 2 or more steps.  No two steps are
allowed to be at the same height - each step must be lower than the previous
one. All steps must contain at least one brick. A step's height is classified as
the total amount of bricks that make up that step.
For example, when N = 3, you have only 1 choice of how to build the staircase,
with the first step having a height of 2 and the second step having a height of
1: (# indicates a brick)

#
##
21

When N = 4, you still only have 1 staircase choice:

#
#
##
31

But when N = 5, there are two ways you can build a staircase from the given
bricks. The two staircases can have heights (4, 1) or (3, 2), as shown below:

#
#
#
##
41

#
##
##
32

Write a function called answer(n) that takes a positive integer n and returns
the number of different staircases that can be built from exactly n bricks.
n will always be at least 3 (so you can have a staircase at all), but no more
than 200, because Commander Lambda's not made of money!
'''
