#!/usr/bin/python

from matrix import eval_poly, generate_curve_coeffs as gcc, make_bezier as mkbz

P = [1, 2, 1]
x = 8

print eval_poly(P, x), " ... should be 81"

P = [1, -2, 1]

print eval_poly(P, x), " ... should be 49"

P = [5, 8, 20, 2, 1]
x = 1

print eval_poly(P, x), " ... should be ", sum(P)

M = mkbz()
print M

P = gcc(1, 1, 1, 1, M)
print P

