import math

def calc_threshold(k, l_prime, l, epsilon):
    ln = math.ceil(k*l_prime / float(l))
    epsilon_abs = math.ceil(epsilon * l)
    return k - ln * epsilon_abs

def float_range(start, stop, step):
    r = start
    while r > stop:
        yield r
        r += step

l = 1000
l_prime = 17
for k in range(5, 100, 5):
    for epsilon in float_range(0.2, 0.01, -0.01):
        t = calc_threshold(k, l_prime, l, epsilon)
        if t > 0:
            print k, epsilon
            break
            